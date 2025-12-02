from django.db import models
from django.core.exceptions import ValidationError

class Category(models.Model):
    name = models.CharField(max_length=128, verbose_name='Kategori Adı')
    is_active = models.BooleanField(default=True, verbose_name='Kategori Durumu (Aktif veya Pasif)', help_text='İşaret kaldırılır ise kategori artık pasif hale gelir.')
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Üst Kategori', help_text='Bu kategori, bir üst kategoriye sahipse lütfen seçiniz.')

    class Meta:
        verbose_name_plural = 'Kategoriler'
        verbose_name = 'Kategori'

    def __str__(self):
        chain = []
        p = self

        while p:
            chain.append(p.name)
            p = p.parent_category

        chain.reverse()
        return " > ".join(chain)

class Product(models.Model):
    name = models.CharField(max_length=128, verbose_name='Ürün Adı')
    description = models.TextField(verbose_name='Ürün Açıklaması')
    stock = models.IntegerField(default=0, verbose_name='Ürün Stok Sayısı')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ürün Fiyatı (TL)')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Ürünler'
        verbose_name = 'Ürün'
    
    def __str__(self):
        return self.name


class Feature(models.Model):
    INPUT_TYPES = (
        ('select', 'Seçilebilir (Örn: Yaka Tipi, Desen Tipi)'),
        ('number', 'Sayısal Değer (Örn: Beden, Boy)'),
        ('text', 'Serbest Metin (Diğer)'),
    )
    
    name = models.CharField(max_length=100, verbose_name='Özellik Adı')
    input_type = models.CharField(max_length=10, choices=INPUT_TYPES, default='select', verbose_name='Veri Tipi')
    unit = models.CharField(max_length=20, blank=True, null=True, verbose_name='Birim')

    class Meta:
        verbose_name_plural = 'Özellikler'
        verbose_name = 'Özellik'

    def __str__(self):
        return f"{self.name} ({self.get_input_type_display()})"


class FeatureValue(models.Model):
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, related_name='values', verbose_name='Özellik Adı')
    value = models.CharField(max_length=100, verbose_name='Değeri')

    class Meta:
        verbose_name_plural = 'Özellik Değerleri'
        verbose_name = 'Özellik Değeri'
        
    def __str__(self):
        return f"{self.feature.name}: {self.value}"


class ProductFeature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='features', verbose_name='Ürün')
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, verbose_name='Özellik',)
    value_selected = models.ForeignKey(FeatureValue, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Seçilebilir Değer')
    value_custom = models.CharField(max_length=255, null=True, blank=True, verbose_name='Serbest Metin/Sayısal Değer')

    class Meta:
        verbose_name_plural = 'Ürün Özellikleri'
        verbose_name = 'Ürün Özelliği'
        unique_together = ('product', 'feature')

    @property
    def get_value(self):
        if self.feature.input_type == 'select' and self.value_selected:
            return self.value_selected.value
        elif self.value_custom:
            return f"{self.value_custom} {self.feature.unit if self.feature.unit else ''}"
        return "-"
    
    def clean(self):
        # 1. Eğer tip Select ise ama seçim yapılmamışsa hata ver
        if self.feature.input_type == 'select' and not self.value_selected:
            raise ValidationError('Bu özellik seçmeli tiptedir, lütfen listeden bir değer seçin.')
        
        # 2. Eğer tip Select ise ama gidip elle değer yazılmışsa hata ver
        if self.feature.input_type == 'select' and self.value_custom:
             raise ValidationError('Bu özellik seçmeli tiptedir, manuel değer giremezsiniz.')

        # 3. Eğer tip Number/Text ise ama seçim yapılmışsa hata ver
        if self.feature.input_type != 'select' and self.value_selected:
            raise ValidationError('Bu özellik manuel giriş gerektirir, listeden seçim yapamazsınız.')
            
        # 4. Eğer tip Number ise ve girilen değer sayı değilse (Opsiyonel kontrol)
        if self.feature.input_type == 'number' and self.value_custom:
            if not self.value_custom.isdigit():
                 raise ValidationError('Lütfen geçerli bir sayı giriniz.')
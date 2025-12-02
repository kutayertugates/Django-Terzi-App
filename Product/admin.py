from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('is_active', 'name', 'parent_category')

    list_filter = ('is_active', 'parent_category')

    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'stock', 'price')

    list_filter = ('stock', 'price')

    search_fields = ('name', 'description', 'stock', 'price')

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'input_type', 'unit')

    list_filter = ('input_type', 'unit')

    search_fields = ('name',)

@admin.register(FeatureValue)
class FeatureValueAdmin(admin.ModelAdmin):
    list_display = ('feature', 'value')

    list_filter = ('feature',)

    search_fields = ('feature', 'value')

@admin.register(ProductFeature)
class ProductFeatureAdmin(admin.ModelAdmin):
    list_display = ('product', 'feature', 'value_selected', 'value_custom')

    list_filter = ('product', 'feature')

    search_fields = ('product', 'product')


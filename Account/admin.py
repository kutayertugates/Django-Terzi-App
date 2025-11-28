from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Tabloda Gözükecek Alanlar
    list_display = ['username', 'email', 'is_staff']

    fieldsets = UserAdmin.fieldsets + (
        ('Ekstra Bilgiler', {'fields': ('bio',)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields' : ('email',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
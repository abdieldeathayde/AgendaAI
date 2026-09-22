from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_active',
    )
    fieldsets = UserAdmin.fieldsets + (
        (
            'Informações extras',
            {'fields': ('phone', 'is_customer', 'is_professional')},
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            'Informações extras',
            {'fields': ('phone', 'is_customer', 'is_professional')},
        ),
    )

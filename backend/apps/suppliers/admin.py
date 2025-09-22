"""
Admin configurations for the suppliers app.
"""
from django.contrib import admin

from .models import Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Supplier model.
    """
    list_display = ('name', 'supplier_type', 'contact_name',
                    'email', 'phone', 'is_active')
    search_fields = ('name', 'contact_name', 'email', 'phone')
    list_filter = ('supplier_type', 'is_active')
    ordering = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'supplier_type', 'is_active')
        }),
        ('Contact Information', {
            'fields': ('contact_name', 'email', 'phone', 'website', 'address')
        }),
        ('Additional Details', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
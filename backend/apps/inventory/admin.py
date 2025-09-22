"""
Admin configurations for the inventory app.
"""
from django.contrib import admin

from .models import (BatchInfo, Category, InventoryCount, InventoryItem,
                     Medication, StockAlert, StockTransaction, StockTransfer)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for the Category model."""
    list_display = ('name', 'code', 'parent_category', 'level')
    search_fields = ('name', 'code')
    list_filter = ('level',)
    ordering = ('code',)


@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    """Admin configuration for the Medication model."""
    list_display = ('name', 'drug_code', 'category',
                    'strength', 'is_active')
    search_fields = ('name', 'generic_name', 'brand_name', 'drug_code')
    list_filter = ('category', 'is_active', 'controlled_substance')
    ordering = ('name',)


class BatchInfoInline(admin.TabularInline):
    """Inline representation of BatchInfo for the InventoryItem admin page."""
    model = BatchInfo
    extra = 1
    readonly_fields = ('received_date',)


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    """Admin configuration for the InventoryItem model."""
    list_display = ('medication', 'current_stock',
                    'stock_status', 'status', 'shelf_location')
    search_fields = ('medication__name',)
    list_filter = ('status', 'storage_temp')
    ordering = ('medication__name',)
    readonly_fields = ('stock_status',)
    inlines = [BatchInfoInline]


@admin.register(BatchInfo)
class BatchInfoAdmin(admin.ModelAdmin):
    """Admin configuration for the BatchInfo model."""
    list_display = ('inventory_item', 'batch_number',
                    'expiry_date', 'current_quantity', 'is_expired')
    search_fields = ('batch_number', 'lot_number',
                     'inventory_item__medication__name')
    list_filter = ('is_expired', 'is_recalled', 'supplier')
    ordering = ('expiry_date',)


@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
    """Admin configuration for the StockTransaction model."""
    list_display = ('inventory_item', 'transaction_type',
                    'quantity', 'created_by', 'created_at')
    search_fields = ('reference_number', 'inventory_item__medication__name')
    list_filter = ('transaction_type', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_by', 'created_at')


@admin.register(StockAlert)
class StockAlertAdmin(admin.ModelAdmin):
    """Admin configuration for the StockAlert model."""
    list_display = ('inventory_item', 'alert_type',
                    'priority', 'is_active', 'is_resolved')
    search_fields = ('inventory_item__medication__name', 'message')
    list_filter = ('alert_type', 'priority', 'is_active', 'is_resolved')
    ordering = ('-created_at',)


@admin.register(StockTransfer)
class StockTransferAdmin(admin.ModelAdmin):
    """Admin configuration for the StockTransfer model."""
    list_display = ('from_location', 'to_location',
                    'inventory_item', 'quantity', 'status')
    search_fields = ('from_location', 'to_location',
                     'inventory_item__medication__name')
    list_filter = ('status',)
    ordering = ('-transfer_date',)


@admin.register(InventoryCount)
class InventoryCountAdmin(admin.ModelAdmin):
    """Admin configuration for the InventoryCount model."""
    list_display = ('inventory_item', 'counted_by',
                    'expected_quantity', 'actual_quantity', 'discrepancy', 'status')
    search_fields = ('inventory_item__medication__name', 'counted_by__email')
    list_filter = ('status', 'count_date')
    ordering = ('-count_date',)
    readonly_fields = ('discrepancy',)
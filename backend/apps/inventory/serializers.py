"""
Serializers for the inventory app.

This module defines serializers for the inventory models, following DRF best
practices for handling nested and relational data. It provides both detailed
and minimal serializers to optimize data representation for read and write
operations, preventing issues like circular dependencies and oversized payloads.
"""
from rest_framework import serializers

from .models import (
    Category, Medication, InventoryItem, BatchInfo, StockTransaction,
    StockAlert, StockTransfer, InventoryCount
)
from apps.suppliers.models import Supplier


# --- Minimal Serializers for Nested Representations ---

class MedicationMinimalSerializer(serializers.ModelSerializer):
    """Minimal serializer for nested Medication representation."""
    class Meta:
        model = Medication
        fields = ('medication_id', 'name', 'strength', 'drug_code')


class InventoryItemMinimalSerializer(serializers.ModelSerializer):
    """Minimal serializer for nested InventoryItem representation."""
    medication = MedicationMinimalSerializer(read_only=True)

    class Meta:
        model = InventoryItem
        fields = ('inventory_item_id', 'medication', 'shelf_location', 'current_stock')


class BatchInfoMinimalSerializer(serializers.ModelSerializer):
    """Minimal serializer for nested BatchInfo representation."""
    class Meta:
        model = BatchInfo
        fields = ('id', 'batch_number', 'lot_number', 'expiry_date')


# --- Main Serializers ---

class CategorySerializer(serializers.ModelSerializer):
    """Serializer for the Category model."""

    class Meta:
        """Meta options for the CategorySerializer."""
        model = Category
        fields = (
            'category_id', 'name', 'code', 'description', 'parent_category',
            'level', 'requires_special_handling', 'storage_requirements'
        )
        read_only_fields = ('category_id', 'level')


class MedicationSerializer(serializers.ModelSerializer):
    """Serializer for creating and retrieving Medication instances."""
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )

    class Meta:
        """Meta options for the MedicationSerializer."""
        model = Medication
        fields = (
            'medication_id', 'name', 'generic_name', 'brand_name', 'dosage_form',
            'strength', 'active_ingredient', 'drug_code', 'category', 'category_id',
            'requires_prescription', 'controlled_substance', 'is_active',
            'created_at', 'updated_at'
        )
        read_only_fields = ('medication_id', 'created_at', 'updated_at')


class InventoryItemSerializer(serializers.ModelSerializer):
    """Serializer for creating and retrieving InventoryItem instances."""
    medication = MedicationMinimalSerializer(read_only=True)
    medication_id = serializers.PrimaryKeyRelatedField(
        queryset=Medication.objects.all(), source='medication', write_only=True
    )
    stock_status = serializers.CharField(read_only=True)

    class Meta:
        """Meta options for the InventoryItemSerializer."""
        model = InventoryItem
        fields = '__all__'
        read_only_fields = ('inventory_item_id',)


class BatchInfoSerializer(serializers.ModelSerializer):
    """Serializer for creating and retrieving BatchInfo instances."""
    inventory_item = InventoryItemMinimalSerializer(read_only=True)
    inventory_item_id = serializers.PrimaryKeyRelatedField(
        queryset=InventoryItem.objects.all(), source='inventory_item', write_only=True
    )
    supplier_id = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.all(), source='supplier', write_only=True
    )
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)

    class Meta:
        """Meta options for the BatchInfoSerializer."""
        model = BatchInfo
        fields = (
            'id', 'inventory_item', 'inventory_item_id', 'batch_number', 'lot_number',
            'manufacture_date', 'expiry_date', 'received_date', 'received_quantity',
            'current_quantity', 'supplier_id', 'supplier_name', 'purchase_order',
            'is_expired', 'is_recalled', 'recall_reason'
        )
        read_only_fields = ('id', 'received_date', 'is_expired')


class StockTransactionSerializer(serializers.ModelSerializer):
    """Serializer for the StockTransaction model."""
    inventory_item = InventoryItemMinimalSerializer(read_only=True)
    inventory_item_id = serializers.PrimaryKeyRelatedField(
        queryset=InventoryItem.objects.all(), source='inventory_item', write_only=True
    )
    batch_info = BatchInfoMinimalSerializer(read_only=True, required=False)
    batch_info_id = serializers.PrimaryKeyRelatedField(
        queryset=BatchInfo.objects.all(), source='batch_info',
        write_only=True, required=False, allow_null=True
    )
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        """Meta options for the StockTransactionSerializer."""
        model = StockTransaction
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'created_by')


class StockAlertSerializer(serializers.ModelSerializer):
    """Serializer for the StockAlert model."""
    inventory_item = InventoryItemMinimalSerializer(read_only=True)
    inventory_item_id = serializers.PrimaryKeyRelatedField(
        queryset=InventoryItem.objects.all(), source='inventory_item', write_only=True
    )
    batch_info = BatchInfoMinimalSerializer(read_only=True, required=False)
    batch_info_id = serializers.PrimaryKeyRelatedField(
        queryset=BatchInfo.objects.all(), source='batch_info',
        write_only=True, required=False, allow_null=True
    )
    resolved_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        """Meta options for the StockAlertSerializer."""
        model = StockAlert
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'resolved_at', 'resolved_by')


class StockTransferSerializer(serializers.ModelSerializer):
    """Serializer for the StockTransfer model."""
    inventory_item = InventoryItemMinimalSerializer(read_only=True)
    inventory_item_id = serializers.PrimaryKeyRelatedField(
        queryset=InventoryItem.objects.all(), source='inventory_item', write_only=True
    )
    batch_info = BatchInfoMinimalSerializer(read_only=True, required=False)
    batch_info_id = serializers.PrimaryKeyRelatedField(
        queryset=BatchInfo.objects.all(), source='batch_info',
        write_only=True, required=False, allow_null=True
    )

    class Meta:
        """Meta options for the StockTransferSerializer."""
        model = StockTransfer
        fields = '__all__'
        read_only_fields = ('transfer_id', 'transfer_date', 'completed_date')


class InventoryCountSerializer(serializers.ModelSerializer):
    """Serializer for the InventoryCount model."""
    inventory_item = InventoryItemMinimalSerializer(read_only=True)
    inventory_item_id = serializers.PrimaryKeyRelatedField(
        queryset=InventoryItem.objects.all(), source='inventory_item', write_only=True
    )
    counted_by = serializers.StringRelatedField(read_only=True)
    discrepancy = serializers.IntegerField(read_only=True)

    class Meta:
        """Meta options for the InventoryCountSerializer."""
        model = InventoryCount
        fields = '__all__'
        read_only_fields = ('count_id', 'count_date', 'discrepancy', 'counted_by')
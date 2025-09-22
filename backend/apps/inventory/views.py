"""
Views for the inventory app.

This module provides viewsets for all inventory-related models,
implementing DRF best practices for a scalable and efficient API.
Key features include:
- Query optimization with `select_related` and `prefetch_related`.
- Advanced filtering, searching, and ordering capabilities.
- Custom actions for specific business logic (e.g., resolving alerts).
- Automated field population (e.g., `created_by` user).
"""
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from .models import (
    Category, Medication, InventoryItem, BatchInfo, StockTransaction,
    StockAlert, StockTransfer, InventoryCount
)
from .serializers import (
    CategorySerializer, MedicationSerializer, InventoryItemSerializer,
    BatchInfoSerializer, StockTransactionSerializer, StockAlertSerializer,
    StockTransferSerializer, InventoryCountSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    """API endpoint for managing drug categories."""
    queryset = Category.objects.all().select_related('parent_category')
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['level', 'requires_special_handling']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'level']


class MedicationViewSet(viewsets.ModelViewSet):
    """API endpoint for managing medications."""
    queryset = Medication.objects.all().select_related('category')
    serializer_class = MedicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'dosage_form', 'requires_prescription', 'is_active']
    search_fields = ['name', 'generic_name', 'brand_name', 'drug_code']
    ordering_fields = ['name', 'generic_name', 'created_at']


class InventoryItemViewSet(viewsets.ModelViewSet):
    """API endpoint for managing inventory items."""
    queryset = InventoryItem.objects.all().select_related('medication__category')
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'storage_temp', 'medication__category']
    search_fields = ['medication__name', 'shelf_location']
    ordering_fields = ['medication__name', 'current_stock', 'last_counted']


class BatchInfoViewSet(viewsets.ModelViewSet):
    """API endpoint for managing medication batches."""
    queryset = BatchInfo.objects.all().select_related('inventory_item__medication', 'supplier')
    serializer_class = BatchInfoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['inventory_item', 'supplier', 'is_expired', 'is_recalled']
    search_fields = ['batch_number', 'lot_number', 'purchase_order']
    ordering_fields = ['expiry_date', 'received_date']


class StockTransactionViewSet(viewsets.ModelViewSet):
    """API endpoint for auditing stock transactions."""
    queryset = StockTransaction.objects.all().select_related(
        'inventory_item__medication', 'batch_info', 'created_by'
    )
    serializer_class = StockTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['transaction_type', 'inventory_item', 'created_by']
    ordering_fields = ['-created_at']

    def perform_create(self, serializer):
        """Set the `created_by` field to the current user."""
        serializer.save(created_by=self.request.user)


class StockAlertViewSet(viewsets.ModelViewSet):
    """API endpoint for managing stock alerts."""
    queryset = StockAlert.objects.all().select_related(
        'inventory_item__medication', 'batch_info', 'resolved_by'
    )
    serializer_class = StockAlertSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['alert_type', 'priority', 'is_active', 'is_resolved']
    ordering_fields = ['-created_at', 'priority']

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def resolve(self, request, pk=None):
        """Mark an alert as resolved."""
        alert = self.get_object()
        if alert.is_resolved:
            return Response({'status': 'Alert already resolved'}, status=status.HTTP_400_BAD_REQUEST)
        
        alert.is_resolved = True
        alert.is_active = False
        alert.resolved_by = request.user
        alert.resolved_at = timezone.now()
        alert.resolution_notes = request.data.get('notes', 'Resolved via API.')
        alert.save()
        
        serializer = self.get_serializer(alert)
        return Response(serializer.data)


class StockTransferViewSet(viewsets.ModelViewSet):
    """API endpoint for managing stock transfers."""
    queryset = StockTransfer.objects.all().select_related('inventory_item__medication', 'batch_info')
    serializer_class = StockTransferSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'from_location', 'to_location']
    search_fields = ['inventory_item__medication__name', 'notes']
    ordering_fields = ['-transfer_date']

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark a stock transfer as completed."""
        transfer = self.get_object()
        if transfer.status == 'COMPLETED':
            return Response({'status': 'Transfer already completed'}, status=status.HTTP_400_BAD_REQUEST)
        
        transfer.status = 'COMPLETED'
        transfer.completed_date = timezone.now()
        transfer.save()
        return Response({'status': 'Transfer marked as completed'})


class InventoryCountViewSet(viewsets.ModelViewSet):
    """API endpoint for managing physical inventory counts."""
    queryset = InventoryCount.objects.all().select_related('inventory_item__medication', 'counted_by')
    serializer_class = InventoryCountSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'inventory_item']
    ordering_fields = ['-count_date']

    def perform_create(self, serializer):
        """Set the `counted_by` field to the current user."""
        serializer.save(counted_by=self.request.user)

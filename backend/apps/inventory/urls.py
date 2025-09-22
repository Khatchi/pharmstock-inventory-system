"""
URL configuration for the inventory app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    MedicationViewSet,
    InventoryItemViewSet,
    BatchInfoViewSet,
    StockTransactionViewSet,
    StockAlertViewSet,
    StockTransferViewSet,
    InventoryCountViewSet,
)

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'medications', MedicationViewSet, basename='medication')
router.register(r'inventory-items', InventoryItemViewSet, basename='inventoryitem')
router.register(r'batches', BatchInfoViewSet, basename='batchinfo')
router.register(r'transactions', StockTransactionViewSet, basename='stocktransaction')
router.register(r'alerts', StockAlertViewSet, basename='stockalert')
router.register(r'transfers', StockTransferViewSet, basename='stocktransfer')
router.register(r'counts', InventoryCountViewSet, basename='inventorycount')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]

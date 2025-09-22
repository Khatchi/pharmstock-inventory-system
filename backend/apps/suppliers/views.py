"""
Views for the suppliers app.

This module provides the viewset for the Supplier model, with support
for filtering, searching, and ordering to allow for efficient querying
of supplier data.
"""
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Supplier
from .serializers import SupplierSerializer

class SupplierViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and managing suppliers.

    Provides full CRUD functionality for suppliers. Includes filtering by
    supplier type and active status, as well as full-text search on key
    contact fields.
    """
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['supplier_type', 'is_active']
    search_fields = ['name', 'contact_name', 'email', 'phone', 'address']
    ordering_fields = ['name', 'created_at']

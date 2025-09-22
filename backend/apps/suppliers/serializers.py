"""
Serializers for the suppliers app.
"""
from rest_framework import serializers
from .models import Supplier


class SupplierSerializer(serializers.ModelSerializer):
    """Serializer for the Supplier model."""

    class Meta:
        """Meta options for the SupplierSerializer."""
        model = Supplier
        fields = '__all__'
        read_only_fields = ('supplier_id', 'created_at', 'updated_at')

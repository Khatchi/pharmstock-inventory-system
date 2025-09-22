"""
Supplier models for the pharmstock application.
"""
import uuid
from django.db import models


# Create your models here.

SUPPLIER_TYPES = [
        ('MANUFACTURER', 'Manufacturer'),
        ('DISTRIBUTOR', 'Distributor'),
        ('WHOLESALER', 'Wholesaler'),
        ('OTHER', 'Other'),
    ]


class Supplier(models.Model):
    """
    Supplier information for tracking medications
    """
    supplier_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    supplier_type = models.CharField(max_length=20, choices=SUPPLIER_TYPES, default='DISTRIBUTOR')
    name = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    is_active = models.BooleanField(default=True)
    website = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta class for Supplier model
        """
        ordering = ['name']
        app_label = 'suppliers'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['email']),
            models.Index(fields=['is_active']),
            ]

    def __str__(self):
        """Return a string representation of the supplier."""
        return f"{self.name}"
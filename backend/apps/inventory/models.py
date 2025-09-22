"""
Inventory models for the pharmstock application.
"""
import uuid
from enum import Enum

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

# Choices for models
DOSAGE_FORMS = [
    ('TAB', 'Tablet'),
    ('CAP', 'Capsule'),
    ('SYR', 'Syrup'),
    ('INJ', 'Injection'),
    ('CRE', 'Cream'),
    ('OIN', 'Ointment'),
    ('SUS', 'Suspension'),
    ('SOL', 'Solution'),
    ('POW', 'Powder'),
    ('AER', 'Aerosol'),
]

STORAGE_TEMP_CHOICES = [
    ('ROOM', 'Room Temperature'),
    ('REFRIGERATED', 'Refrigerated (2-8°C)'),
    ('FROZEN', 'Frozen (-20°C)'),
    ('SPECIAL', 'Special Conditions'),
]

TRANSACTION_TYPES = [
    ('IN', 'Stock In'),
    ('OUT', 'Stock Out'),
    ('ADJUST', 'Adjustment'),
    ('TRANSFER', 'Transfer'),
    ('RETURN', 'Return'),
    ('EXPIRED', 'Expired/Disposed'),
    ('DAMAGED', 'Damaged'),
]

ALERT_TYPES = [
    ('LOW_STOCK', 'Low Stock'),
    ('EXPIRED', 'Expired'),
    ('EXPIRING_SOON', 'Expiring Soon'),
    ('OVERSTOCK', 'Overstock'),
    ('OUT_OF_STOCK', 'Out of Stock'),
    ('NEAR_EXPIRY', 'Near Expiry'),
    ('RECALL', 'Recall Alert'),
]

PRIORITY_LEVELS = [
    ('LOW', 'Low'),
    ('MEDIUM', 'Medium'),
    ('HIGH', 'High'),
    ('CRITICAL', 'Critical'),
]

TRANSFER_STATUS = [
    ('PENDING', 'Pending'),
    ('IN_TRANSIT', 'In Transit'),
    ('COMPLETED', 'Completed'),
    ('CANCELLED', 'Cancelled'),
]

COUNT_STATUS = [
    ('PENDING', 'Pending'),
    ('IN_PROGRESS', 'In Progress'),
    ('COMPLETED', 'Completed'),
    ('DISCREPANCY', 'Discrepancy Found'),
]

STATUS_CHOICES = [
    ('ACTIVE', 'Active'),
    ('DISCONTINUED', 'Discontinued'),
    ('RESTRICTED', 'Restricted'),
    ('QUARANTINED', 'Quarantined'),
]


class StockStatus(Enum):
    """Enum for the status of the stock."""
    OUT_OF_STOCK = 'OUT_OF_STOCK'
    LOW_STOCK = 'LOW_STOCK'
    OVERSTOCK = 'OVERSTOCK'
    NORMAL = 'NORMAL'


class Category(models.Model):
    """Drug classification system with hierarchical structure"""
    category_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    parent_category = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE)
    level = models.PositiveIntegerField(default=0, editable=False)

    # Regulatory
    requires_special_handling = models.BooleanField(default=False)
    storage_requirements = models.TextField(blank=True)

    class Meta:
        """Meta options for the Category model."""
        app_label = 'inventory'
        verbose_name_plural = "categories"
        ordering = ['code']

    def __str__(self):
        """Return a string representation of the category."""
        return f"{self.code} - {self.name}"

    def save(self, *args, **kwargs):
        """Save the category and update the level."""
        self.level = self._get_level()
        super().save(*args, **kwargs)

    def _get_level(self):
        """Return the level of the category in the hierarchy."""
        level = 0
        p = self.parent_category
        while p:
            level += 1
            p = p.parent_category
        return level


class Medication(models.Model):
    """Primary medication entity with regulatory information"""
    medication_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)

    # Basic Information
    name = models.CharField(max_length=200)
    generic_name = models.CharField(max_length=200)
    brand_name = models.CharField(max_length=200, blank=True)

    # Medical Details
    dosage_form = models.CharField(max_length=3, choices=DOSAGE_FORMS)
    strength = models.CharField(max_length=50)
    active_ingredient = models.CharField(max_length=200)

    # Regulatory
    drug_code = models.CharField(
        max_length=50, unique=True)  # NDC, DIN, etc.
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    # Business Rules
    requires_prescription = models.BooleanField(default=True)
    controlled_substance = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta options for the Medication model."""
        app_label = 'inventory'
        ordering = ['name']
        indexes = [
            models.Index(fields=['drug_code']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        """Return a string representation of the medication."""
        return f"{self.name} ({self.strength})"


class InventoryItem(models.Model):
    """Stock management for medications"""
    medication = models.ForeignKey(
        Medication, on_delete=models.PROTECT, related_name='inventory_items')

    # Stock Levels
    inventory_item_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    current_stock = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0)])
    minimum_threshold = models.PositiveIntegerField(
        validators=[MinValueValidator(0)])
    maximum_capacity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)])
    reorder_point = models.PositiveIntegerField(
        validators=[MinValueValidator(0)])
    reorder_quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)])

    # Location
    shelf_location = models.CharField(max_length=50)
    storage_temp = models.CharField(
        max_length=12, choices=STORAGE_TEMP_CHOICES, default='ROOM')

    # Status
    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES, default='ACTIVE')
    last_counted = models.DateTimeField(null=True, blank=True)

    # Pricing
    unit_cost = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    selling_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    class Meta:
        """Meta options for the InventoryItem model."""
        app_label = 'inventory'
        ordering = ['medication__name']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['current_stock']),
        ]

    @property
    def medication_name(self):
        """Returns the name of the medication."""
        return self.medication.name

    def __str__(self):
        """Return a string representation of the inventory item."""
        return f"{self.medication_name} - Stock: {self.current_stock}"

    @property
    def stock_status(self):
        """Return the stock status of the inventory item."""
        if self.current_stock == 0:
            return StockStatus.OUT_OF_STOCK.value
        if self.current_stock <= self.minimum_threshold:
            return StockStatus.LOW_STOCK.value
        if self.current_stock >= self.maximum_capacity * 0.9:
            return StockStatus.OVERSTOCK.value
        return StockStatus.NORMAL.value


class BatchInfo(models.Model):
    """Lot/Batch tracking with expiration management"""
    inventory_item = models.ForeignKey(
        InventoryItem, on_delete=models.PROTECT, related_name='batches')

    # Batch Details
    batch_number = models.CharField(max_length=100)
    lot_number = models.CharField(max_length=100, blank=True)

    # Dates
    manufacture_date = models.DateField()
    expiry_date = models.DateField()
    received_date = models.DateField(auto_now_add=True)

    # Quantities
    received_quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)])
    current_quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(0)])

    # Supplier Info - Reference to your existing supplier app
    supplier = models.ForeignKey('suppliers.Supplier', on_delete=models.PROTECT)
    purchase_order = models.CharField(max_length=100, blank=True)

    # Status
    is_expired = models.BooleanField(default=False)
    is_recalled = models.BooleanField(default=False)
    recall_reason = models.TextField(blank=True)

    class Meta:
        """Meta options for the BatchInfo model."""
        app_label = 'inventory'
        ordering = ['expiry_date']
        unique_together = ['inventory_item', 'batch_number']
        indexes = [
            models.Index(fields=['expiry_date']),
            models.Index(fields=['is_expired']),
        ]

    def __str__(self):
        """Return a string representation of the batch info."""
        return f"Batch {self.batch_number} - {self.inventory_item.medication_name}"

    def save(self, *args, **kwargs):
        """Save the batch info and update the expired status."""
        # Auto-update expired status
        if self.expiry_date and self.expiry_date < timezone.now().date():
            self.is_expired = True
        super().save(*args, **kwargs)


class StockTransaction(models.Model):
    """Audit trail for all stock movements"""
    inventory_item = models.ForeignKey(
        InventoryItem, on_delete=models.PROTECT, related_name='transactions')
    batch_info = models.ForeignKey(
        BatchInfo, on_delete=models.SET_NULL, null=True, blank=True)

    # Transaction Details
    transaction_type = models.CharField(
        max_length=10, choices=TRANSACTION_TYPES)
    quantity = models.IntegerField()  # positive for IN, negative for OUT

    # References
    reference_number = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)

    # Audit
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta options for the StockTransaction model."""
        app_label = 'inventory'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['transaction_type']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        """Return a string representation of the stock transaction."""
        return f"{self.transaction_type} - {self.quantity} units"


class StockAlert(models.Model):
    """Automated monitoring and alert system"""
    inventory_item = models.ForeignKey(
        InventoryItem, on_delete=models.PROTECT, related_name='alerts')
    batch_info = models.ForeignKey(
        BatchInfo, on_delete=models.SET_NULL, null=True, blank=True)

    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS)
    message = models.TextField()

    # Status
    is_active = models.BooleanField(default=True)
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    resolution_notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta options for the StockAlert model."""
        app_label = 'inventory'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['alert_type']),
        ]

    def __str__(self):
        """Return a string representation of the stock alert."""
        return f"{self.alert_type} - {self.inventory_item.medication_name}"


class StockTransfer(models.Model):
    """Inter-location stock transfers"""
    transfer_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    inventory_item = models.ForeignKey(
        InventoryItem, on_delete=models.PROTECT)
    batch_info = models.ForeignKey(
        BatchInfo, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(
        max_length=10, choices=TRANSFER_STATUS, default='PENDING')
    transfer_date = models.DateTimeField(auto_now_add=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        """Meta options for the StockTransfer model."""
        app_label = 'inventory'
        ordering = ['-transfer_date']

    def __str__(self):
        """Return a string representation of the stock transfer."""
        return f"Transfer #{self.transfer_id} - {self.inventory_item.medication_name}"


class InventoryCount(models.Model):
    """Physical inventory counts"""
    count_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    inventory_item = models.ForeignKey(
        InventoryItem, on_delete=models.PROTECT)
    counted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    expected_quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(0)])
    actual_quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(0)])
    count_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=12, choices=COUNT_STATUS, default='PENDING')
    notes = models.TextField(blank=True)

    class Meta:
        """Meta options for InventoryCount."""
        app_label = 'inventory'
        ordering = ['-count_date']

    def __str__(self):
        """Return a string representation of the inventory count."""
        return f"Count #{self.count_id} - {self.inventory_item.medication_name}"

    @property
    def discrepancy(self):
        """Calculate the difference between actual and expected quantities."""
        if self.actual_quantity is None or self.expected_quantity is None:
            return None
        return self.actual_quantity - self.expected_quantity

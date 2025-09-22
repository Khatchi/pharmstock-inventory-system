"""
Reports models for the pharmstock application.
"""
import uuid

from django.db import models
from django.conf import settings

# Choices for models
REPORT_TYPES = [
    ('INVENTORY_LEVEL', 'Inventory Level Report'),
    ('EXPIRATION', 'Expiration Report'),
    ('TRANSACTION_HISTORY', 'Transaction History Report'),
    ('SUPPLIER_PERFORMANCE', 'Supplier Performance Report'),
    ('LOW_STOCK', 'Low Stock Report'),
    ('STOCK_ADJUSTMENT', 'Stock Adjustment Report'),
]

REPORT_STATUS = [
    ('PENDING', 'Pending'),
    ('PROCESSING', 'Processing'),
    ('COMPLETED', 'Completed'),
    ('FAILED', 'Failed'),
]

FILE_FORMATS = [
    ('PDF', 'PDF'),
    ('CSV', 'CSV'),
    ('JSON', 'JSON'),
]


class Report(models.Model):
    """
    Model to store generated reports.
    """
    report_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    report_type = models.CharField(max_length=50, choices=REPORT_TYPES)
    generated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=20, choices=REPORT_STATUS, default='PENDING')
    file_format = models.CharField(max_length=10, choices=FILE_FORMATS)
    report_file = models.FileField(
        upload_to='reports/', null=True, blank=True)
    parameters = models.JSONField(default=dict, blank=True)
    file_size = models.PositiveIntegerField(
        null=True, blank=True, editable=False)
    execution_time = models.DurationField(null=True, blank=True)
    error_message = models.TextField(blank=True, null=True)

    class Meta:
        """Meta options for the Report model."""
        app_label = 'reports'
        ordering = ['-generated_at']
        indexes = [
            models.Index(fields=['report_type']),
            models.Index(fields=['status']),
            models.Index(fields=['generated_at']),
            models.Index(fields=['report_type', 'status']),
        ]

    def __str__(self):
        """Return a string representation of the report."""
        return f"{self.get_report_type_display()} ({self.start_date} to {self.end_date})"

    @property
    def is_available(self):
        """Return True if the report is completed and the file exists."""
        return self.status == 'COMPLETED' and bool(self.report_file)

    def get_file_size_display(self):
        """
        Return a human-readable file size (e.g., KB, MB, GB).
        """
        if not self.file_size:
            return "0 Bytes"

        size = self.file_size
        if size < 1024:
            return f"{size} Bytes"
        if size < 1024**2:
            return f"{size / 1024:.2f} KB"
        if size < 1024**3:
            return f"{size / (1024**2):.2f} MB"
        return f"{size / (1024**3):.2f} GB"

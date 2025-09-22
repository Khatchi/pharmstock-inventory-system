"""
Serializers for the reports app.
"""
from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    """Serializer for the Report model."""
    generated_by = serializers.StringRelatedField(read_only=True)
    is_available = serializers.BooleanField(read_only=True)
    file_size_display = serializers.CharField(
        source='get_file_size_display', read_only=True
    )

    class Meta:
        """Meta options for the ReportSerializer."""
        model = Report
        fields = (
            'report_id', 'report_type', 'generated_by', 'generated_at',
            'start_date', 'end_date', 'status', 'file_format',
            'report_file', 'parameters', 'file_size', 'execution_time',
            'error_message', 'is_available', 'file_size_display'
        )
        read_only_fields = (
            'report_id', 'generated_at', 'report_file', 'file_size',
            'execution_time', 'error_message', 'is_available',
            'file_size_display', 'generated_by'
        )

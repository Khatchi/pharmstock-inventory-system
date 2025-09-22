"""
Admin configurations for the reports app.
"""
from django.contrib import admin

from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Report model.
    """
    list_display = ('report_type', 'generated_by', 'status',
                    'generated_at', 'file_format', 'is_available')
    list_filter = ('report_type', 'status', 'file_format', 'generated_at')
    search_fields = ('generated_by__email', 'report_type')
    ordering = ('-generated_at',)

    # Make the model read-only in the admin, as reports are system-generated
    readonly_fields = [
        'report_id', 'report_type', 'generated_by', 'generated_at',
        'start_date', 'end_date', 'status', 'file_format', 'report_file',
        'parameters', 'file_size', 'execution_time', 'error_message',
        'is_available', 'get_file_size_display'
    ]

    def has_add_permission(self, request):
        """Prevent manual creation of reports."""
        return False

    def has_change_permission(self, request, obj=None):
        """Allow viewing but not changing reports."""
        return False
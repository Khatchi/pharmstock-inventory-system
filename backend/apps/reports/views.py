"""
Views for the reports app.

This module provides a viewset for generating and retrieving reports.
The viewset is read-only for existing reports but allows for the creation
of new report generation tasks. It includes filtering and a custom action
for downloading report files.
"""
from rest_framework import viewsets, permissions, mixins, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend

from .models import Report
from .serializers import ReportSerializer

class ReportViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """
    API endpoint for viewing and generating reports.

    - **List:** Returns a list of all generated reports.
    - **Retrieve:** Returns details of a specific report.
    - **Create:** Initiates the generation of a new report.
      (Note: The actual report generation should be handled asynchronously,
      e.g., by a Celery task).
    - **Download:** A custom action to download the report file.
    """
    queryset = Report.objects.all().select_related('generated_by')
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        'report_type': ['exact'],
        'status': ['exact'],
        'generated_at': ['gte', 'lte', 'exact'],
    }
    ordering_fields = ['-generated_at', 'report_type', 'status']

    def perform_create(self, serializer):
        """
        Set the `generated_by` field to the current user and trigger
        the report generation process.
        """
        # In a real-world application, this is where you would trigger
        # an asynchronous task to generate the report.
        # from .tasks import generate_report_task
        # report = serializer.save(generated_by=self.request.user)
        # generate_report_task.delay(report.report_id)
        serializer.save(generated_by=self.request.user)

    @action(detail=True, methods=['get'], url_path='download')
    def download(self, request, pk=None):
        """
        Provides a direct download link for a completed report file.
        """
        report = self.get_object()
        if report.is_available and report.report_file:
            try:
                # This provides a streaming response, efficient for large files
                return FileResponse(report.report_file.open('rb'), as_attachment=True)
            except FileNotFoundError:
                return Response(
                    {'error': 'Report file not found on storage.'},
                    status=status.HTTP_404_NOT_FOUND
                )
        return Response(
            {'error': 'Report is not available for download.'},
            status=status.HTTP_404_NOT_FOUND
        )

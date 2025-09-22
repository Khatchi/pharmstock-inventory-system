"""
Main URL configuration for the pharmstock project.

This module routes URLs to the appropriate apps and sets up the
API documentation endpoints using drf-yasg for Swagger and ReDoc.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configure the schema view for API documentation
schema_view = get_schema_view(
   openapi.Info(
      title="Pharmstock API",
      default_version='v1',
      description="API documentation for the Pharmstock Inventory Management System.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@pharmstock.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# Main URL patterns for the project
urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints version 1
    path('api/v1/', include([
        path('auth/', include('apps.authentication.urls')),
        path('inventory/', include('apps.inventory.urls')),
        path('reports/', include('apps.reports.urls')),
        path('suppliers/', include('apps.suppliers.urls')),
    ])),

    # API documentation endpoints
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
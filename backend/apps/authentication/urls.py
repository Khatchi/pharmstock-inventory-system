"""
URL configuration for the authentication app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserProfileViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'profiles', UserProfileViewSet, basename='userprofile')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]

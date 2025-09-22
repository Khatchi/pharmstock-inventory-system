"""
Views for the authentication app.

This module provides the viewsets for the User and UserProfile models,
incorporating DRF best practices such as query optimization, filtering,
and searching to ensure efficient and secure data handling.
"""
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import User, UserProfile
from .serializers import UserSerializer, UserProfileSerializer
# Assuming you have custom permissions, e.g., in a shared 'utils' app
# from utils.permissions import IsAdminOrReadOnly, IsOwnerOrAdmin

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and managing users.

    Provides full CRUD functionality for users. Includes filtering by role
    and active status, searching by name and email, and ordering.
    Querysets are optimized using `select_related` to fetch user profiles
    efficiently.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]  # Stricter permissions
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['role', 'is_active']
    search_fields = ['first_name', 'last_name', 'email']
    ordering_fields = ['email', 'first_name', 'last_name', 'date_joined']

    def get_queryset(self):
        """
        Optimize queryset by pre-fetching related user profiles.
        """
        return User.objects.all().select_related('profile').order_by('-date_joined')


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and managing user profiles.

    Allows users to view and edit their own profiles. Administrators can
    access all profiles. The queryset is optimized using `select_related`
    to fetch user data efficiently.
    """
    serializer_class = UserProfileSerializer
    # Example of more granular permissions:
    # permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Restricts the returned profiles to the currently authenticated user,
        unless the user is a staff member, who can see all profiles.
        """
        user = self.request.user
        if user.is_staff:
            return UserProfile.objects.all().select_related('user')
        return UserProfile.objects.filter(user=user).select_related('user')

    def perform_update(self, serializer):
        """
        Ensure that the user being updated is the request user,
        unless the request user is an admin.
        """
        # This logic is better handled by a custom permission class like IsOwnerOrAdmin
        # but is included here for clarity.
        profile = self.get_object()
        if profile.user != self.request.user and not self.request.user.is_staff:
            self.permission_denied(self.request)
        serializer.save()

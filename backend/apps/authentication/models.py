"""
Authentication models for the pharmstock application.
"""
import uuid

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Choices for models
USER_ROLES = [
    ('ADMIN', 'Admin'),
    ('PHARMACIST', 'Pharmacist'),
    ('STAFF', 'Staff'),
    ('MANAGER', 'Manager'),
]


class UserManager(BaseUserManager):
    """
    Custom user manager for email-based authentication.
    """
    
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular user with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'ADMIN')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    """
    user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=20, choices=USER_ROLES, default='STAFF')
    email = models.EmailField(unique=True)

    # Remove username field since we're using email
    username = None

    # Custom manager
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Remove username from required fields

    class Meta:
        """Meta options for the User model."""
        app_label = 'authentication'
        ordering = ['email']
        db_table = 'auth_user'

    def __str__(self):
        """Return a string representation of the user."""
        return self.email


class UserProfile(models.Model):
    """
    Stores additional information for a user.
    """
    profile_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta options for the UserProfile model."""
        app_label = 'authentication'
        ordering = ['user__email']
        db_table = 'auth_user_profile'

    def __str__(self):
        """Return a string representation of the user profile."""
        return f"{self.user.email}'s Profile"


@receiver(post_save, sender=User)
def handle_user_profile(sender, instance, created, **kwargs):
    """
    Create or update user profile when User is saved.
    Uses a single handler to avoid signal recursion.
    """
    if created:
        UserProfile.objects.create(user=instance)
    else:
        # Only save if profile exists to avoid recursion
        if hasattr(instance, 'profile'):
            instance.profile.save()
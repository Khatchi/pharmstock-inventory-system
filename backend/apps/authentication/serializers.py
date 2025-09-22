"""
Serializers for the authentication app.
"""
from rest_framework import serializers
from .models import User, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for the UserProfile model."""

    class Meta:
        """Meta options for the UserProfileSerializer."""
        model = UserProfile
        fields = '__all__'
        read_only_fields = ('profile_id', 'user', 'created_at', 'updated_at')


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    Handles user creation and data serialization.
    """
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        """Meta options for the UserSerializer."""
        model = User
        fields = (
            'user_id', 'email', 'first_name', 'last_name', 'role',
            'is_active', 'is_staff', 'profile', 'password'
        )
        read_only_fields = ('user_id', 'is_staff')
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}}
        }

    def create(self, validated_data):
        """
        Create and return a new user instance, given the validated data.
        Hashes the password before saving.
        """
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        """
        Update and return an existing user instance, given the validated data.
        Handles password updates correctly.
        """
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

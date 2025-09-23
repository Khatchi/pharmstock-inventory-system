"""
Authentication views and serializers for JWT.
"""
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.authentication.serializers import UserSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom token obtain pair serializer to add extra user data to the token.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['user_id'] = str(user.user_id)
        token['role'] = user.role
        
        return token

    def validate(self, attrs):
        """
        Validate the token and add user data to the response.
        """
        data = super().validate(attrs)
        
        # Add user data to the response
        data['user'] = UserSerializer(self.user).data
        
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom token obtain pair view to use the custom serializer.
    """
    serializer_class = CustomTokenObtainPairSerializer

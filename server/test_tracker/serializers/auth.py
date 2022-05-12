from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.state import token_backend
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer,TokenRefreshSerializer
from rest_framework import fields

from typing import Dict, Any


from server.test_tracker.models.users import User
from server.test_tracker.services.users import get_user_by_id

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Override TokenObtainPairSerializer to add extra responses"""
    def validate(self, attrs : Any) -> Dict[str,Any] :
        data:Dict       = super().validate(attrs)
        refresh:Dict    = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access']  = str(refresh.access_token)
        return data


class MyTokenRefreshSerializer(TokenRefreshSerializer):
    """serializer to refresh user token"""
    def validate(self, attrs : Any) -> Dict[str,Any]:
        data = super().validate(attrs)
        decoded_payload = token_backend.decode(data['access'], verify=True)
        user_id=decoded_payload['user_id']
        user = get_user_by_id(user_id)
        refresh = RefreshToken.for_user(user)
        data['refresh'] = str(refresh)
        return data

class RegisterSerializer(ModelSerializer):
    """class RegisterSerializer to serialize the user obj"""
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name',
            'email', 'password'
        )

class LoginSerializer(ModelSerializer):
    """employers, job-seekers serializer class"""
    email = fields.CharField()
    class Meta:
        model = User
        fields = ['email', 'password']
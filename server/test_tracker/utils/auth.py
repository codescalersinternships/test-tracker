from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from server.test_tracker.serializers.auth import (
    MyTokenObtainPairSerializer,
    MyTokenRefreshSerializer
)

class MyTokenObtainPairView(TokenObtainPairView):
    """
    An end point for the user token
    """
    serializer_class = MyTokenObtainPairSerializer

class MyTokenRefreshView(TokenRefreshView):
    """
    An end point to refresh the user token
    """
    serializer_class = MyTokenRefreshSerializer

def get_tokens_for_user(user):
    """Return token for user to authenticate"""
    refresh = RefreshToken.for_user(user)
    response = {
        "access_token": f"{refresh.access_token}",
        "refresh_token": f"{refresh}"
    }
    return response
from rest_framework.serializers import ModelSerializer
from server.test_tracker.models.users import User


class RegisterSerializer(ModelSerializer):
    """class RegisterSerializer to serialize the user obj"""
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name',
            'email', 'password'
        )
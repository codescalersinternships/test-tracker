"""Everything related to Member"""
from typing import Any, Dict
from rest_framework.serializers import ModelSerializer

from server.test_tracker.models.dashboard import Member

class MemberSetPasswordSerializer(ModelSerializer):
    """Class Member to set password for member on Member table"""
    class Meta:
        model = Member
        fields = ['password']

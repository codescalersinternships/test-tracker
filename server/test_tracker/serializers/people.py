"""Everything related to people"""
from typing import Any, Dict
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.hashers import make_password

from server.test_tracker.models.dashboard import People

class PeopleSetPasswordSerializer(ModelSerializer):
    """Class people to set password for person on people table"""
    class Meta:
        model = People
        fields = ['password']

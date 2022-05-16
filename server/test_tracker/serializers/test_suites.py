"""Everything related to TestSuites"""


from server.test_tracker.models.project import TestSuites
from rest_framework.serializers import ModelSerializer

class TestSuitesSerializer(ModelSerializer):
    """class TestSuitesSerializer to serialize the test suite obj"""
    class Meta:
        model = TestSuites
        exclude = ('project',)

"""Everything related to TestSuites and TestCases"""


from attr import fields
from server.test_tracker.models.project import TestSuites, TestCases
from rest_framework.serializers import ModelSerializer

class TestSuitesSerializer(ModelSerializer):
    """class TestSuitesSerializer to serialize the test suite obj"""
    class Meta:
        model = TestSuites
        exclude = ('project',)

class TestCaseSerializer(ModelSerializer):
    """class TestCaseSerializer to serialize the test case obj"""
    class Meta:
        model = TestCases
        fields = ('id','title','test_steps','expected_result', 'verifies_requirements')
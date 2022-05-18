"""Everything related to TestCases"""


from server.test_tracker.models.project import TestCases
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from server.test_tracker.serializers.requirement import RequirementsSerializer





class TestCaseSerializer(ModelSerializer):
    """class TestCaseSerializer to serialize the test case obj"""
    requirement = SerializerMethodField()
    created = SerializerMethodField()
    assigned_user = SerializerMethodField()

    class Meta:
        model = TestCases
        exclude = (
            'verify_requirement', 'test_suite',
            'comments', 'passed', 'failed', 'skipped', 'run',
            'status', 'completed'
        )

    def get_requirement(self, obj):
        """Method to get the requirement obj"""
        return RequirementsSerializer(obj.verify_requirement).data
    
    def get_created(self, obj):
        return obj.created.date()
    
    def get_assigned_user(self, obj):
        return {"id": obj.assigned_user.id,"full_name":obj.assigned_user.full_name}


class GetSingleTestCaseSerializer(ModelSerializer):
    """class TestCaseSerializer to serialize the test case obj"""
    requirement = SerializerMethodField()

    class Meta:
        model = TestCases
        fields = (
            'title', 'description', 'test_steps', 'expected_result',
            'requirement', 'test_suite','comments', 'passed', 'failed',
            'skipped', 'run', 'status', 'completed'
        )

    def get_requirement(self, obj):
        """Method to get the requirement obj"""
        return RequirementsSerializer(obj.verify_requirement).data
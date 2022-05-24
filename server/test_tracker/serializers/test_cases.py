"""Everything related to TestCases"""


from server.test_tracker.models.project import TestCases
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from server.test_tracker.serializers.requirement import RequirementsSerializer





class TestCaseSerializer(ModelSerializer):
    """class TestCaseSerializer to serialize the test case obj"""
    requirement = SerializerMethodField()
    created = SerializerMethodField()
    modified = SerializerMethodField()
    last_saved = SerializerMethodField()

    class Meta:
        model = TestCases
        exclude = (
            'verify_requirement', 'test_suite',
            'comments', 'passed', 'failed', 'skipped', 'run', 'completed'
        )

    def get_requirement(self, obj):
        """Method to get the requirement obj"""
        return RequirementsSerializer(obj.verify_requirement).data
    
    def get_created(self, obj):
        """Method to get the created date"""
        return obj.created.date()
    
    def get_modified(self, obj):
        """Method to get the modified date"""
        return obj.modified.date()
    
    def get_last_saved(self, obj):
        """Method to get the last saved user"""
        data = {
            'id': obj.last_saved.id,
            "full_name" : obj.last_saved.full_name,
        }
        return data


class GetSingleTestCaseSerializer(ModelSerializer):
    """class TestCaseSerializer to serialize the test case obj"""
    requirement = SerializerMethodField()
    created = SerializerMethodField()
    modified = SerializerMethodField()
    last_saved = SerializerMethodField()

    class Meta:
        model = TestCases
        fields = (
            'title', 'description', 'test_steps', 'expected_result',
            'requirement', 'test_suite','comments', 'passed', 'failed',
            'skipped', 'run', 'completed', 'last_saved'
        )

    def get_requirement(self, obj):
        """Method to get the requirement obj"""
        return RequirementsSerializer(obj.verify_requirement).data

    def get_created(self, obj):
        """Method to get the created date"""
        return obj.created.date()
    
    def get_modified(self, obj):
        """Method to get the modified date"""
        return obj.modified.date()
    
    def get_last_saved(self, obj):
        """Method to get the last saved user"""
        data = {
            'id': obj.last_saved.id,
            "full_name" : obj.last_saved.full_name,
        }
        return data
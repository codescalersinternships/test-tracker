"""Everything related to TestCases"""


from test_tracker.models.project import TestCases
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from test_tracker.serializers.requirement import RequirementsSerializer


class TestCaseSerializer(ModelSerializer):
    """class TestCaseSerializer to serialize the test case obj"""

    requirement = SerializerMethodField()
    created = SerializerMethodField()
    modified = SerializerMethodField()
    last_saved = SerializerMethodField()
    testcase_title = SerializerMethodField()
    test_suite = SerializerMethodField()

    class Meta:
        model = TestCases
        exclude = (
            "verify_requirement",
            "comments",
            "passed",
            "failed",
            "skipped",
            "run",
            "completed",
        )

    def get_requirement(self, obj):
        """Method to get the requirement obj"""
        return (
            RequirementsSerializer(obj.verify_requirement).data
            if obj.verify_requirement
            else None
        )

    def get_created(self, obj):
        """Method to get the created date"""
        return obj.created.date()

    def get_modified(self, obj):
        """Method to get the modified date"""
        return obj.modified.date()

    def get_testcase_title(self, obj):
        """Method to get the testcase_title"""
        return obj.testcase_title

    def get_last_saved(self, obj):
        """Method to get the last saved user"""
        if obj.last_saved:
            data = {
                "id": obj.last_saved.id,
                "full_name": obj.last_saved.full_name,
            }
            return data

    def get_test_suite(self, obj):
        return obj.test_suite.title


class UpdateTestCaseAfterRunSerializer(ModelSerializer):
    """This class to update test case after run"""

    class Meta:
        model = TestCases
        fields = ("id", "passed", "failed", "skipped", "run", "completed", "comments")

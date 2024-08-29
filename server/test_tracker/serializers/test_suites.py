"""Everything related to TestSuites"""


from test_tracker.models.project import TestCases, TestSuites
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from test_tracker.serializers.test_cases import TestCaseSerializer


class TestSuitesSerializer(ModelSerializer):
    """class TestSuitesSerializer to serialize the test suite obj"""

    created = SerializerMethodField()
    modified = SerializerMethodField()
    number_of_test_cases = SerializerMethodField()

    class Meta:
        model = TestSuites
        exclude = ("project",)

    def get_created(self, obj):
        """Method to get the created date"""
        return obj.created.date()

    def get_modified(self, obj):
        """Method to get the modified date"""
        return obj.modified.date()

    def get_number_of_test_cases(self, obj):
        """Method to get the number of test cases"""
        return TestCases.objects.filter(test_suite=obj).count()


class TestSuitesDetailSerializer(ModelSerializer):
    """class TestSuitesSerializer to serialize the test suite obj"""

    created = SerializerMethodField()
    modified = SerializerMethodField()
    number_of_test_cases = SerializerMethodField()
    test_cases = SerializerMethodField()
    test_plan = SerializerMethodField()
    passed = SerializerMethodField()
    failed = SerializerMethodField()
    skipped = SerializerMethodField()
    not_run = SerializerMethodField()

    class Meta:
        model = TestSuites
        exclude = ("project",)

    def get_created(self, obj):
        """Method to get the created date"""
        return obj.created.date()

    def get_modified(self, obj):
        """Method to get the modified date"""
        return obj.modified.date()

    def get_number_of_test_cases(self, obj):
        """Method to get the number of test cases"""
        return TestCases.objects.filter(test_suite=obj).count()

    def get_test_plan(self, obj):
        """Method to get the test plan"""
        data = {
            "id": obj.test_plan.id,
            "title": obj.test_plan.title,
        }
        return data

    def get_test_cases(self, obj: TestSuites) -> int:
        """
        This method is used to get the total number of test cases
        """
        return TestCaseSerializer(
            obj.test_suite_test_cases.all().order_by("-created"), many=True
        ).data

    def get_passed(self, obj: TestSuites) -> int:
        """Return length of passed test cases"""
        return len(
            obj.test_suite_test_cases.filter(passed=True, failed=False, skipped=False)
        )

    def get_failed(self, obj: TestSuites) -> int:
        """Return length of passed test cases"""
        return len(
            obj.test_suite_test_cases.filter(failed=True, passed=False, skipped=False)
        )

    def get_skipped(self, obj: TestSuites) -> int:
        """Return length of passed test cases"""
        return len(
            obj.test_suite_test_cases.filter(failed=False, passed=False, skipped=True)
        )

    def get_not_run(self, obj: TestSuites) -> int:
        """Return length of passed test cases"""
        return len(
            obj.test_suite_test_cases.filter(
                run=False,
                failed=False,
                passed=False,
                skipped=False,
            )
        )

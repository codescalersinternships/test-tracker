"""Everything related to TestRuns"""
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from server.test_tracker.models.dashboard import People

from server.test_tracker.models.project import TestCases, TestRun, TestSuites



class TestRunsSerializer(ModelSerializer):
    """Test run serializer class"""
    user = SerializerMethodField()
    total_test_cases = SerializerMethodField()
    passed = SerializerMethodField()
    failed = SerializerMethodField()
    skipped = SerializerMethodField()
    not_run = SerializerMethodField()
    completed = SerializerMethodField()

    class Meta:
        model = TestRun
        fields = [
            'id','title','test_suites','total_test_cases','user',
            'passed', 'failed','skipped', 'not_run', 'completed'
        ]

    def test_cases(self, test_suites: TestSuites) -> TestCases:
        """Service method to return all of test cases based on test suite"""
        return TestCases.objects.filter(test_suite__in=test_suites.all())

    def get_total_test_cases(self, obj: TestRun) -> int:
        """
        This method is used to get the total number of test cases
        """
        return len(self.test_cases(obj.test_suites))

    def get_passed(self, obj: TestRun) -> int:
        """Return length of passed test cases"""
        return len(self.test_cases(obj.test_suites).filter(
                passed=True
            )
        )

    def get_failed(self, obj: TestRun) -> int:
        """Return length of passed test cases"""
        return len(self.test_cases(obj.test_suites).filter(
                failed=True
            )
        )

    def get_skipped(self, obj: TestRun) -> int:
        """Return length of passed test cases"""
        return len(self.test_cases(obj.test_suites).filter(
                skipped=True
            )
        )

    def get_not_run(self, obj: TestRun) -> int:
        """Return length of passed test cases"""
        return len(self.test_cases(obj.test_suites).filter(
                run=True
            )
        )

    def get_completed(self, obj: TestRun) -> int:
        """Return length of passed test cases"""
        if  self.get_not_run(obj) == 0 and len(self.test_cases(obj.test_suites))== 0:
            return f"0.00 %"
        return f"{self.get_not_run(obj) / len(self.test_cases(obj.test_suites)) * 100} %"

    def get_user(self, obj: TestRun) -> People:
        """Return assigned user"""
        return obj.assigned_user.full_name
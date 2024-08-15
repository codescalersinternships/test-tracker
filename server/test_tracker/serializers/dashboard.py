from rest_framework.serializers import ModelSerializer, SerializerMethodField

from test_tracker.models.dashboard import Project
from test_tracker.models.users import User
from test_tracker.serializers.project import TestPlanSerializer
from test_tracker.serializers.requirement import RequirementDocsSerializer
from test_tracker.serializers.test_run import TestRunsSerializer
from test_tracker.serializers.test_suites import TestSuitesSerializer
from test_tracker.services.dashboard import my_projects
from test_tracker.services.member import get_member_by_id
from test_tracker.models.project import (
    TEST_RUN_STATUS_CHOICES,
    RequirementDocs,
    TestPlan,
    TestRun,
    TestSuites,
)


class GetRequestUserSerializers(ModelSerializer):
    permission = SerializerMethodField()
    projects = SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "full_name",
            "last_name",
            "email",
            "phone",
            "permission",
            "projects",
        ]

    def get_permission(self, obj):
        if get_member_by_id(obj.id) is not None:
            return "member"
        return "admin"

    def get_projects(self, obj):
        return len(my_projects(obj))


class ProjectsSerializer(ModelSerializer):
    """class ProjectsSerializer to serialize the project obj"""

    user = SerializerMethodField()
    teams = SerializerMethodField()
    modified = SerializerMethodField()
    created = SerializerMethodField()
    activity = SerializerMethodField()
    total_test_plan = SerializerMethodField()
    total_requirements_docs = SerializerMethodField()
    total_suites = SerializerMethodField()
    total_test_runs = SerializerMethodField()
    incomplete_test_runs_assigned_to_you = SerializerMethodField()
    people_with_the_most_incomplete_test_runs = SerializerMethodField()

    class Meta:
        model = Project
        exclude = ("members", "TC_Title", "REQ_Title")

    def get_created(self, obj):
        """Return created date"""
        return obj.created.date()

    def get_user(self, obj):
        """Return created date"""
        return obj.user.full_name

    def get_modified(self, obj):
        """Return created date"""
        return obj.modified.date()

    def get_teams(self, obj):
        """Return created date"""
        from test_tracker.serializers.member import MemberSerializers

        if self.context.get("profile_view"):
            return MemberSerializers(
                obj.members.all().exclude(id=self.context["this_user"].id), many=True
            ).data
        return MemberSerializers(obj.members.all(), many=True).data

    def get_activity(self, obj):
        """Return all project activity"""
        result = []
        for action, values in obj.activity.items():
            result.append(values)
        result = result[::-1]
        return result[:11]

    def get_total_test_plan(self, obj):
        """Return all of test plan for its project"""
        test_plans = TestPlan.objects.filter(project=obj)
        return TestPlanSerializer(test_plans, many=True).data

    def get_total_requirements_docs(self, obj):
        """Return project requirement"""
        requirements = RequirementDocs.objects.filter(project=obj)
        return RequirementDocsSerializer(requirements, many=True).data

    def get_total_suites(self, obj):
        """Return project suites"""
        test_suites = TestSuites.objects.filter(project=obj)
        return TestSuitesSerializer(test_suites, many=True).data

    def get_total_test_runs(self, obj):
        """Return project runs"""
        test_suites = TestSuites.objects.filter(project=obj).values_list(
            "id", flat=True
        )
        test_runs = TestRun.objects.filter(test_suites__id__in=test_suites)
        return TestRunsSerializer(test_runs, many=True).data

    def get_not_started_test_runs(self, obj):
        """Return project not started runs"""
        test_suites = TestSuites.objects.filter(project=obj).values_list(
            "id", flat=True
        )
        test_cases = TestRun.objects.filter(
            test_suites__id__in=test_suites, status=TEST_RUN_STATUS_CHOICES.NOT_STARTED
        )
        return TestRunsSerializer(test_cases, many=True).data

    def get_in_progress_test_runs(self, obj):
        """Return project in progress"""
        test_suites = TestSuites.objects.filter(project=obj).values_list(
            "id", flat=True
        )
        test_cases = TestRun.objects.filter(
            test_suite__id__in=test_suites, status=TEST_RUN_STATUS_CHOICES.IN_PROGRESS
        )
        return TestRunsSerializer(test_cases, many=True).data

    def get_incomplete_test_runs_assigned_to_you(self, obj):
        """Get total complected runs based on user"""
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        if user:
            test_suites = TestSuites.objects.filter(project=obj)
            test_runs = (
                TestRun.objects.filter(
                    test_suites__in=test_suites,
                    status=TEST_RUN_STATUS_CHOICES.NOT_STARTED,
                    assigned_user=user,
                )
                .order_by("-created")
                .first()
            )
            if test_runs:
                return TestRunsSerializer(test_runs).data
            return None
        return

    def get_people_with_the_most_incomplete_test_runs(self, obj):
        """Get total comleated runs based on user"""
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        if user:
            test_suites = TestSuites.objects.filter(project=obj)
            test_runs = (
                TestRun.objects.filter(
                    test_suites__in=test_suites,
                    status=TEST_RUN_STATUS_CHOICES.NOT_STARTED,
                )
                .exclude(assigned_user=None)
                .order_by("-created")
            )
            return TestRunsSerializer(test_runs[:5], many=True).data
        return

from rest_framework.serializers import ModelSerializer, SerializerMethodField
from server.test_tracker.models.dashboard import Member, Project
from server.test_tracker.models.project import TEST_RUN_STATUS_CHOICES, ProjectRequirement, TestCases, TestPlan, TestRun, TestSuites
from server.test_tracker.models.users import User
from server.test_tracker.serializers.project import TestPlanSerializer
from server.test_tracker.serializers.requirement import ProjectRequirementSerializer
from server.test_tracker.serializers.test_cases import TestCaseSerializer
from server.test_tracker.serializers.test_run import TestRunsSerializer
from server.test_tracker.serializers.test_suites import TestSuitesSerializer


class ProjectsSerializer(ModelSerializer):
    """class ProjectsSerializer to serialize the project obj"""
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
        exclude = ('user', 'members',)
    
    def get_created(self, obj):
        """Return created date"""
        return obj.created.date()

    def get_activity(self, obj):
        """Return all project activity"""
        return obj.activity

    def get_total_test_plan(self, obj):
        """Return all of test plan for its project"""
        test_plans = TestPlan.objects.filter(project = obj)
        return TestPlanSerializer(test_plans, many=True).data
    
    def get_total_requirements_docs(self, obj):
        """Return project requirement"""
        requirements = ProjectRequirement.objects.filter(project = obj)
        return ProjectRequirementSerializer(requirements, many=True).data

    def get_total_suites(self, obj):
        """Return project suites"""
        test_suites = TestSuites.objects.filter(project = obj)
        return TestSuitesSerializer(test_suites, many=True).data

    def get_total_test_runs(self, obj):
        """Return project runs"""
        test_suites = TestSuites.objects.filter(project = obj).values_list("id", flat=True)
        test_runs = TestRun.objects.filter(test_suites__id__in = test_suites)
        return TestRunsSerializer(test_runs, many=True).data

    def get_not_started_test_runs(self, obj):
        """Return project not started runs"""
        test_suites = TestSuites.objects.filter(
            project = obj
        ).values_list("id", flat=True)
        test_cases = TestCases.objects.filter(test_suite__id__in = test_suites, status = TEST_RUN_STATUS_CHOICES.NOT_STARTED)
        return TestCaseSerializer(test_cases, many=True).data

    def get_in_progress_test_runs(self, obj):
        """Return project in progress"""
        test_suites = TestSuites.objects.filter(
            project = obj
        ).values_list("id", flat=True)
        test_cases = TestCases.objects.filter(test_suite__id__in = test_suites, status = TEST_RUN_STATUS_CHOICES.IN_PROGRESS)
        return TestCaseSerializer(test_cases, many=True).data
    
    def get_incomplete_test_runs_assigned_to_you(self, obj):
        """Get total comleated runs based on user"""
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        if user:
            test_suites = TestSuites.objects.filter(
            project = obj
            ).values_list("id", flat=True)
            test_cases = TestCases.objects.filter(
                test_suite__id__in = test_suites, completed=False,
                assigned_user = user
                ).order_by('-created')
            return TestCaseSerializer(test_cases[:5], many=True).data
        return

    def get_people_with_the_most_incomplete_test_runs(self, obj):
        """Get total comleated runs based on user"""
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        if user:
            test_suites = TestSuites.objects.filter(
            project = obj
            ).values_list("id", flat=True)
            test_cases = TestCases.objects.filter(
                test_suite__id__in = test_suites, completed=False,
            ).order_by('-created')
            return TestCaseSerializer(test_cases[:5], many=True).data
        return



class MemberSerializer(ModelSerializer):
    """class MemberSerializer to serialize the Member obj"""
    class Meta:
        model = Member
        fields = ('first_name', 'last_name', 'email','permission')

class GetMemberSerializer(ModelSerializer):
    """class GetMemberSerializer to serialize the Member obj"""
    created = SerializerMethodField()
    last_project_working_on = SerializerMethodField()
    phone = SerializerMethodField()

    class Meta:
        model = Member
        fields = ('id', 'permission','full_name', 'email', 'phone', 'created', 'last_project_working_on')

    def get_created(self, obj):
        """Return created date"""
        return obj.created.date()

    def get_phone(self, obj):
        """Return created date"""
        return '' if obj.phone is None else obj.phone

    def get_last_project_working_on(self, obj):
        """Get last project working on for member"""
        project = Project.objects.filter(members__id = obj.id).last()
        return ProjectsSerializer(project).data

class ProfileSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id','first_name','last_name', 'email',
            'phone'
        ]
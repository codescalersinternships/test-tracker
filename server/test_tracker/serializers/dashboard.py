from rest_framework.serializers import ModelSerializer, SerializerMethodField
from server.test_tracker.models.dashboard import Member, Project
from server.test_tracker.models.project import TEST_RUN_STATUS_CHOICES, ProjectRequirement, TestCases, TestPlan, TestRun, TestSuites
from server.test_tracker.models.users import User
from server.test_tracker.serializers.project import TestPlanSerializer
from server.test_tracker.serializers.requirement import ProjectRequirementSerializer
from server.test_tracker.serializers.test_cases import TestCaseSerializer
from server.test_tracker.serializers.test_run import TestRunsSerializer
from server.test_tracker.serializers.test_suites import TestSuitesSerializer



class ProfileSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','full_name','email','phone']


class ProjectsSerializer(ModelSerializer):
    """class ProjectsSerializer to serialize the project obj"""
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
        exclude = ('user', 'members',)
    
    def get_created(self, obj):
        """Return created date"""
        return obj.created.date()

    def get_modified(self, obj):
        """Return created date"""
        return obj.modified.date()

    def get_teams(self, obj):
        """Return created date"""
        if self.context.get('profile_view'):
            return ProfileSerializers(
                obj.members.all().exclude(
                    id = self.context['this_user'].id
                ), many=True
            ).data
        return ProfileSerializers(obj.members.all(), many=True).data

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

class GetMemberSerializer(ModelSerializer):
    """class GetGetMemberSerializer to serialize the Member obj"""
    created = SerializerMethodField()
    last_project_working_on = SerializerMethodField()
    total_project_worked_on = SerializerMethodField()
    last_tests_assigned = SerializerMethodField()
    phone = SerializerMethodField()

    class Meta:
        model = Member
        fields = (
            'id', 'permission','full_name', 'email', 'phone', 'created', 
            'last_project_working_on', 'total_project_worked_on','last_tests_assigned'
        )

    def get_created(self, obj):
        """Return created date"""
        return obj.created.date()

    def get_phone(self, obj):
        """Return created date"""
        return '' if obj.phone is None else obj.phone

    def get_last_project_working_on(self, obj):
        """Get last project working on for member"""
        project = Project.objects.filter(members__id = obj.id).order_by('-created').first()
        return ProjectsSerializer(project, context=self.context).data

    def get_total_project_worked_on(self, obj):
        """Get total projects worked on for member"""
        project = Project.objects.filter(members__id = obj.id).count()
        return project

    def get_last_tests_assigned(self, obj):
        """Get total projects worked on for member"""
        project = Project.objects.filter(members__id__in = [obj.id])
        test_suites = TestSuites.objects.filter(project__id__in = project)
        test_cases = TestCases.objects.filter(
            test_suite__in = test_suites, assigned_user__id__in = [obj.id]
        ).order_by('-created').first()
        return TestCaseSerializer(test_cases).data

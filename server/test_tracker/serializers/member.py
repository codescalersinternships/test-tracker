"""Everything related to Member"""
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from test_tracker.models.dashboard import Member, Project
from test_tracker.models.project import TestRun, TestSuites
from test_tracker.serializers.test_run import TestRunsSerializer


class MemberSetPasswordSerializer(ModelSerializer):
    """Class Member to set password for member on Member table"""

    class Meta:
        model = Member
        fields = ["password"]


class ProjectTeamSerializer(ModelSerializer):
    """Class Member to get project teams"""

    created = SerializerMethodField()

    class Meta:
        model = Member
        fields = ["id", "first_name", "last_name", "full_name", "created"]

    def get_created(self, obj):
        """Return created date"""
        return obj.created.date()


class MemberSerializers(ModelSerializer):
    created = SerializerMethodField()
    last_project_working_on = SerializerMethodField()
    total_project_worked_on = SerializerMethodField()
    last_tests_assigned = SerializerMethodField()
    phone = SerializerMethodField()
    invited = SerializerMethodField()
    accepted = SerializerMethodField()

    class Meta:
        model = Member
        fields = (
            "id",
            "permission",
            "full_name",
            "email",
            "phone",
            "created",
            "first_name",
            "last_name",
            "last_project_working_on",
            "total_project_worked_on",
            "last_tests_assigned",
            "accepted",
            "invited",
        )

    def get_created(self, obj):
        """Return created date"""
        return obj.created.date()

    def get_invited(self, obj):
        return obj.invited

    def get_accepted(self, obj):
        return obj.accepted

    def get_phone(self, obj):
        """Return created date"""
        return "" if obj.phone is None else obj.phone

    def get_last_project_working_on(self, obj):
        """Get last project working on for member"""
        project = (
            Project.objects.filter(members__in=[obj.id]).order_by("-created").first()
        )
        if project:
            return {
                "title": project.title,
                "id": project.id,
                "teams": ProjectTeamSerializer(project.members.all(), many=True).data,
                "created": project.created.date(),
                "modified": project.modified.date(),
            }
        return None

    def get_total_project_worked_on(self, obj):
        """Get total projects worked on for member"""
        return Project.objects.filter(members__id__in=[obj.id]).count()

    def get_first_name(self, obj):
        """Get first name of member"""
        return obj.first_name.upper()

    def get_last_name(self, obj):
        """Get last name of member"""
        return obj.last_name.upper()

    def get_last_tests_assigned(self, obj):
        """Get total projects worked on for member"""
        project = Project.objects.filter(members__id__in=[obj.id])
        test_suites = TestSuites.objects.filter(project__id__in=project)
        test_run = (
            TestRun.objects.filter(test_suites__in=test_suites, assigned_user=obj)
            .order_by("-created")
            .first()
        )
        if test_run:
            return TestRunsSerializer(test_run).data
        return None

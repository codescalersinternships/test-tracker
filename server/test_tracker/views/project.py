"""Everything related to the project."""
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from server.test_tracker.api.response import CustomResponse


from server.test_tracker.models.project import PLAN_CHOICES, TestPlan
from server.test_tracker.serializers.project import ActivitySerializer, AddOrUpdateTempsSerializer, TestPlanDetailSerializer, TestPlanSerializer, UpdateTestPlanSerializer
from server.test_tracker.services.project import update_activity
from server.test_tracker.utils.testplan_handle import TestPlanHandeling
from server.test_tracker.utils.testplan_temp import TestPlanTemp
from server.test_tracker.services.dashboard import get_plans_based_on_project, get_project_by_id
import datetime


class TestPlansAPIView(GenericAPIView):
    """Create a test plan."""
    serializer_class = TestPlanSerializer
    def post(self, request:Request, project_id: str) -> Response:
        """
            Use this endpoint to create a new test plan
            You can set temps of null to create a test plan with default temps
        """
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            type = serializer.validated_data.get('type')
            project = get_project_by_id(project_id)
            if project is None:
                return CustomResponse.not_found(message = "Project not found")
            if type == PLAN_CHOICES.TEMPLATE.value:
                temps = TestPlanTemp.create_temps()
                serializer.save(project = project, temps = temps)
            serializer.save(project = project)
            update_activity(
                datetime.datetime.now(), request.user, project,
                "Create", "Test Plan", serializer.data.get('name')
            )
            return CustomResponse.success(
                data=serializer.validated_data,
                message="Test plan created successfully"
            )
        return CustomResponse.bad_request(
            data=serializer.errors,
            message="Test plan not created",
            status_code=201
        )

    def get(self, request: Request, project_id: str) -> Response:
        """Method get to get all of test plans based on the project"""
        project = get_project_by_id(project_id)
        if project is None:
            return CustomResponse.not_found(message = "Project not found")
        plans = get_plans_based_on_project(project)
        serializer = TestPlanSerializer(plans, many=True)
        return CustomResponse.success(
            message = "Success plans found.",
            data = serializer.data
        )


class TestPlansDetailAPIView(GenericAPIView):
    """This class for [GET, UPDATE, DELETE] test plans methods"""
    serializer_class = TestPlanDetailSerializer


    def get(self, request: Request, project_id:str, test_plan_id: str) -> Response:
        """Get a test plan from the specified project"""
        test_plan = TestPlanHandeling.valid(project_id, test_plan_id)
        if isinstance(test_plan, TestPlan):
            return CustomResponse.success(
                message="Test plan found successfully",
                data=TestPlanDetailSerializer(test_plan).data
            )
        return test_plan
    

    def delete(self, request: Request, project_id:str, test_plan_id: str) -> Response:
        """Delete a test plan from the specified project"""
        test_plan = TestPlanHandeling.valid(project_id, test_plan_id)
        if isinstance(test_plan, TestPlan):
            update_activity(
                datetime.datetime.now(), request.user, get_project_by_id(project_id),
                "Delete", "Test Plan", test_plan.name
            )
            test_plan.delete()
            return CustomResponse.success(
                message="DELETED",
                status_code=204
            )
        return test_plan

class UpdateTestPlanAPIView(GenericAPIView):
    serializer_class = UpdateTestPlanSerializer
    def put(self, request: Request, project_id:str, test_plan_id:str) -> Response:
        """Update test plan title"""
        test_plan = TestPlanHandeling.valid(project_id, test_plan_id)
        if isinstance(test_plan, TestPlan):
            serializer = self.get_serializer(test_plan, data = request.data)
            if serializer.is_valid():
                serializer.save()
                update_activity(
                    datetime.datetime.now(), request.user, get_project_by_id(project_id),
                    "Update", "Test Plan", test_plan.name
                )
                return CustomResponse.success(
                    message="Test plan Updated",
                    status_code=200
                )
            return CustomResponse.bad_request(
                errors=serializer.errors,
                message="Test plan not updated",
            )
        return test_plan

class AddOrUpdateTempsAPIView(GenericAPIView):
    """Add or update content area to test plan"""
    serializer_class = AddOrUpdateTempsSerializer

    def post (self, request: Request, project_id:str, test_plan_id: str) -> Response:
        """Add custom content area to test plan"""
        test_plan = TestPlanHandeling.valid(project_id, test_plan_id)
        if isinstance(test_plan, TestPlan):
            serializer = self.get_serializer(data = request.data)
            if serializer.is_valid():
                title = serializer.validated_data.get('title')
                content = serializer.validated_data.get('content')
                test_plan.add_or_update_temps(title, content)
                update_activity(
                    datetime.datetime.now(), request.user, get_project_by_id(project_id),
                    "Create", "Test Plan Template", test_plan.name
                )
                return CustomResponse.success(
                    message="Successfully added content area to test plan",
                    data = serializer.data,
                    status_code=201
                )
            return CustomResponse.bad_request(
                error=serializer.errors,
                message="Content area not added",
            )
        return test_plan


class DeleteContentAreaAPIView(GenericAPIView):
    """Delete content area from test plan"""
    def delete(self, request: Request, project_id:str, test_plan_id: str, title:str) -> Response:
        test_plan = TestPlanHandeling.valid(project_id, test_plan_id)
        if isinstance(test_plan, TestPlan):
            deleted = test_plan.delete_temp(title)
            if deleted:
                update_activity(
                    datetime.datetime.now(), request.user, get_project_by_id(project_id),
                    "Create", "Test Plan Template", test_plan.name
                )
                return CustomResponse.success(
                    message="DELETED",
                    status_code=204
                )
            return CustomResponse.not_found(
                message = 'There are no content area with this title'
            )
        return test_plan

class ProjectActivityAPIView(GenericAPIView):
    """Get all project activity"""
    def get(self, request: Request, project_id: str) -> Response:
        project = get_project_by_id(project_id)
        if project is None:
            return CustomResponse.not_found(message = "Project not found")
        return CustomResponse.success(
            message="Success plans found.",
            data = ActivitySerializer(project).data
        )
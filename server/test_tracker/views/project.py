"""Everything related to the project."""
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from server.test_tracker.api.response import CustomResponse


from server.test_tracker.models.project import PLAN_CHOICES
from server.test_tracker.serializers.project import TestPlanDetailSerializer, TestPlanSerializer
from server.test_tracker.services.project import get_test_plan_by_id
from server.test_tracker.utils.testplan_temp import TestPlanTemp
from server.test_tracker.services.dashboard import get_plans_based_on_project, get_project_by_id


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
        project = get_project_by_id(project_id)
        test_plan = get_test_plan_by_id(test_plan_id)
        if project is None:
            return CustomResponse.not_found(
                    message="There are no test plan with this id"
                )
        if test_plan is None:
            return CustomResponse.not_found(
                message="There are no test plan with this id"
            )
        if test_plan.project != project:
            return CustomResponse.bad_request(
                message="You don't have permission to access this test plan"
            )
        return CustomResponse.success(
            message="Test plan found successfully",
            data=TestPlanDetailSerializer(test_plan).data
        )

    def delete(self, request: Request, project_id:str, test_plan_id: str) -> Response:
        project = get_project_by_id(project_id)
        test_plan = get_test_plan_by_id(test_plan_id)
        if project is None:
            return CustomResponse.not_found(
                    message="There are no test plan with this id"
                )
        if test_plan is None:
            return CustomResponse.not_found(
                message="There are no test plan with this id"
            )
        if test_plan.project != project:
            return CustomResponse.bad_request(
                message="You don't have permission to access this test plan"
            )
        test_plan.delete()
        return CustomResponse.success(
            message="DELETED",
            status_code=204
        )
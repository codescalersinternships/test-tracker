"""Everything related to the project."""
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from server.test_tracker.api.response import CustomResponse


from server.test_tracker.models.project import PLAN_CHOICES
from server.test_tracker.serializers.project import TestPlanSerializer
from server.test_tracker.utils.testplan_temp import TestPlanTemp
from server.test_tracker.services.dashboard import get_project_by_id


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
            message="Test plan not created"
        )


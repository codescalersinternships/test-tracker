"""Everything related to requeriments"""
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from server.test_tracker.api.response import CustomResponse
from server.test_tracker.serializers.requirement import ProjectRequirementSerializer
from server.test_tracker.services.dashboard import get_project_by_id
from server.test_tracker.services.requirement import get_requirement_by_id, get_requirements_by_project




class ProjectRequirementAPIView(GenericAPIView):
    """class project requirement view"""
    serializer_class = ProjectRequirementSerializer

    def post(self, request: Request, project_id: str) -> Response:
        """post a new requirement"""
        project = get_project_by_id(project_id)
        if project is not None:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(project=project)
                return CustomResponse.success(
                    data=serializer.data,
                    message="Requirement created successfully",
                    status_code=201
                )
            return CustomResponse.bad_request(
                message="Requirement creation failed",
                error=serializer.errors
            )
        return CustomResponse.not_found(message="Project not found")

class GetProjectRequirementAPIView(GenericAPIView):
    """class project requirement view"""
    serializer_class = ProjectRequirementSerializer

    def get(self, request: Request, project_id: str) -> Response:
        """get all requirements for a project"""
        project = get_project_by_id(project_id)
        if project is None:
            return CustomResponse.not_found(message = "Project not found")
        requirements = get_requirements_by_project(project)
        serializer = self.get_serializer(requirements, many=True)
        return CustomResponse.success(
            data=serializer.data,
            message="All requirements for project",
            status_code=200
        )

class UpdateProjectRequirementAPIView(GenericAPIView):
    """class project requirement view"""
    serializer_class = ProjectRequirementSerializer

    def put(self, request: Request, project_id: str, requirement_id: str) -> Response:
        """update a requirement"""
        project = get_project_by_id(project_id)
        requirement = get_requirement_by_id(int(requirement_id))
        if project is None:
            return CustomResponse.not_found(message = "Project not found")
        if requirement is None:
            return CustomResponse.not_found(message = "Requirement not found")

        serializer = self.get_serializer(requirement, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                data=serializer.data,
                message="Requirement updated successfully",
                status_code=201
            )
        return CustomResponse.bad_request(
            message="Requirement update failed",
            error=serializer.errors
        )
    
    def delete(self, request: Request, project_id: str, requirement_id: str) -> Response:
        """delete a requirement"""
        project = get_project_by_id(project_id)
        requirement = get_requirement_by_id(int(requirement_id))
        if project is None:
            return CustomResponse.not_found(message = "Project not found")
        if requirement is None:
            return CustomResponse.not_found(message = "Requirement not found")

        requirement.delete()
        return CustomResponse.success(
            data={},
            message="Requirement deleted successfully",
            status_code=204
        )
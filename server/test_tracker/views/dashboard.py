"""Everything related to dashboard."""
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from server.test_tracker.api.permission import UserIsAuthenticated
from server.test_tracker.api.response import CustomResponse
from server.test_tracker.serializers.dashboard import ProjectsSerializer
from server.test_tracker.services.dashboard import find_project_name_based_on_user, get_project_by_id
from server.test_tracker.utils.validations import Validator



class ProjectsAPIView(GenericAPIView):
    """
        Class ProjectsAPIView have a create method which creates a new project
    """
    serializer_class = ProjectsSerializer
    permission_classes = (UserIsAuthenticated,)

    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            project_name: str = serializer.validated_data.get('name')
            validate_name: str = Validator().validate_string(project_name)
            if validate_name:
                no_project = find_project_name_based_on_user(request.user, project_name)
                if no_project:
                    serializer.save(user = request.user)
                    return CustomResponse.success(
                        data = serializer.data, 
                        message = "Project created successfully", 
                        status_code = 201
                    )
                return CustomResponse.bad_request(
                    message = "Project already exists",
                    status_code = 400
                )
            return CustomResponse.bad_request(
                error = f"Name '{project_name}' is not a valid name",
                message = "Project creation failed",
            )
        return CustomResponse.bad_request(
            error = serializer.errors,
            message = "Project creation failed"
        )
class ProjectsDetailAPIView(GenericAPIView):
    """
        Class ProjectsAPIView have all the functionality based on the project
        Methods [GET, POST, PUT, DELETE]
    """
    serializer_class = ProjectsSerializer
    permission_classes = (UserIsAuthenticated,)

    def get(self, request: Request, project_id: str) -> Response:
        """Return a single project based on the given project id"""
        project = get_project_by_id(project_id)
        if project is not None:
            return CustomResponse.success(
                data=ProjectsSerializer(project).data,
                message="Project found successfully",
            )
        return CustomResponse.not_found(
            message="Project not found",
        )

    def put(self, request: Request, project_id: int) -> Response:
        """Put some data into the project"""
        project = get_project_by_id(project_id)
        if project is not None:
            serializer = self.get_serializer(project, data=request.data)
            if serializer.is_valid():
                project_name: str = serializer.validated_data.get('name')
                validate_name: str = Validator().validate_string(project_name)
                if validate_name:
                    no_project = find_project_name_based_on_user(request.user, project_name)
                    if no_project:
                        serializer.save(user = request.user)
                        return CustomResponse.success(
                            data=serializer.data,
                            message="Project updated successfully",
                        )
                    return CustomResponse.bad_request(
                        message = "Project already exists",
                        status_code = 400
                    )
                return CustomResponse.bad_request(
                    error = f"Name '{project_name}' is not a valid name",
                    message = "Project creation failed",
                )
            return CustomResponse.bad_request(
                error=serializer.errors,
                message="Project update failed",
            )
        return CustomResponse.not_found(
            message="Project not found",
        )

    def delete(self, request: Request, project_id: int) -> Response:
        project = get_project_by_id(project_id)
        if project is not None :
            project.delete()
            return CustomResponse.success(
                message="Project deleted successfully",
                status_code=204
            )
        return CustomResponse.not_found(
            message="Project not found",
        )
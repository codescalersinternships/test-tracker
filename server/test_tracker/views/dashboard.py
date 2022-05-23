"""Everything related to dashboard."""
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from server.test_tracker.api.permission import UserIsAuthenticated
from server.test_tracker.api.response import CustomResponse
from server.test_tracker.services.dashboard import *
from server.test_tracker.services.member import get_member_by_email
from server.test_tracker.services.users import get_user_by_id
from server.test_tracker.utils.send_mail import send_email
from server.test_tracker.utils.validations import Validator
from server.test_tracker.serializers.dashboard import *
from server.test_tracker.serializers.member import MemberSerializers


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
                        status_code = 203
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
    
    def get(self, request: Request) -> Response:
        """Get all projects based on creator, Members users"""
        projects = get_projects_by_user(request.user)
        serializer = ProjectsSerializer(projects, many=True)
        return CustomResponse.success(
            data = serializer.data,
            message = "Projects retrieved successfully",
            status_code = 200
        )

class MemberAPIView(GenericAPIView):
    """
        Class MemberAPIView have all the functionality based on the user
    """
    serializer_class = MemberSerializers
    permission_classes = (UserIsAuthenticated,)

    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email: str = serializer.validated_data.get('email')
            if not get_member_by_email(email):
                member = serializer.save(host_user=request.user, invited = True)
                send_email(
                    member.first_name, request.user, member.email, 
                    redirect_link=f"http://localhost:8080/auth/register/?signature={member.signature}"
                )
                return CustomResponse.success(
                    data=serializer.data,
                    message="Member added successfully",
                )
            return CustomResponse.bad_request(
                message="Member already exists",
                status_code=400
            )
        return CustomResponse.bad_request(
            error=serializer.errors,
            message="Member creation failed",
        )

class UpdateProfileAPIView(GenericAPIView):
    """This class to update profile info"""
    serializer_class = MemberSerializers
    permission_classes = (UserIsAuthenticated,)

    def put(self, request: Request) -> Response:
        user = get_user_by_id(request.user.id)
        serializer = self.get_serializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                data=serializer.data,
                message="Profile updated successfully",
                status_code=203
            )
        return CustomResponse.bad_request(
            error=serializer.errors,
            message="Profile update failed",
        )

class GetProfileAPIView(GenericAPIView):
    """This class to update profile info"""
    serializer_class = MemberSerializers
    permission_classes = (UserIsAuthenticated,)

    def get(self, request: Request, user_id:str) -> Response:
        """Returns user profile"""
        user = get_user_by_id(user_id)
        if user is not None:
            return CustomResponse.success(
                data=MemberSerializers(user).data,
                message="Profile found successfully",
            )
        return CustomResponse.not_found(
            message="Profile not found",
        )

class MyProjectsAPIView(APIView):
    """This class to get total projects"""
    permission_classes = (UserIsAuthenticated,)

    def get(self, request: Request) -> Response:
        """Returns total projects"""
        total_projects = my_projects(request.user)
        return CustomResponse.success(
            data=total_projects,
            message="Total projects found successfully",
        )

class GetRequestUserAPIView(GenericAPIView):
    """Returns user information"""
    permission_classes = (UserIsAuthenticated,)
    serializer_class = GetRequestUserSerializers

    def get(self, request:Request) -> Response:
        """Returns request user information"""
        user = request.user
        return CustomResponse.success(
            message="Success",
            data=self.get_serializer(user).data
        )
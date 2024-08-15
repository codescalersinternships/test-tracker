"""Everything related to dashboard."""
import datetime
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from test_tracker.api.permission import UserIsAuthenticated
from test_tracker.api.response import CustomResponse
from test_tracker.serializers.dashboard import (
    GetRequestUserSerializers,
    ProjectsSerializer,
)
from test_tracker.services.dashboard import (
    get_projects_by_user,
    my_projects,
    user_has_same_project_title,
)
from test_tracker.services.member import get_member_by_email
from test_tracker.services.project import update_activity
from test_tracker.services.users import get_user_by_id
from test_tracker.utils.send_mail import send_email
from test_tracker.utils.validations import Validator
from test_tracker.serializers.member import MemberSerializers


class ProjectsAPIView(GenericAPIView):
    """
    Class ProjectsAPIView has a post method which creates an new project
    """

    serializer_class = ProjectsSerializer
    permission_classes = (UserIsAuthenticated,)

    def post(self, request: Request) -> Response:
        """Create a new project"""
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return CustomResponse.bad_request(
                error=serializer.errors,
                message="Project update failed, please make sure that you entered a valid data",
            )

        project_title: str = serializer.validated_data.get("title")
        validate_name: str = Validator().validate_string(project_title)
        if not validate_name:
            return CustomResponse.bad_request(
                message=f"Name '{project_title}' is not a valid name, Please choose a valid project name.",
            )

        same_title = user_has_same_project_title(request.user, project_title)
        if same_title:
            return CustomResponse.bad_request(
                message="Please choose a project name that does not exist in your projects.",
                status_code=400,
            )
        project = serializer.save(user=request.user)
        update_activity(
            datetime.datetime.now(),
            request.user,
            project,
            "Create",
            "Project",
            project.title,
        )
        return CustomResponse.success(
            data=serializer.data,
            message="Project Created successfully",
            status_code=200,
        )

    def get(self, request: Request) -> Response:
        """Get all projects based on creator, Members users"""
        projects = get_projects_by_user(request.user).order_by("-created")
        serializer = ProjectsSerializer(projects, many=True)
        return CustomResponse.success(
            data=serializer.data,
            message="Projects retrieved successfully",
            status_code=200,
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
            email: str = serializer.validated_data.get("email")
            if not get_member_by_email(email):
                member = serializer.save(host_user=request.user, invited=True)
                send_email(
                    member.first_name,
                    request.user,
                    member.email,
                    redirect_link=f"http://localhost:8080/auth/register/?signature={member.signature}",
                )
                return CustomResponse.success(
                    data=serializer.data,
                    message="Member added successfully",
                )
            return CustomResponse.bad_request(
                message="Member already exists", status_code=400
            )
        return CustomResponse.bad_request(
            error=serializer.errors,
            message="Member creation failed",
        )


class GetProfileAPIView(GenericAPIView):
    """This class to update profile info"""

    serializer_class = MemberSerializers
    permission_classes = (UserIsAuthenticated,)

    def get(self, request: Request, user_id: str) -> Response:
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

    def get(self, request: Request) -> Response:
        """Returns request user information"""
        user = request.user
        return CustomResponse.success(
            message="Success", data=self.get_serializer(user).data
        )

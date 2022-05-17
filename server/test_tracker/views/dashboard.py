"""Everything related to dashboard."""
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from server.test_tracker.api.permission import UserIsAuthenticated
from server.test_tracker.api.response import CustomResponse
from server.test_tracker.models.dashboard import Member
from server.test_tracker.services.dashboard import *
from server.test_tracker.services.member import get_member_by_email
from server.test_tracker.services.users import get_user_by_id
from server.test_tracker.utils.send_mail import send_email
from server.test_tracker.utils.validations import Validator
from server.test_tracker.serializers.dashboard import (
    GetMemberSerializer, MemberSerializer, MemberSerializer, ProjectsSerializer, ProfileSerializers
)


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
        projects = get_project_by_user_id(request.user.id)
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
    serializer_class = MemberSerializer
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

class GetMemberApiView(GenericAPIView):
    """
        You may have to use this class when you want to get all of your Member
        You must be authenticated to access this view
    """
    serializer_class = GetMemberSerializer
    permission_classes = (UserIsAuthenticated,)

    def get(self, request: Request) -> Response:
        """Use this method to get all of member based on request user"""
        member: Member = get_member_based_on_user(request.user)
        if len(member) > 0:
            return CustomResponse.success(
                data=GetMemberSerializer(member, many=True).data,
                message="Member found successfully",
            )
        return CustomResponse.success(
            [],
            message="There are no Member yet, try tp add one",
        )

class MemberDetailAPIView(GenericAPIView):
    """
        Class MemberDetailAPIView has all the functionality based on the Member added
        Methods [GET, PUT, DELETE]
    """
    serializer_class = MemberSerializer
    permission_classes = (UserIsAuthenticated,)

    def get(self, request: Request, member_email: str) -> Response:
        """Return a single member based on the request user, member_email"""
        member: Member = get_member_by_user_and_member_email(
            request.user, member_email
        )
        if member is not None:
            return CustomResponse.success(
                data=MemberSerializer(member).data,
                message="User found successfully",
            )
        return CustomResponse.not_found(
            message="User not found",
        )

    def delete(self, request: Request, member_email: str) -> Response:
        """
            The host can delete the member, 
            but it will not deleted from the whole system (only from access)
        """
        member: Member = get_member_by_user_and_member_email(
            request.user, member_email
        )
        if member is not None:
            member.delete()
            return CustomResponse.success(
                message="User deleted successfully",
                status_code=204
            )
        return CustomResponse.not_found(
            message="User not found",
        )

class FULLACCESSPermissionAPIView(GenericAPIView):
    """
        Class MemberPermissionAPIView have all the functionality based on the Member added
    """
    serializer_class = MemberSerializer
    permission_classes = (UserIsAuthenticated,)

    def get(self, request: Request) -> Response:
        member = get_full_access_permission_based_on_user(request.user)
        return CustomResponse.success(
            data=MemberSerializer(member, many=True).data,
            message="Member found successfully",
        )

class ADMINACCESSPermissionAPIView(GenericAPIView):
    """
        Class MemberPermissionAPIView have all the functionality based on the Member added
    """
    serializer_class = MemberSerializer
    permission_classes = (UserIsAuthenticated,)

    def get(self, request: Request) -> Response:
        member = get_admin_access_permission_based_on_user(request.user)
        return CustomResponse.success(
            data=MemberSerializer(member, many=True).data,
            message="Member found successfully",
        )

class UpdateProfileAPIView(GenericAPIView):
    """This class to update profile info"""
    serializer_class = ProfileSerializers
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
    serializer_class = ProfileSerializers
    permission_classes = (UserIsAuthenticated,)

    def get(self, request: Request, user_id:str) -> Response:
        """Returns user profile"""
        user = get_user_by_id(user_id)
        if user is not None:
            return CustomResponse.success(
                data=ProfileSerializers(user).data,
                message="Profile found successfully",
            )
        return CustomResponse.not_found(
            message="Profile not found",
        )

class GetTotalProjectsAPIView(GenericAPIView):
    """This class to get total projects"""
    permission_classes = (UserIsAuthenticated,)

    def get(self, request: Request) -> Response:
        """Returns total projects"""
        total_projects = get_total_projects(request.user)
        return CustomResponse.success(
            data=total_projects,
            message="Total projects found successfully",
        )

"""Everything related to dashboard."""
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from server.test_tracker.api.permission import UserIsAuthenticated
from server.test_tracker.api.response import CustomResponse
from server.test_tracker.models.dashboard import People
from server.test_tracker.models.users import InviteSignature, User
from server.test_tracker.services.dashboard import *
from server.test_tracker.services.users import get_user_by_email_for_login, get_user_by_id
from server.test_tracker.utils.send_mail import send_email
from server.test_tracker.utils.validations import Validator
from server.test_tracker.serializers.dashboard import (
    GetPersonSerializer, PeopleSerializer, ProjectsSerializer, ProfileSerializers
)
from server.components import config



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
        """Get all projects based on creator, people users"""
        projects = get_project_by_user_id(request.user.id)
        serializer = ProjectsSerializer(projects, many=True)
        return CustomResponse.success(
            data = serializer.data,
            message = "Projects retrieved successfully",
            status_code = 200
        )
class ProjectsDetailAPIView(GenericAPIView):
    """
        Class ProjectsAPIView have all the functionality based on the project
        Methods [GET, PUT, DELETE]
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
                            status_code=203
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

class PeopleAPIView(GenericAPIView):
    """
        Class PeopleAPIView have all the functionality based on the user
    """
    serializer_class = PeopleSerializer
    permission_classes = (UserIsAuthenticated,)

    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.data['host_user'] = request.user
            new_signature = InviteSignature.objects.create(
                json_data = serializer.data
            )
            first_name:str = serializer.validated_data.get('first_name')
            email:str = serializer.validated_data.get('email')
            if get_user_by_email_for_login(email):
                send_email(
                    first_name, request.user, email, 
                    redirect_link=f"http://localhost:8080/auth/register/?signature={new_signature.signature}"
                )
                People.objects.create(
                    host_user=request.user,
                    invited=True,
                    signature = new_signature
                )
                return CustomResponse.success(
                    data=serializer.data,
                    message="Person added successfully",
                )
            return CustomResponse.bad_request(
                message="Person already exists",
                status_code=400
            )
        return CustomResponse.bad_request(
            error=serializer.errors,
            message="Person creation failed",
        )

class GetPersonApiView(GenericAPIView):
    """
        You may have to use this class when you want to get all of your people
        You must be authenticated to access this view
    """
    serializer_class = GetPersonSerializer
    permission_classes = (UserIsAuthenticated,)

    def get(self, request: Request) -> Response:
        """Use this method to get all of people based on request user"""
        people: People = get_people_based_on_user(request.user)
        if len(people) > 0:
            return CustomResponse.success(
                data=GetPersonSerializer(people, many=True).data,
                message="People found successfully",
            )
        return CustomResponse.success(
            [],
            message="There are no people yet, try tp add one",
        )

class PeopleDetailAPIView(GenericAPIView):
    """
        Class PeopleDetailAPIView has all the functionality based on the people added
        Methods [GET, PUT, DELETE]
    """
    serializer_class = PeopleSerializer
    permission_classes = (UserIsAuthenticated,)

    def get(self, request: Request, person_email: str) -> Response:
        """Return a single person based on the request user, person_email"""
        person: People = get_person_by_user_and_person_email(
            request.user, person_email
        )
        if person is not None:
            return CustomResponse.success(
                data=PeopleSerializer(person).data,
                message="User found successfully",
            )
        return CustomResponse.not_found(
            message="User not found",
        )

    def delete(self, request: Request, person_email: str) -> Response:
        """
            The host can delete the person, 
            but it will not deleted from the whole system (only from access)
        """
        person: People = get_person_by_user_and_person_email(
            request.user, person_email
        )
        if person is not None:
            person.delete()
            return CustomResponse.success(
                message="User deleted successfully",
                status_code=204
            )
        return CustomResponse.not_found(
            message="User not found",
        )

class FULLACCESSPermissionAPIView(GenericAPIView):
    """
        Class PeoplePermissionAPIView have all the functionality based on the people added
    """
    serializer_class = PeopleSerializer
    permission_classes = (UserIsAuthenticated,)

    def get(self, request: Request) -> Response:
        people = get_full_access_permission_based_on_user(request.user)
        return CustomResponse.success(
            data=PeopleSerializer(people, many=True).data,
            message="People found successfully",
        )

class ADMINACCESSPermissionAPIView(GenericAPIView):
    """
        Class PeoplePermissionAPIView have all the functionality based on the people added
    """
    serializer_class = PeopleSerializer
    permission_classes = (UserIsAuthenticated,)

    def get(self, request: Request) -> Response:
        people = get_admin_access_permission_based_on_user(request.user)
        return CustomResponse.success(
            data=PeopleSerializer(people, many=True).data,
            message="People found successfully",
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
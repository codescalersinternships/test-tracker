"""Everything related to the project."""
import datetime
from server.test_tracker.api.permission import HasProjectAccess, UserIsAuthenticated
from server.test_tracker.api.response import CustomResponse
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from server.test_tracker.models.dashboard import Member, Project
from server.test_tracker.serializers.dashboard import ProjectsSerializer
from server.test_tracker.serializers.project import ActivitySerializer

from server.test_tracker.services.dashboard import find_project_name_based_on_user, get_project_by_id
from server.test_tracker.services.member import get_member_by_id
from server.test_tracker.services.project import project_member_validation, update_activity
from server.test_tracker.utils.validations import Validator




class ProjectsDetailAPIView(GenericAPIView):
    """
        Class ProjectsAPIView have all the functionality based on the project
        Methods [GET, PUT, DELETE]
    """
    serializer_class = ProjectsSerializer
    permission_classes = (HasProjectAccess,)

    def get(self, request: Request, project_id: str) -> Response:
        """Return a single project based on the given project id"""
        project = get_project_by_id(project_id)
        serializer = ProjectsSerializer(project, context={'request': request})
        if project is not None:
            return CustomResponse.success(
                data=serializer.data,
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
                        project = serializer.save(user = request.user)
                        update_activity(
                            datetime.datetime.now(), request.user, project,
                            "Create", "Project", project.name
                        )
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

class ProjectActivityAPIView(GenericAPIView):
    """Get all project activity"""
    serializer_class = ActivitySerializer
    permission_classes = (UserIsAuthenticated,)

    def get(self, request: Request, project_id: str) -> Response:
        project = get_project_by_id(project_id)
        if project is None:
            return CustomResponse.not_found(message = "Project not found")
        result = []
        if len(project.activity) > 0:
            for items, values in project.activity.items():                    
                result.append(
                    {
                        "date" : values.get('date'),
                        "action" : values.get('action')
                    }
                )

        return CustomResponse.success(
            message="Success plans found.",
            data = result[::-1]
        )

class AddMemberToProjectAPIView(GenericAPIView):
    """Add Member to project"""
    permission_classes = (UserIsAuthenticated,)
    serializer_class = ProjectsSerializer

    def put(self, request:Request, project_id: Project, member_id: Member) -> Response:
        """
            Add Member to project
            You must be authenticated to access this view
        """
        project = get_project_by_id(project_id)
        member = get_member_by_id(member_id)
        user = request.user

        if project_member_validation(project, member, user) != True:
            return project_member_validation(project, member, user)
        update_activity(
            datetime.datetime.now(), request.user, project,
            f"added {member.first_name.title()} to", "Project", project.name
        )
        project.members.add(member)
        return CustomResponse.success(
            message = "Member added to project successfully",
            status_code = 201
        )

    def delete(self, request:Request, project_id: Project, member_id: Member) -> Response:
        """
            Add Member to project
            You must be authenticated to access this view
        """
        project = get_project_by_id(project_id)
        member = get_member_by_id(member_id)
        user = request.user

        if project_member_validation(project, member, user, remove=True) != True:
            return project_member_validation(project, member, user)
        update_activity(
            datetime.datetime.now(), request.user, project,
            f"removed {member.first_name.title()} from", "Project", project.name
        )
        project.members.remove(member)
        return CustomResponse.success(
            status_code = 204
        )

class GetLast5ProjectsUpdatedAPIView(GenericAPIView):
    """
        * Usage
        Class to get last 5 Updated
    """
    serializer_class = ProjectsSerializer
    permission_classes = (UserIsAuthenticated,)

    def get(self, request: Request) -> Response:
        """
            Get last 5 projects updated based on user
            You must be authenticated to access this view
        """
        member = get_member_by_id(str(request.user.id))

        if member is not None:
            # Thats mean the request from a member
            user = member.host_user
            projects = Project.objects.filter(
                members__in=[request.user.id], user = user
            ).order_by('-modified')
        else:
            projects = Project.objects.filter(user=request.user).order_by('-modified')
        projects = projects[:5]

        return CustomResponse.success(
            message = "Success projects found.",
            data = ProjectsSerializer(projects, many=True).data
        )


class GetActivityOfLast5ProjectsAPIView(GenericAPIView):
    """
        * Usage
        This class to concatenate the activity of the last 5 projects updated.
    """
    serializer_class = ActivitySerializer
    permission_classes = (UserIsAuthenticated,)

    def get(self, request: Request) -> Response:
        """A get method that returns last update from last 5 projects activity"""
        result = []
        member = get_member_by_id(str(request.user.id))

        if member is not None:
            # Thats mean the request from a member
            user = member.host_user
            projects = Project.objects.filter(
                members__in=[request.user.id], user = user
            ).order_by('-modified')

        else:
            projects = Project.objects.filter(user = request.user).order_by('-modified')
        projects = projects[:5]

        for project in projects:
            if len(list(project.activity.keys())) > 1:
                last_key = project.activity[list(project.activity.keys())[-1]]                    
                if last_key.get('date') and last_key.get('action'):
                    result.append(
                        {
                        "date" : last_key.get('date'),
                        "action" : last_key.get('action')
                        }
                    )
        return CustomResponse.success(
            message="Success activity found.",
            data = result
        )

class SearchProjectAPIView(GenericAPIView):
    """
        * Usage
        This class to filter all op projects based on project name.
    """
    serializer_class = ProjectsSerializer
    permission_classes = (UserIsAuthenticated,)

    def get(self, request:Request, project_name: str):
        """
            Get all projects based on project name
            You must be authenticated to access this view
        """
        user = request.user
        if hasattr(user, 'permission'):
            member = get_member_by_id(user.id)
            user = member.host_user
        projects = Project.objects.filter(name__icontains=project_name, user=user)
        return CustomResponse.success(
            message="Success projects found.",
            data = ProjectsSerializer(projects, many=True).data
        )
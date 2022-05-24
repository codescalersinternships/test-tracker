"""Everything related to requeriments"""
import datetime
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from django.db.models import Q

from server.test_tracker.api.permission import HasProjectAccess, UserIsAuthenticated
from server.test_tracker.services.requirement import *
from server.test_tracker.api.response import CustomResponse
from server.test_tracker.serializers.requirement import RequirementDocsSerializer, RequirementsSerializer
from server.test_tracker.services.dashboard import get_project_by_id
from server.test_tracker.services.project import update_activity
from server.test_tracker.utils.handler import RequirementDocssHandling, RequirementHandling




class PostNewRequirementDocssAPIView(GenericAPIView):
    """class project requirement view"""
    serializer_class = RequirementDocsSerializer
    permission_classes = (HasProjectAccess,)

    def post(self, request: Request, project_id: str) -> Response:
        """post a new requirement"""
        project = get_project_by_id(project_id)
        if project is not None:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                requirements = serializer.save(project=project)
                update_activity(
                    datetime.datetime.now(), request.user, project,
                    "Create", "Project requirements", requirements.title
                )
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

class GetAllRequirementDocssAPIView(GenericAPIView):
    """class project requirement view"""
    serializer_class = RequirementDocsSerializer
    permission_classes = (HasProjectAccess,)

    def get(self, request: Request, project_id: str) -> Response:
        """
            *Usage
            get all requirements for a project
        """
        project = get_project_by_id(project_id)
        if project is None:
            return CustomResponse.not_found(message = "Project not found")
        requirements = filter_requirements_by_project(project)
        serializer = self.get_serializer(requirements, many=True)
        return CustomResponse.success(
            data=serializer.data,
            message="All requirements for project",
            status_code=200
        )

class SearchRequirementDocssAPIView(GenericAPIView):
    """
        *Usage
        class project requirement view search on project requirements
    """
    serializer_class = RequirementDocsSerializer
    permission_classes = (HasProjectAccess,)

    def get(self, request: Request, project_id: str, key_word: str) -> Response:
        """get all requirements for a project"""
        project = get_project_by_id(project_id)
        if project is None:
            return CustomResponse.not_found(message = "Project not found")
        requirements = RequirementDocs.objects.filter(
            title__icontains=key_word,
            project = project
        )
        serializer = self.get_serializer(requirements, many=True)
        return CustomResponse.success(
            data=serializer.data,
            message="All requirements for project",
            status_code=200
        )

class RequirementDocssDetailsAPIView(GenericAPIView):
    """
        *Usage: Get
        class project requirement view
    """
    serializer_class = RequirementDocsSerializer
    permission_classes = (HasProjectAccess,)

    def get(self, request: Request, project_id: str, requirement_id: str) -> Response:
        """Use this endpoint to get requirement detail and sub requirements"""
        project_requirement = RequirementDocssHandling.validate(project_id, requirement_id)
        serializer = RequirementDocsSerializer(project_requirement)
        return CustomResponse.success(
            message="Success Found Project Requirement",
            data=serializer.data
        )

    def put(self, request: Request, project_id: str, requirement_id: str) -> Response:
        """update a requirement"""
        project_requirement = RequirementDocssHandling.validate(project_id, requirement_id)
        serializer = self.get_serializer(project_requirement, data=request.data)

        if serializer.is_valid():
            saved_project_requirement = serializer.save()
            update_activity(
                datetime.datetime.now(), request.user, get_project_by_id(project_id),
                "Update", "Project requirement", saved_project_requirement.title
            )
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
        project_requirement = RequirementDocssHandling.validate(project_id, requirement_id)
        update_activity(
            datetime.datetime.now(), request.user, get_project_by_id(project_id),
            "Delete", "Project requirements", project_requirement.title
        )
        project_requirement.delete()
        return CustomResponse.success(
            data={},
            message="Requirement deleted successfully",
            status_code=204
        )

class RequirementAPIView(GenericAPIView):
    """This class is a sub requirement for project requirements"""
    serializer_class = RequirementsSerializer
    permission_classes = (UserIsAuthenticated,)

    def post(self, request: Request, requirements_id: str) -> Response:
        """
            post a new requirement based on the requirements_id
            - requirements_id: the id of the parent requirements
        """
        requirements = get_project_requirement_by_id(requirements_id)
        if requirements is not None:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                requirement = serializer.save(requirement=requirements)
                update_activity(
                    datetime.datetime.now(), request.user, requirements.project,
                    "Create", "requirement", requirement.title
                )
                return CustomResponse.success(
                    data=serializer.data,
                    message="Requirement created successfully",
                    status_code=201
                )
            return CustomResponse.bad_request(
                message="Requirement creation failed",
                error=serializer.errors
            )
        return CustomResponse.not_found(message="Requirement not found")

    def get(self, request: Request, requirements_id: str) -> Response:
        """
            get all requirements based on the requirements_id
            - requirements_id: the id of the parent requirements
        """
        project_requirements = get_project_requirement_by_id(requirements_id)
        requirements = filter_requirements_based_on_project_requirement(project_requirements)
        if project_requirements is None:
            return CustomResponse.not_found(message = "Project requirement not found")
        serializer = self.get_serializer(requirements, many=True)
        return CustomResponse.success(
            data=serializer.data,
            message="All requirements for requirement",
            status_code=200
        )

class RequirementsDetailAPIView(GenericAPIView):
    """
        *Usage 
        class project requirement view
    """
    serializer_class = RequirementsSerializer
    permission_classes = (HasProjectAccess,)

    def get(
        self, request: Request, project_id: str, project_requirement_id: str,
        requirement_id: str
        ) -> Response:
        """
            Get the requirement based on 3 things:
                -1 project_id, this is the project id 
                    to check if you have a permission for this action or not
                -2 project_requirement_id, this is another required thing to get all sub requirements
                -3 requirement_id, as logical this is the requirement id
        """
        requirement = RequirementHandling.validate(
            project_id, project_requirement_id, requirement_id
        )

        serializer = self.get_serializer(requirement)
        return CustomResponse.success(
            data=serializer.data,
            message="Requirement retrieved successfully",
            status_code=200
        )

    def put(self, request: Request, project_id: str, project_requirement_id: str,
        requirement_id: str
        ) -> Response:
        """
            Update the requirement based on 3 things:
                -1 project_id, this is the project id 
                    to check if you have a permission for this action or not
                -2 project_requirement_id, this is another required thing to get all sub requirements
                -3 requirement_id, as logical this is the requirement id
        """
        requirement = RequirementHandling.validate(
            project_id, project_requirement_id, requirement_id
        )

        serializer = self.get_serializer(requirement, data=request.data)
        if serializer.is_valid():
            requirement = serializer.save()
            update_activity(
                datetime.datetime.now(), request.user, requirement.requirement.project,
                "Update", "requirement", requirement.title
            )
            return CustomResponse.success(
                data=serializer.data,
                message="Requirement updated successfully",
                status_code=201
            )
        return CustomResponse.bad_request(
            message="Requirement update failed",
            error=serializer.errors
        )
    
    def delete(
        self, request: Request, project_id: str, project_requirement_id: str,
        requirement_id: str
        ) -> Response:
        """
            Delete the requirement based on 3 things:
                -1 project_id, this is the project id 
                    to check if you have a permission for this action or not
                -2 project_requirement_id, this is another required thing to get all sub requirements
                -3 requirement_id, as logical this is the requirement id
        """
        requirement = RequirementHandling.validate(
            project_id, project_requirement_id, requirement_id
        )
        update_activity(
            datetime.datetime.now(), request.user, requirement.requirement.project,
            "Delete", "requirement", requirement.title
        )
        requirement.delete()
        return CustomResponse.success(
            data={},
            message="Requirement deleted successfully",
            status_code=204
        )

class SearchRequirementsInRequirementDocssAPIView(APIView):
    """
        *Usage
        Use this endpoint to filter any requirement based on title or description
    """
    def get(self, request: Request, project_id: str, key_word: str):
        """
            Keyword is the key you pass to filter
        """
        project = get_project_by_id(project_id)
        requirement = Requirements.objects.filter(
            Q(
                title__icontains = key_word, 
                requirement__id__in = project.project_requirements.all().values_list('id', flat=True)
            )| 
            Q(
                description__icontains = key_word, 
                requirement__id__in = project.project_requirements.all().values_list('id', flat=True)
            )
        )
        return CustomResponse.success(
            data=RequirementsSerializer(requirement, many=True).data,
            message = "Successfully.",
        )
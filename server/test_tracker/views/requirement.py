"""Everything related to requeriments"""
import datetime
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from django.db.models import Q

from test_tracker.api.permission import HasProjectAccess
from test_tracker.api.response import CustomResponse
from test_tracker.models.project import RequirementDocs, Requirements
from test_tracker.serializers.requirement import (
    RequirementDocsSerializer,
    RequirementsSerializer,
)
from test_tracker.services.dashboard import get_project_by_id
from test_tracker.services.project import update_activity
from test_tracker.services.requirement import (
    filter_requirements_based_on_project_requirement,
    filter_requirements_by_project,
    get_project_requirement_by_id,
    get_requirement_doc_by_id,
)
from test_tracker.utils.handler import (
    RequirementDocssHandling,
    RequirementHandling,
)
from test_tracker.utils.validations import Validator


class PostNewRequirementDocsAPIView(GenericAPIView):
    """class project requirement view"""

    serializer_class = RequirementDocsSerializer
    permission_classes = (HasProjectAccess,)

    def post(self, request: Request, project_id: str) -> Response:
        """post a new requirement"""
        project = get_project_by_id(project_id)
        if project is not None:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                title: str = serializer.validated_data.get("title")
                validate_name: str = Validator().validate_string(title)
                if not validate_name:
                    return CustomResponse.bad_request(
                        message=f"Name '{title}' is not a valid name, Please choose a valid project name.",
                    )
                requirements = serializer.save(project=project)
                update_activity(
                    datetime.datetime.now(),
                    request.user,
                    project,
                    "Create",
                    "Project requirements",
                    requirements.title,
                )
                return CustomResponse.success(
                    data=serializer.data,
                    message="Requirement created successfully",
                    status_code=201,
                )
            return CustomResponse.bad_request(
                message="Requirement creation failed", error=serializer.errors
            )
        return CustomResponse.not_found(message="Project not found")


class GetAllRequirementDocsAPIView(GenericAPIView):
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
            return CustomResponse.not_found(message="Project not found")
        requirements = filter_requirements_by_project(project)
        serializer = self.get_serializer(requirements, many=True)
        return CustomResponse.success(
            data=serializer.data,
            message="All requirements for project",
            status_code=200,
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
            return CustomResponse.not_found(message="Project not found")
        requirements = RequirementDocs.objects.filter(
            title__icontains=key_word, project=project
        )
        serializer = self.get_serializer(requirements, many=True)
        return CustomResponse.success(
            data=serializer.data,
            message="All requirements for project",
            status_code=200,
        )


class RequirementDocsDetailsAPIView(GenericAPIView):
    """
    *Usage: Get
    class project requirement view
    """

    serializer_class = RequirementDocsSerializer
    permission_classes = (HasProjectAccess,)

    def get(self, request: Request, project_id: str, requirement_id: str) -> Response:
        """Use this endpoint to get requirement detail and sub requirements"""
        project = get_project_by_id(project_id)
        requirement = get_requirement_doc_by_id(requirement_id)
        print(project, requirement)
        if project is None:
            return CustomResponse.not_found(message="Project not found")
        if requirement is None:
            return CustomResponse.not_found(message="Requirement not found")
        if requirement.id not in project.project_requirements.all().values_list(
            "id", flat=True
        ):
            return CustomResponse.unauthorized()
        serializer = self.get_serializer(requirement)
        return CustomResponse.success(
            data=serializer.data, message="Requirement detail", status_code=200
        )

    def put(self, request: Request, project_id: str, requirement_id: str) -> Response:
        """update a requirement"""
        project_requirement = RequirementHandling.validate(project_id, requirement_id)
        serializer = self.get_serializer(project_requirement, data=request.data)

        if serializer.is_valid():
            saved_project_requirement = serializer.save()
            update_activity(
                datetime.datetime.now(),
                request.user,
                get_project_by_id(project_id),
                "Update",
                "Project requirement",
                saved_project_requirement.title,
            )
            return CustomResponse.success(
                data=serializer.data,
                message="Requirement updated successfully",
                status_code=201,
            )
        return CustomResponse.bad_request(
            message="Requirement update failed", error=serializer.errors
        )

    def delete(
        self, request: Request, project_id: str, requirement_id: str
    ) -> Response:
        """delete a requirement"""
        project_requirement = RequirementDocssHandling.validate(
            project_id, requirement_id
        )
        update_activity(
            datetime.datetime.now(),
            request.user,
            get_project_by_id(project_id),
            "Delete",
            "Project requirements",
            project_requirement.title,
        )
        project_requirement.delete()
        return CustomResponse.success(
            data={}, message="Requirement deleted successfully", status_code=204
        )


class RequirementAPIView(GenericAPIView):
    """This class is a sub requirement for project requirements"""

    serializer_class = RequirementsSerializer
    permission_classes = (HasProjectAccess,)

    def post(self, request: Request, project_id: str, requirements_id: str) -> Response:
        """
        post a new requirement based on the requirements_id
        - project_id: project that requirement will create inside
        - requirements_id: the id of the parent requirement document
        """
        title: str = request.data.get("title")
        validate_name: str = Validator().validate_string(title)
        project = get_project_by_id(project_id)
        requirement = get_project_requirement_by_id(requirements_id)

        if not validate_name:
            return CustomResponse.bad_request(
                message=f"Name '{title}' is not a valid name, Please choose a valid project name.",
            )
        if project is None:
            return CustomResponse.not_found("Project not found.")
        if requirement is None:
            return CustomResponse.not_found("Project requirement document not found.")
        if requirement.project != project:
            return CustomResponse.unauthorized()

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            req_id_project = requirement.project.REQ_Title
            if len(req_id_project) > 0:
                last_title = int(req_id_project[-1][3:])
            else:
                last_title = 0
            if last_title < 9:
                last_title = "0" + str(last_title + 1)
            else:
                last_title = str(last_title + 1)
            req_id_project.append(f"REQ{last_title}")
            requirement = serializer.save(
                requirement=requirement, requirement_title=f"REQ{last_title}"
            )
            update_activity(
                datetime.datetime.now(),
                request.user,
                requirement.requirement.project,
                "Create",
                "requirement",
                requirement.title,
            )
            return CustomResponse.success(
                data=serializer.data,
                message="Requirement created successfully",
                status_code=201,
            )

    def get(self, request: Request, project_id: str, requirements_id: str) -> Response:
        """
        get all requirements based on the requirements_id
        - requirements_id: the id of the parent requirements
        """
        project_requirements = get_project_requirement_by_id(requirements_id)
        requirements = filter_requirements_based_on_project_requirement(
            project_requirements
        )
        if project_requirements is None:
            return CustomResponse.not_found(message="Project requirement not found")
        serializer = self.get_serializer(requirements, many=True)
        return CustomResponse.success(
            data=serializer.data,
            message="All requirements for requirement",
            status_code=200,
        )


class RequirementsDetailAPIView(GenericAPIView):
    """
    *Usage
    class project requirement view
    """

    serializer_class = RequirementsSerializer
    permission_classes = (HasProjectAccess,)

    def get(
        self,
        request: Request,
        project_id: str,
        project_requirement_id: str,
        requirement_id: str,
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
            status_code=200,
        )

    def put(
        self,
        request: Request,
        project_id: str,
        project_requirement_id: str,
        requirement_id: str,
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
                datetime.datetime.now(),
                request.user,
                requirement.requirement.project,
                "Update",
                "requirement",
                requirement.title,
            )
            return CustomResponse.success(
                data=serializer.data,
                message="Requirement updated successfully",
                status_code=201,
            )
        return CustomResponse.bad_request(
            message="Requirement update failed", error=serializer.errors
        )

    def delete(
        self,
        request: Request,
        project_id: str,
        project_requirement_id: str,
        requirement_id: str,
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
            datetime.datetime.now(),
            request.user,
            requirement.requirement.project,
            "Delete",
            "requirement",
            requirement.title,
        )
        requirement.delete()
        return CustomResponse.success(
            data={}, message="Requirement deleted successfully", status_code=204
        )


class SearchRequirementsInRequirementDocssAPIView(APIView):
    """
    *Usage
    Use this endpoint to filter any requirement based on title or description
    """

    permission_classes = (HasProjectAccess,)

    def get(self, request: Request, project_id: str, key_word: str):
        """
        Keyword is the key you pass to filter
        """
        project = get_project_by_id(project_id)
        print(key_word)
        requirements = Requirements.objects.filter(
            Q(
                title__icontains=key_word,
                requirement__id__in=project.project_requirements.all().values_list(
                    "id", flat=True
                ),
            )
            | Q(
                description__icontains=key_word,
                requirement__id__in=project.project_requirements.all().values_list(
                    "id", flat=True
                ),
            )
            | Q(
                requirement_title__icontains=key_word,
                requirement__id__in=project.project_requirements.all().values_list(
                    "id", flat=True
                ),
            )
        )
        return CustomResponse.success(
            data=RequirementsSerializer(requirements, many=True).data,
            message="Successfully.",
        )

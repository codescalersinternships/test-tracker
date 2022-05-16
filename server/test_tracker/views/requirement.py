"""Everything related to requeriments"""
import datetime
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from server.test_tracker.services.requirement import *
from server.test_tracker.api.response import CustomResponse
from server.test_tracker.serializers.requirement import ProjectRequirementSerializer, RequirementsSerializer
from server.test_tracker.services.dashboard import get_project_by_id
from server.test_tracker.services.project import update_activity




class ProjectRequirementsAPIView(GenericAPIView):
    """class project requirement view"""
    serializer_class = ProjectRequirementSerializer

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

class GetProjectRequirementsAPIView(GenericAPIView):
    """class project requirement view"""
    serializer_class = ProjectRequirementSerializer

    def get(self, request: Request, project_id: str) -> Response:
        """get all requirements for a project"""
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

class UpdateProjectRequirementsAPIView(GenericAPIView):
    """class project requirement view"""
    serializer_class = ProjectRequirementSerializer

    def put(self, request: Request, project_id: str, requirement_id: str) -> Response:
        """update a requirement"""
        project = get_project_by_id(project_id)
        requirement = get_requirements_by_id(requirement_id)
        if project is None:
            return CustomResponse.not_found(message = "Project not found")
        if requirement is None:
            return CustomResponse.not_found(message = "Requirement not found")

        serializer = self.get_serializer(requirement, data=request.data)
        if serializer.is_valid():
            requirements = serializer.save()
            update_activity(
                datetime.datetime.now(), request.user, project,
                "Update", "Project requirements", requirements.title
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
        project = get_project_by_id(project_id)
        requirements = get_requirements_by_id(requirement_id)
        if project is None:
            return CustomResponse.not_found(message = "Project not found")
        if requirements is None:
            return CustomResponse.not_found(message = "Requirement not found")
        update_activity(
            datetime.datetime.now(), request.user, project,
            "DELETE", "Project requirements", requirements.title
        )
        requirements.delete()
        return CustomResponse.success(
            data={},
            message="Requirement deleted successfully",
            status_code=204
        )

class RequirementAPIView(GenericAPIView):
    """This class is a sub requirement for project requirements"""
    serializer_class = RequirementsSerializer

    def post(self, request: Request, requirements_id: str) -> Response:
        """
            post a new requirement based on the requirements_id
            - requirements_id: the id of the parent requirements
        """
        requirements = get_requirements_by_id(requirements_id)
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
        project_requirements = get_requirements_by_id(requirements_id)
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
    """class project requirement view"""
    serializer_class = RequirementsSerializer

    def get(self, request: Request, requirement_id: str) -> Response:
        """get a requirement"""
        requirement = get_requirement_by_id(requirement_id)
        if requirement is None:
            return CustomResponse.not_found(message = "Requirement not found")
        serializer = self.get_serializer(requirement)
        return CustomResponse.success(
            data=serializer.data,
            message="Requirement retrieved successfully",
            status_code=200
        )

    def put(self, request: Request, requirement_id: str) -> Response:
        """update a requirement"""
        requirement = get_requirement_by_id(requirement_id)

        if requirement is None:
            return CustomResponse.not_found(message = "Requirement not found")

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
    
    def delete(self, request: Request, requirement_id: str) -> Response:
        """delete a requirement"""
        requirement = get_requirement_by_id(requirement_id)

        if requirement is None:
            return CustomResponse.not_found(message = "Requirement not found")
        update_activity(
            datetime.datetime.now(), request.user, requirement.requirement.project,
            "Update", "requirement", requirement.title
        )
        requirement.delete()
        return CustomResponse.success(
            data={},
            message="Requirement deleted successfully",
            status_code=204
        )
from test_tracker.api.response import CustomResponse
from test_tracker.services.dashboard import get_project_by_id
from test_tracker.services.project import get_test_plan_by_id
from test_tracker.services.requirement import (
    get_project_requirement_by_id,
    get_requirement_by_id,
)


class TestPlanHandling:
    """There was a duplication on the code thats why we create this class"""

    @staticmethod
    def validate(project_id: str, test_plan_id: str):
        """Validate project and test plan if right"""
        project = get_project_by_id(project_id)
        test_plan = get_test_plan_by_id(test_plan_id)
        if project is None:
            return CustomResponse.not_found(
                message="There are no test plan with this id"
            )
        if test_plan is None:
            return CustomResponse.not_found(
                message="There are no test plan with this id"
            )
        if test_plan.project != project:
            return CustomResponse.bad_request(
                message="You don't have permission to access this test plan"
            )
        return test_plan


class RequirementDocssHandling:
    """
    There was a duplication on the code thats why we create this class
    """

    @staticmethod
    def validate(project_id: str, requirement_id: str):
        """Validate project and project_requirements if right"""
        project = get_project_by_id(project_id)
        project_requirement = get_project_requirement_by_id(requirement_id)

        if project is None:
            return CustomResponse.not_found(message="Project does not exist")
        if project_requirement is None:
            return CustomResponse.not_found(
                message="Project Requirement does not exist"
            )

        if project_requirement.project != project:
            return CustomResponse.bad_request(
                message="You don't have permission to access this test plan"
            )
        return project_requirement


class RequirementHandling:
    """
    There was a duplication on the code thats why we create this class
    """

    @staticmethod
    def validate(project_id: str, project_requirement_id: str, requirement_id: str):
        """Validate project and project_requirements if right"""
        project = get_project_by_id(project_id)
        project_requirement = get_project_requirement_by_id(project_requirement_id)
        requirement = get_requirement_by_id(requirement_id)

        if project is None:
            return CustomResponse.not_found(message="Project does not exist")
        if project_requirement is None:
            return CustomResponse.not_found(
                message="Project Requirement does not exist"
            )
        if requirement is None:
            return CustomResponse.not_found(message="This requirement does not exist")

        if (
            project_requirement.project != project
            or requirement.requirement != project_requirement
        ):
            return CustomResponse.bad_request(
                message="You don't have permission to access this test plan"
            )

        return requirement

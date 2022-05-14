from server.test_tracker.api.response import CustomResponse
from server.test_tracker.services.dashboard import get_project_by_id
from server.test_tracker.services.project import get_test_plan_by_id


class TestPlanHandeling():
    """There was a duplication on the code thats why we create this class"""
    @staticmethod
    def valid(project_id:str, test_plan_id:str):
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
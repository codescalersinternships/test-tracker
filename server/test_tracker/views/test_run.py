"""Everything related to test runs"""
import datetime
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from test_tracker.api.permission import HasProjectAccess, UserIsAuthenticated
from test_tracker.api.response import CustomResponse
from test_tracker.models.project import (
    TEST_RUN_STATUS_CHOICES,
    TestCases,
    TestPlan,
    TestRun,
    TestSuites,
)
from test_tracker.serializers.test_cases import TestCaseSerializer
from test_tracker.serializers.test_run import TestRunsSerializer
from test_tracker.services.dashboard import get_project_by_id
from test_tracker.services.member import get_member_by_id
from test_tracker.services.project import get_test_run_by_id, update_activity
from test_tracker.services.test_cases import (
    filter_test_cases_by_test_suite,
    month_filter_test_cases_based_on_test_suites,
)


class TestRunAPIView(GenericAPIView):
    """Class TestRunAPIView to handle test runs endpoints"""

    serializer_class = TestRunsSerializer
    permission_classes = (HasProjectAccess,)

    def post(self, request: Request, project_id: str) -> Response:
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            project = get_project_by_id(project_id)
            test_suites_ids = [suite["id"] for suite in request.data["test_suites"]]
            test_suites = TestSuites.objects.filter(id__in=test_suites_ids)
            for suite in test_suites:
                if suite.project != project:
                    return CustomResponse(
                        status=400, message="Test suite does not belong to this project"
                    )
            test_plan = TestPlan.objects.get(
                project=project, id=request.data["test_plan"]
            )
            if test_plan.project != project:
                return CustomResponse(
                    status=400, message="Test plan does not belong to this project"
                )

            run = serializer.save(
                status=TEST_RUN_STATUS_CHOICES.NOT_STARTED,
                test_suites=test_suites,
                test_plan=test_plan,
            )
            update_activity(
                datetime.datetime.now(),
                request.user,
                project,
                "Create",
                "Test Run",
                run.title,
            )
            return CustomResponse.success(
                message="Success created test run",
                data=serializer.data,
                status_code=201,
            )
        return CustomResponse.bad_request(serializer.errors)

    def get(self, request: Request, project_id: str) -> Response:
        """
        This method is used to get all the test runs
        """
        runs_ids = list(
            set(
                TestRun.objects.filter(test_suites__project__id=project_id).values_list(
                    "id", flat=True
                )
            )
        )
        test_runs = TestRun.objects.filter(id__in=runs_ids).order_by("-created")
        serializer = self.serializer_class(test_runs, many=True)
        return CustomResponse.success(data=serializer.data)


class TestRunDetailAPIView(GenericAPIView):
    """Class TestRunAPIView to handle test runs endpoints"""

    serializer_class = TestRunsSerializer
    permission_classes = (HasProjectAccess,)

    def get(self, request: Request, project_id: str, test_run_id: str) -> Response:
        """
        This method is used to get all the test cases based on test run id
        """
        project = get_project_by_id(project_id)
        if not project:
            return CustomResponse.not_found(message="Project not found")
        test_run = get_test_run_by_id(test_run_id)
        if test_run is None:
            return CustomResponse.not_found(
                message="Test run with id {} not found".format(test_run_id)
            )
        serializer = self.serializer_class(test_run)
        return CustomResponse.success(data=serializer.data)

    def delete(self, request: Request, project_id: str, test_run_id: str) -> Response:
        """Method delete to delete test run"""
        test_run = get_test_run_by_id(test_run_id)
        project = get_project_by_id(project_id)

        if not test_run:
            return CustomResponse.not_found(message="Test Run not found")
        if not project:
            return CustomResponse.not_found(message="Project not found")

        test_suites = test_run.test_suites.all()
        for test_suite in test_suites:
            if test_suite.project != project:
                return CustomResponse.unauthorized()

        update_activity(
            datetime.datetime.now(),
            request.user,
            project,
            "DELETE",
            "Test Run",
            test_run.title,
        )
        test_run.delete()
        return CustomResponse.success(
            message="Test Run deleted successfully", status_code=204
        )


class SearchOnTestRunAPIView(GenericAPIView):
    """
    *Usage
    This class will filter all test runs based on user and status.
    """

    serializer_class = TestRunsSerializer
    permission_classes = (HasProjectAccess,)

    def get(self, request: Request, project_id: str) -> Response:
        """
        This method is used to get all the test runs
        """
        project = get_project_by_id(project_id)
        if not project:
            return CustomResponse.not_found(message="Project not found")

        params = request.query_params
        member = params.get("member")
        status = params.get("status")
        if member:
            test_runs = TestRun.objects.filter(
                test_suites__project_id=project_id, assigned_user__id=int(member)
            )

        if member and status:
            test_runs = TestRun.objects.filter(
                test_suites__project_id=project_id,
                status=status,
                assigned_user__id=int(member),
            )
        if status and not member:
            test_runs = TestRun.objects.filter(
                test_suites__project_id=project_id,
                status=status,
            )
        serializer = self.serializer_class(test_runs, many=True)
        return CustomResponse.success(data=serializer.data)


class LastWeekTestRunReportSheetAPIView(GenericAPIView):
    permission_classes = (HasProjectAccess,)

    def get(self, request: Request, project_id: str) -> Response:
        """
        This method is used to get all the test runs report based on last week
        """
        project = get_project_by_id(project_id)
        if not project:
            return CustomResponse.not_found(message="Project not found")
        today = datetime.datetime.today().date()

        test_runs = TestRun.objects.filter(
            test_suites__project_id=project_id,
            modified__gte=today - datetime.timedelta(days=7),
        ).values_list("id", flat=True)

        test_suites = TestSuites.objects.filter(
            project_id=project_id, run_suites__id__in=test_runs
        ).values_list("id", flat=True)

        test_cases = TestCases.objects.filter(test_suite__id__in=test_suites)
        data = {
            "not_run": test_cases.filter(run=False).count(),
            "passed": test_cases.filter(run=True, passed=True).count(),
            "failed": test_cases.filter(run=True, passed=False, failed=True).count(),
            "skipped": test_cases.filter(
                run=True, passed=False, failed=False, skipped=True
            ).count(),
            "not_started_test_runs": {
                "involve_you": test_runs.filter(
                    status=TEST_RUN_STATUS_CHOICES.NOT_STARTED,
                    assigned_user=request.user,
                ).count(),
                "total_not_started": test_runs.filter(
                    status=TEST_RUN_STATUS_CHOICES.NOT_STARTED,
                ).count(),
            },
            "in_progress_test_runs": {
                "involve_you": test_runs.filter(
                    status=TEST_RUN_STATUS_CHOICES.IN_PROGRESS,
                    assigned_user=request.user,
                ).count(),
                "total_in_progress": test_runs.filter(
                    status=TEST_RUN_STATUS_CHOICES.IN_PROGRESS,
                ).count(),
            },
        }
        return CustomResponse.success(data=data)


class RunAllTestCasesAPIView(GenericAPIView):
    permission_classes = (HasProjectAccess,)
    serializer_class = TestCaseSerializer

    def get(self, request: Request, project_id: str, test_run_id: str) -> Response:
        """Get all test cases for a given test run."""
        project = get_project_by_id(int(project_id))
        test_run = get_test_run_by_id(int(test_run_id))
        test_suites = (
            get_test_run_by_id(int(test_run_id))
            .test_suites.all()
            .values_list("id", flat=True)
        )
        if project is None or project_id.isdigit() is False:
            return CustomResponse.not_found(message="Project not found.")
        if test_run is None:
            return CustomResponse.not_found(message="TestRun not found.")

        test_cases = TestCases.objects.filter(
            test_suite__id__in=test_suites, completed=False
        )
        return CustomResponse.success(
            message="Success cases found.",
            data=self.get_serializer(test_cases, many=True).data,
        )

    def put(self, request: Request, project_id: str, test_run_id: str) -> Response:
        """Update activity with test run"""
        project = get_project_by_id(int(project_id))
        test_run = get_test_run_by_id(int(test_run_id))
        if project is None or project_id.isdigit() is False:
            return CustomResponse.not_found(message="Project not found.")
        if test_run is None:
            return CustomResponse.not_found(message="TestRun not found.")
        update_activity(
            datetime.datetime.now(),
            request.user,
            project,
            "Run",
            "Test Run",
            test_run.title,
        )
        if (
            len(
                filter_test_cases_by_test_suite(test_run.test_suites.all()).filter(
                    run=False
                )
            )
            > 0
        ):
            test_run.status = TEST_RUN_STATUS_CHOICES.IN_PROGRESS
        else:
            test_run.status = TEST_RUN_STATUS_CHOICES.COMPLETED
        test_run.save()
        return CustomResponse.success(
            message=f"Test run {test_run.title} running successfully.", status_code=201
        )


class SetAssignedUserTestRunAPIView(GenericAPIView):
    permission_classes = (HasProjectAccess,)
    serializer_class = TestRunsSerializer

    def put(self, request: Request, project_id: str, test_run_id: str) -> Response:
        """User this endpoint to set assigned user to test run"""
        assigned_user = request.query_params.get("assigned_user")
        member = get_member_by_id(int(assigned_user))
        project = get_project_by_id(project_id)
        test_run = get_test_run_by_id(test_run_id)
        if not assigned_user:
            return CustomResponse.bad_request(message="Please select a user")
        if not project:
            return CustomResponse.not_found(message="Project not found")
        if not test_run:
            return CustomResponse.not_found(message="Test run not found")
        if not member:
            return CustomResponse.not_found(message="Member not found")
        test_run.assigned_user = member
        test_run.save()
        return CustomResponse.success(
            message=f"Test run {test_run.title} assigned to {member.full_name}",
            data=self.get_serializer(test_run).data,
            status_code=201,
        )


class ReportMonthTestRunAPIView(GenericAPIView):
    """Get all test cases runing based on day"""

    permission_classes = (UserIsAuthenticated,)

    def get(self, request: Request) -> Response:
        """
        This method will return the number of test cases running on days of the month.
        test_run_id => Test run id
        """
        test_run_id = request.query_params.get("run")
        month = request.query_params.get("month")
        test_run = get_test_run_by_id(test_run_id)
        test_suites = test_run.test_suites.all()
        return CustomResponse.success(
            data=month_filter_test_cases_based_on_test_suites(test_suites, month)
        )


class CompleteTestRunAPIView(GenericAPIView):
    """Complete test run after run all test cases."""

    permission_classes = (HasProjectAccess,)

    def put(self, request: Request, project_id: str, test_run_id: str) -> Response:
        """We will use this endpoint to complete the test run after running all test cases"""
        project = get_project_by_id(int(project_id))
        test_run = get_test_run_by_id(int(test_run_id))
        if project is None or project_id.isdigit() is False:
            return CustomResponse.not_found(message="Project not found.")
        if test_run is None:
            return CustomResponse.not_found(message="TestRun not found.")
        update_activity(
            datetime.datetime.now(),
            request.user,
            project,
            "Complete",
            "Test Run",
            test_run.title,
        )
        test_run.status = TEST_RUN_STATUS_CHOICES.COMPLETED
        test_run.save()

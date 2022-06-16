"""Everything related to test runs"""
import datetime
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from server.test_tracker.api.permission import HasProjectAccess
from server.test_tracker.api.response import CustomResponse
from server.test_tracker.models.project import TEST_RUN_STATUS_CHOICES, TestCases, TestRun, TestSuites
from server.test_tracker.serializers.test_run import TestRunsSerializer
from server.test_tracker.services.dashboard import get_project_by_id
from server.test_tracker.services.project import get_test_run_by_id, update_activity





class TestRunAPIView(GenericAPIView):
    """Class TestRunAPIView to handle test runs endpoints"""
    serializer_class = TestRunsSerializer
    permission_classes = (HasProjectAccess,)

    def post(self, request:Request, project_id: str) -> Response:
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            run = serializer.save()
            update_activity(
                datetime.datetime.now(), request.user, run.test_suites.first().project,
                "Create", "Test Run", run.title
            )
            return CustomResponse.success(
                data = serializer.data, status_code=201
            )
        return CustomResponse.bad_request(serializer.errors)
    
    def get(self, request:Request, project_id:str) -> Response:
        """
        This method is used to get all the test runs
        """
        test_runs = TestRun.objects.filter(
            test_suites__project__id = project_id
        ).order_by('-created')
        serializer = self.serializer_class(test_runs, many=True)
        return CustomResponse.success(data=serializer.data)

class TestRunDetailAPIView(GenericAPIView):
    """Class TestRunAPIView to handle test runs endpoints"""
    serializer_class = TestRunsSerializer
    permission_classes = (HasProjectAccess,)
    
    def get(self, request:Request, project_id:str, test_run_id: str) -> Response:
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

    def delete(self, request: Request, project_id:str, test_run_id: str) -> Response:
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
            datetime.datetime.now(), request.user, project,
            "DELETE", "Test Run", test_run.title
        )
        test_run.delete()
        return CustomResponse.success(
            message="Test Run deleted successfully",
            status_code=204
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
        member = params.get('member')
        status = params.get('status')
        if member:
            test_runs = TestRun.objects.filter(
                test_suites__project_id=project_id,
                assigned_user__id=int(member)
            )
        
        if member and status:
            test_runs = TestRun.objects.filter(
                test_suites__project_id=project_id,
                status=status,
                assigned_user__id=int(member)
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
            modified__gte=today - datetime.timedelta(days=7)
        ).values_list('id', flat=True)

        test_suites = TestSuites.objects.filter(
            project_id=project_id,
            run_suites__id__in=test_runs
        ).values_list('id', flat=True)

        test_cases = TestCases.objects.filter(
            test_suite__id__in=test_suites
        )
        data = {
            'not_run':test_cases.filter(run=False).count(),
            'passed':test_cases.filter(run=True, passed=True).count(),
            'failed':test_cases.filter(run=True, passed=False, failed=True).count(),
            'skipped':test_cases.filter(run=True, passed=False, failed=False, skipped=True).count(),
            'not_started_test_runs':{
                'involve_you':test_runs.filter(
                    status=TEST_RUN_STATUS_CHOICES.NOT_STARTED, 
                    assigned_user=request.user
                ).count(),
                'total_not_started':test_runs.filter(
                    status=TEST_RUN_STATUS_CHOICES.NOT_STARTED, 
                ).count()
            },
            'in_progress_test_runs':{
                'involve_you':test_runs.filter(
                    status=TEST_RUN_STATUS_CHOICES.IN_PROGRESS, 
                    assigned_user=request.user
                ).count(),
                'total_in_progress':test_runs.filter(
                    status=TEST_RUN_STATUS_CHOICES.IN_PROGRESS, 
                ).count()
            }
        }
        return CustomResponse.success(data=data)
"""Everything related to test runs"""
import datetime
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from server.test_tracker.api.response import CustomResponse
from server.test_tracker.models.project import TestRun
from server.test_tracker.serializers.test_run import TestRunsSerializer
from server.test_tracker.services.project import get_test_run_by_id, update_activity





class TestRunAPIView(GenericAPIView):
    """Class TestRunAPIView to handle test runs endpoints"""
    serializer_class = TestRunsSerializer

    def post(self, request:Request) -> Response:
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
    
    def get(self, request:Request) -> Response:
        """
        This method is used to get all the test runs
        """
        test_runs = TestRun.objects.all()
        serializer = self.serializer_class(test_runs, many=True)
        return CustomResponse.success(data=serializer.data)

class TestRunDetailAPIView(GenericAPIView):
    """Class TestRunAPIView to handle test runs endpoints"""
    serializer_class = TestRunsSerializer
    
    def get(self, request:Request, test_run_id: str) -> Response:
        """
        This method is used to get all the test runs
        """
        test_runs = get_test_run_by_id(test_run_id)
        if test_runs is None:
            return CustomResponse.not_found(
                message="Test run with id {} not found".format(test_run_id)
            )
        serializer = self.serializer_class(test_runs)
        return CustomResponse.success(data=serializer.data)

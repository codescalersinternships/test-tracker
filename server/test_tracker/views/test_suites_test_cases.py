"""Everything related to test suites and test cases"""

import datetime
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from server.test_tracker.api.response import CustomResponse
from server.test_tracker.serializers.test_suites_test_cases import TestSuitesSerializer
from server.test_tracker.services.dashboard import get_project_by_id
from server.test_tracker.services.project import update_activity
from server.test_tracker.services.test_suites_test_cases import get_test_suite_by_id


class TestSuitesAPIView(GenericAPIView):
    """Create a new test suite"""
    serializer_class = TestSuitesSerializer

    def post(self, request: Request, project_id: str) -> Response:
        """
            Use this endpoint to create a new test suite
        """
        serializer = self.get_serializer(data=request.data)
        project = get_project_by_id(project_id)
        if project is None:
            return CustomResponse.not_found(message="Project not found")
        if serializer.is_valid():
            suite = serializer.save(project=project)
            update_activity(
                datetime.datetime.now(), request.user, project,
                "Create", "Test suite", suite.title
            )
            return CustomResponse.success(
                data=serializer.validated_data,
                message="Test suite created successfully"
            )
        return CustomResponse.bad_request(
            data=serializer.errors,
            message="Test suite not created",
            status_code=201
        )

    def get(self, request: Request, project_id: str) -> Response:
        """Method get to get all of test suites based on the project"""
        project = get_project_by_id(project_id)
        if project is None:
            return CustomResponse.not_found(message="Project not found")
        suites = project.project_test_suites.all()
        serializer = TestSuitesSerializer(suites, many=True)
        return CustomResponse.success(
            message="Success suites found.",
            data=serializer.data
        )


class TestSuitesDetailAPIView(GenericAPIView):
    """Create a new test suite"""
    serializer_class = TestSuitesSerializer

    def put(self, request: Request, test_suite: str) -> Response:
        """
            Use this endpoint to create a new test suite
        """
        test_suite = get_test_suite_by_id(test_suite)
        serializer = self.get_serializer(test_suite, data=request.data)
        if test_suite is None:
            return CustomResponse.not_found(message="Test suite not found")
        if serializer.is_valid():
            suite = serializer.save()
            update_activity(
                datetime.datetime.now(), request.user, suite.project,
                "Update", "Test suite", suite.title
            )
            return CustomResponse.success(
                data=serializer.validated_data,
                message="Test suite Updated successfully"
            )
        return CustomResponse.bad_request(
            data=serializer.errors,
            message="Test suite not created",
            status_code=201
        )

    def get(self, request: Request, test_suite: str) -> Response:
        """Method get to get all of test suites based on the project"""
        test_suite = get_test_suite_by_id(test_suite)
        if test_suite is None:
            return CustomResponse.not_found(message="Test suite not found")
        serializer = TestSuitesSerializer(test_suite)
        return CustomResponse.success(
            message="Success suites found.",
            data=serializer.data
        )

    def delete(self, request: Request, test_suite: str) -> Response:
        """Method get to get all of test suites based on the project"""
        test_suite = get_test_suite_by_id(test_suite)
        if test_suite is None:
            return CustomResponse.not_found(message="Test suite not found")
        update_activity(
            datetime.datetime.now(), request.user, test_suite.project,
            "DELETE", "Test suite", test_suite.title
        )
        return CustomResponse.success(
            message="Test suite deleted successfully",
            status_code=204
        )

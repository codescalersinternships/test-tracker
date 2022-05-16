"""Everything related to test suites"""

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from server.test_tracker.api.response import CustomResponse
from server.test_tracker.serializers.test_cases import GetSingleTestCaseSerializer, TestCaseSerializer
from server.test_tracker.services.project import update_activity
from server.test_tracker.services.requirement import get_requirement_by_id
from server.test_tracker.services.test_cases import get_test_case_by_id
from server.test_tracker.services.test_suites import get_test_suite_by_id

import datetime




class TestCasesAPIView(GenericAPIView):
    """Create a new test suite"""
    serializer_class = TestCaseSerializer

    def post(self, request: Request, test_suite: str, requirement_id: str) -> Response:
        """
            Use this endpoint to create a new test case
        """
        serializer = self.get_serializer(data=request.data)
        test_suite = get_test_suite_by_id(test_suite)
        requirement = get_requirement_by_id(requirement_id)
        if test_suite is None:
            return CustomResponse.not_found(message="Test suite not found")
        if requirement is None:
            return CustomResponse.not_found(message="Requirement suite not found")
        if serializer.is_valid():
            testcase = serializer.save(test_suite=test_suite, verify_requirement=requirement)
            update_activity(
                datetime.datetime.now(), request.user, test_suite.project,
                "Create", "Test Case", testcase.title
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
    
class GetAllTestCasesAPIView(GenericAPIView):
    """Get all of test cases"""
    serializer_class = TestCaseSerializer

    def get(self, request: Request, test_suite: str) -> Response:
        """Method get to get all of test cases based on the test suite"""
        test_suite = get_test_suite_by_id(test_suite)
        if test_suite is None:
            return CustomResponse.not_found(message="Test suite not found")
        suites = test_suite.test_suite_test_cases.all()
        serializer = TestCaseSerializer(suites, many=True)
        return CustomResponse.success(
            message="Success suites found.",
            data=serializer.data
        )


class TestCaseDetailAPIView(GenericAPIView):
    """Create a new test suite"""
    serializer_class = TestCaseSerializer

    def put(self, request: Request, test_case: str) -> Response:
        """
            Use this endpoint to create a new test suite
        """
        test_case = get_test_case_by_id(test_case)
        serializer = self.get_serializer(test_case, data=request.data)
        if test_case is None:
            return CustomResponse.not_found(message="Test Case not found")
        if serializer.is_valid():
            case = serializer.save()
            update_activity(
                datetime.datetime.now(), request.user, test_case.test_suite.project,
                "Update", "Test Case", case.title
            )
            return CustomResponse.success(
                data=serializer.validated_data,
                message="Test Case Updated successfully"
            )
        return CustomResponse.bad_request(
            data=serializer.errors,
            message="Test Case not created",
            status_code=201
        )


    def delete(self, request: Request, test_case: str) -> Response:
        """Method get to get all of test suites based on the project"""
        test_case = get_test_case_by_id(test_case)
        if test_case is None:
            return CustomResponse.not_found(message="Test Case not found")

        update_activity(
            datetime.datetime.now(), request.user, test_case.test_suite.project,
            "DELETE", "Test Case", test_case.title
        )
        test_case.delete()
        return CustomResponse.success(
            message="Test Case deleted successfully",
            status_code=204
        )


class GetSingleTestCaseAPIView(GenericAPIView):
    serializer_class = GetSingleTestCaseSerializer

    def get(self, request: Request, test_case_id: str):
        test_case = get_test_case_by_id(test_case_id)
        if test_case is None:
            return CustomResponse.not_found(message = "TestCase not found")
        return CustomResponse.success(
            message="Test Case found",
            data=self.get_serializer(test_case).data
        )
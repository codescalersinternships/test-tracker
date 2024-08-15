"""Everything related to test suites"""

import datetime
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from test_tracker.api.permission import HasProjectAccess

from test_tracker.api.response import CustomResponse
from test_tracker.models.project import TestSuites
from test_tracker.serializers.test_suites import (
    TestSuitesDetailSerializer,
    TestSuitesSerializer,
)
from test_tracker.services.dashboard import get_project_by_id
from test_tracker.services.project import update_activity
from test_tracker.services.test_plans import filter_test_plans_based_on_project
from test_tracker.services.test_suites import get_test_suite_by_id


class TestSuitesAPIView(GenericAPIView):
    """Create a new test suite"""

    serializer_class = TestSuitesSerializer
    permission_classes = (HasProjectAccess,)

    def post(self, request: Request, project_id: str) -> Response:
        """
        Use this endpoint to create a new test suite
        """
        serializer = self.get_serializer(data=request.data)
        project = get_project_by_id(project_id)
        test_plans = filter_test_plans_based_on_project(project).values_list(
            "id", flat=True
        )
        if project is None:
            return CustomResponse.not_found(message="Project not found")
        if serializer.is_valid():
            if serializer.validated_data.get("test_plan").id not in test_plans:
                return CustomResponse.bad_request(
                    message="Wrong Test Plan, Please Select or Load Another Test Plan For ` {} `".format(
                        project.title
                    )
                )
            suite = serializer.save(project=project)
            update_activity(
                datetime.datetime.now(),
                request.user,
                project,
                "Create",
                "Test suite",
                suite.title,
            )
            return CustomResponse.success(
                data=serializer.data, message="Test suite created successfully"
            )
        return CustomResponse.bad_request(
            data=serializer.errors, message="Test suite not created", status_code=201
        )

    def get(self, request: Request, project_id: str) -> Response:
        """Method get to get all of test suites based on the project"""
        project = get_project_by_id(project_id)
        if project is None:
            return CustomResponse.not_found(message="Project not found")
        suites = project.project_test_suites.all().order_by("-created")
        serializer = TestSuitesSerializer(suites, many=True)
        return CustomResponse.success(
            message="Success suites found.", data=serializer.data
        )


class TestSuitesDetailAPIView(GenericAPIView):
    """Create a new test suite"""

    serializer_class = TestSuitesDetailSerializer
    permission_classes = (HasProjectAccess,)

    def put(self, request: Request, project_id: str, test_suite_id: str) -> Response:
        """
        Use this endpoint to create a new test suite
        """
        test_suite = get_test_suite_by_id(test_suite_id)
        serializer = self.get_serializer(test_suite, data=request.data)
        if test_suite is None:
            return CustomResponse.not_found(message="Test suite not found")
        if serializer.is_valid():
            suite = serializer.save()
            update_activity(
                datetime.datetime.now(),
                request.user,
                suite.project,
                "Update",
                "Test suite",
                suite.title,
            )
            return CustomResponse.success(
                data=serializer.validated_data,
                message="Test suite Updated successfully",
            )
        return CustomResponse.bad_request(
            data=serializer.errors, message="Test suite not created", status_code=201
        )

    def get(self, request: Request, project_id: str, test_suite_id: str) -> Response:
        """Get a test suite based on its id, project id"""
        test_suite = get_test_suite_by_id(test_suite_id)
        if test_suite is None:
            return CustomResponse.not_found(message="Test suite not found")
        serializer = TestSuitesDetailSerializer(test_suite)
        return CustomResponse.success(
            message="Success suites found.", data=serializer.data
        )

    def delete(self, request: Request, project_id: str, test_suite_id: str) -> Response:
        """Delete a test suite based on its id, project id"""
        test_suite = get_test_suite_by_id(test_suite_id)
        if test_suite is None:
            return CustomResponse.not_found(message="Test suite not found")
        update_activity(
            datetime.datetime.now(),
            request.user,
            test_suite.project,
            "Delete",
            "Test suite",
            test_suite.title,
        )
        test_suite.delete()
        return CustomResponse.success(
            message="Test suite deleted successfully", status_code=204
        )


class SearchTestSuiteAPIView(GenericAPIView):
    """
    * Usage
    This class to filter all project test suites that matches the key word.
    """

    serializer_class = TestSuitesSerializer
    permission_classes = (HasProjectAccess,)

    def get(self, request: Request, project_id: str, key_word: str):
        """
        Search on any testsuite that matches this key word.
        """
        project = get_project_by_id(project_id)
        suites = TestSuites.objects.filter(
            title__icontains=key_word, project__id=project.id
        )
        return CustomResponse.success(
            message="Success suites found.",
            data=TestSuitesSerializer(suites, many=True).data,
        )

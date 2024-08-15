"""Everything related to test suites"""

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from django.db.models import Q
from test_tracker.api.permission import HasProjectAccess, UserIsAuthenticated

from test_tracker.api.response import CustomResponse
from test_tracker.models.project import Requirements, TestCases
from test_tracker.serializers.requirement import RequirementsSerializer
from test_tracker.serializers.test_cases import (
    TestCaseSerializer,
    UpdateTestCaseAfterRunSerializer,
)
from test_tracker.services.dashboard import get_project_by_id
from test_tracker.services.member import get_member_by_id
from test_tracker.services.project import update_activity
from test_tracker.services.requirement import get_requirement_by_id
from test_tracker.services.test_cases import get_test_case_by_id
from test_tracker.services.test_suites import get_section_by_id, get_test_suite_by_id

import datetime


class TestCasesAPIView(GenericAPIView):
    """Create a new test suite"""

    serializer_class = TestCaseSerializer
    permission_classes = (UserIsAuthenticated,)

    def post(self, request: Request, test_suite: str) -> Response:
        """
        Use this endpoint to create a new test case
        """
        serializer = self.get_serializer(data=request.data)
        test_suite = get_test_suite_by_id(test_suite)
        if test_suite is None:
            return CustomResponse.not_found(message="Test suite not found")
        if serializer.is_valid():
            tc_id_project = test_suite.project.TC_Title
            if len(tc_id_project) > 0:
                last_title = int(tc_id_project[-1][2:])
            else:
                last_title = 0
            if last_title < 9:
                last_title = "0" + str(last_title + 1)
            else:
                last_title = str(last_title + 1)
            tc_id_project.append(f"TC{last_title}")
            section = None
            if request.query_params.get("section_id"):
                section_id = request.query_params.get("section_id")
                section = get_section_by_id(section_id)
                if section is None:
                    return CustomResponse.not_found(message=f"Cannot find section {section_id}")
            testcase = serializer.save(
                test_suite=test_suite,
                testcase_title=f"TC{last_title}",
                last_saved=request.user,
            )

            if section:
                section.test_cases.add(testcase)
                section.save()

            if request.query_params.get("requirement"):
                requirement = get_requirement_by_id(
                    request.query_params.get("requirement")
                )
                if requirement is None:
                    return CustomResponse.not_found(message="Requirement not found")
                testcase.verify_requirement = requirement
                testcase.save()

            update_activity(
                datetime.datetime.now(),
                request.user,
                test_suite.project,
                "Create",
                "Test Case",
                testcase.title,
            )

            return CustomResponse.success(
                data=serializer.data, message="Test suite created successfully"
            )

        return CustomResponse.bad_request(
            data=serializer.errors, message="Test suite not created", status_code=201
        )


class GetAllTestCasesAPIView(GenericAPIView):
    """Get all of test cases"""

    serializer_class = TestCaseSerializer
    permission_classes = (UserIsAuthenticated,)

    def get(self, request: Request, test_suite: str) -> Response:
        """Method get to get all of test cases based on the test suite"""
        test_suite = get_test_suite_by_id(test_suite)
        if test_suite is None:
            return CustomResponse.not_found(message="Test suite not found")
        suites = test_suite.test_suite_test_cases.all().order_by("-created")
        serializer = TestCaseSerializer(suites, many=True)
        return CustomResponse.success(
            message="Success suites found.", data=serializer.data
        )


class TestCaseDetailAPIView(GenericAPIView):
    """Create a new test suite"""

    serializer_class = TestCaseSerializer
    permission_classes = (UserIsAuthenticated,)

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
                datetime.datetime.now(),
                request.user,
                test_case.test_suite.project,
                "Update",
                "Test Case",
                case.title,
            )
            return CustomResponse.success(
                data=serializer.validated_data, message="Test Case Updated successfully"
            )
        return CustomResponse.bad_request(
            data=serializer.errors, message="Test Case not created", status_code=201
        )

    def delete(self, request: Request, test_case: str) -> Response:
        """Method get to get all of test suites based on the project"""
        test_case = get_test_case_by_id(test_case)
        if test_case is None:
            return CustomResponse.not_found(message="Test Case not found")

        update_activity(
            datetime.datetime.now(),
            request.user,
            test_case.test_suite.project,
            "DELETE",
            "Test Case",
            test_case.title,
        )
        test_case.delete()
        return CustomResponse.success(
            message="Test Case deleted successfully", status_code=204
        )


class GetSingleTestCaseAPIView(GenericAPIView):
    serializer_class = TestCaseSerializer
    permission_classes = (UserIsAuthenticated,)

    def get(self, request: Request, test_case_id: str):
        test_case = get_test_case_by_id(test_case_id)
        if test_case is None:
            return CustomResponse.not_found(message="TestCase not found")
        return CustomResponse.success(
            message="Test Case found", data=self.get_serializer(test_case).data
        )


class SearchTestCaseAPIView(GenericAPIView):
    """
    * Usage
    This class to filter all project testcase that matches the key word.
    """

    serializer_class = TestCaseSerializer
    permission_classes = (HasProjectAccess,)

    def get(self, request: Request, project_id: str, key_word: str):
        """
        Search on any testcase that matches this key word.
        """
        project = get_project_by_id(project_id)
        cases = TestCases.objects.filter(
            Q(title__icontains=key_word, test_suite__project__id=project.id)
            | Q(testcase_title__icontains=key_word, test_suite__project__id=project.id)
        )
        return CustomResponse.success(
            message="Success suites found.",
            data=TestCaseSerializer(cases, many=True).data,
        )


class GetAllProjectRequirementsAPIView(GenericAPIView):
    """Get all of test cases"""

    serializer_class = RequirementsSerializer
    permission_classes = (HasProjectAccess,)

    def get(self, request: Request, project_id: str) -> Response:
        """Method get to get all of test cases based on the test suite"""
        project = get_project_by_id(project_id)
        if project is None:
            return CustomResponse.not_found(message="Project not found")
        requirements = Requirements.objects.filter(
            requirement__project=project
        ).order_by("-created")
        serializer = RequirementsSerializer(requirements, many=True)
        return CustomResponse.success(
            message="Success requirements found.", data=serializer.data
        )


class UpdateTestCaseAfterRunAPIView(GenericAPIView):
    """This class to update the test case by pass bool field"""

    serializer_class = UpdateTestCaseAfterRunSerializer
    permission_classes = (HasProjectAccess,)

    def put(self, request: Request, project_id: str, test_case_id: str) -> Response:
        """Method put to update the test case by pass bool field"""
        project = get_project_by_id(project_id)
        test_case = get_test_case_by_id(test_case_id)
        if project is None:
            return CustomResponse.not_found(message="Project not found")
        if test_case is None:
            return CustomResponse.not_found(message="Test case not found")
        serializer = self.get_serializer(test_case, data=request.data)
        if serializer.is_valid():
            member = get_member_by_id(request.user.id)
            if member is not None:
                serializer.save(last_saved=member)
            else:
                serializer.save()
        return CustomResponse.success(
            message="Test case updated successfully",
            status_code=201,
            data=serializer.data,
        )

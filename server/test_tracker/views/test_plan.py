"""Everything related to the test plan."""
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from test_tracker.api.permission import HasProjectAccess
from test_tracker.api.response import CustomResponse
from test_tracker.models.project import PLAN_CHOICES, TestPlan
from test_tracker.utils.handler import TestPlanHandling
from test_tracker.utils.testplan_temp import TestPlanTemp
from test_tracker.utils.validations import Validator
from test_tracker.services.project import update_activity
from test_tracker.serializers.project import (
    TestPlanDetailSerializer,
    TestPlanSerializer,
    TestPlanTempsSerializer,
    UpdateTestPlanSerializer,
)
from test_tracker.services.dashboard import (
    get_plans_based_on_project,
    get_project_by_id,
)

import datetime


class TestPlansAPIView(GenericAPIView):
    """Create a test plan."""

    serializer_class = TestPlanSerializer
    permission_classes = (HasProjectAccess,)

    def post(self, request: Request, project_id: str) -> Response:
        """
        Use this endpoint to create a new test plan
        You can set temps of null to create a test plan with default temps
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            type = serializer.validated_data.get("type")
            project = get_project_by_id(project_id)
            if project is None:
                return CustomResponse.not_found(message="Project not found")
            title: str = serializer.validated_data.get("title")
            validate_name: str = Validator().validate_string(title)
            if not validate_name:
                return CustomResponse.bad_request(
                    message=f"Name '{title}' is not a valid name, Please choose a valid project name.",
                )
            if type == PLAN_CHOICES.TEMPLATE.value:
                temps = TestPlanTemp.create_temps()
                serializer.save(project=project, temps=temps)
            serializer.save(project=project)
            update_activity(
                datetime.datetime.now(),
                request.user,
                project,
                "Create",
                "Test Plan",
                serializer.data.get("title"),
            )
            return CustomResponse.success(
                data=serializer.data, message="Test plan created successfully"
            )
        return CustomResponse.bad_request(
            data=serializer.errors, message="Test plan not created", status_code=201
        )

    def get(self, request: Request, project_id: str) -> Response:
        """Method get to get all of test plans based on the project"""
        project = get_project_by_id(project_id)
        if project is None:
            return CustomResponse.not_found(message="Project not found")
        plans = get_plans_based_on_project(project).order_by("-created")
        serializer = TestPlanSerializer(plans, many=True)
        return CustomResponse.success(
            message="Success plans found.", data=serializer.data
        )


class TestPlansDetailAPIView(GenericAPIView):
    """This class for [GET, UPDATE, DELETE] test plans methods"""

    serializer_class = TestPlanDetailSerializer
    permission_classes = (HasProjectAccess,)

    def get(self, request: Request, project_id: str, test_plan_id: str) -> Response:
        """Get a test plan from the specified project"""
        test_plan = TestPlanHandling.validate(project_id, test_plan_id)
        if isinstance(test_plan, TestPlan):
            return CustomResponse.success(
                message="Test plan found successfully",
                data=TestPlanDetailSerializer(test_plan).data,
            )
        return test_plan

    def delete(self, request: Request, project_id: str, test_plan_id: str) -> Response:
        """Delete a test plan from the specified project"""
        test_plan = TestPlanHandling.validate(project_id, test_plan_id)
        if isinstance(test_plan, TestPlan):
            update_activity(
                datetime.datetime.now(),
                request.user,
                get_project_by_id(project_id),
                "Delete",
                "Test Plan",
                test_plan.title,
            )
            test_plan.delete()
            return CustomResponse.success(message="DELETED", status_code=204)
        return test_plan


class UpdateTestPlanAPIView(GenericAPIView):
    serializer_class = UpdateTestPlanSerializer
    permission_classes = (HasProjectAccess,)

    def put(self, request: Request, project_id: str, test_plan_id: str) -> Response:
        """Update test plan title"""
        test_plan = TestPlanHandling.validate(project_id, test_plan_id)
        if isinstance(test_plan, TestPlan):
            serializer = self.get_serializer(test_plan, data=request.data)
            if serializer.is_valid():
                serializer.save()
                update_activity(
                    datetime.datetime.now(),
                    request.user,
                    get_project_by_id(project_id),
                    "Update",
                    "Test Plan",
                    test_plan.name,
                )
                return CustomResponse.success(
                    message="Test plan Updated", status_code=200
                )
            return CustomResponse.bad_request(
                errors=serializer.errors,
                message="Test plan not updated",
            )
        return test_plan


class PostNewTestPlanContentAreaAPIView(GenericAPIView):
    """
    * Usage
    Add or update content area to test plan
    """

    serializer_class = TestPlanTempsSerializer
    permission_classes = (HasProjectAccess,)

    def post(self, request: Request, project_id: str, test_plan_id: str) -> Response:
        """Add custom content area to test plan"""
        test_plan = TestPlanHandling.validate(project_id, test_plan_id)
        if isinstance(test_plan, TestPlan):
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                title = serializer.validated_data.get("title")
                content = serializer.validated_data.get("content")
                test_plan.temps.append({"title": title, "content": content})
                test_plan.save()
                update_activity(
                    datetime.datetime.now(),
                    request.user,
                    get_project_by_id(project_id),
                    "Create",
                    f"Test Plan Content Area {test_plan.title} Inside Test Plan",
                    title,
                )
                return CustomResponse.success(
                    message="Successfully added content area to test plan",
                    data=serializer.data,
                    status_code=201,
                )
            return CustomResponse.bad_request(
                error=serializer.errors,
                message="Content area not added",
            )
        return test_plan


class TestPlanContentAreaAPIView(GenericAPIView):
    """
    * Usage
    Delete and get test plan content area based on its title
    """

    permission_classes = (HasProjectAccess,)
    serializer_class = TestPlanTempsSerializer

    def put(
        self, request: Request, project_id: str, test_plan_id: str, title: str
    ) -> Response:
        """
        As we do temps or contents saved in database as a json field so,
            title = the old key to get this obj
            new_content = a json field has a {title and content}
        Update content area with new content area
        """
        test_plan = TestPlanHandling.validate(project_id, test_plan_id)
        if isinstance(test_plan, TestPlan):
            new_title = request.data.get("title")
            content = request.data.get("content")
            if Validator().validate_string(request.data.get("title")):
                update_activity(
                    datetime.datetime.now(),
                    request.user,
                    get_project_by_id(project_id),
                    "Update",
                    f"Test Plan Content Area '{test_plan.temps[title]}' with new title '{new_title} from ' ",
                    test_plan.title,
                )
                if test_plan.temps.get(title):
                    del test_plan.temps[title]
                test_plan.temps[new_title] = content
                test_plan.save()
                return CustomResponse.success(
                    message="Success",
                    data={new_title: content},
                )
            return CustomResponse.bad_request(
                error={"title": new_title},
                message="Title must be a valid title name",
            )
        return test_plan

    def delete(
        self, request: Request, project_id: str, test_plan_id: str, title: str
    ) -> Response:
        """Delete a content area from test plan"""
        test_plan = TestPlanHandling.validate(project_id, test_plan_id)
        if isinstance(test_plan, TestPlan):
            contents = test_plan.temps
            for content in contents:
                if content["title"] == title:
                    contents.remove(content)
                    test_plan.save()
                    update_activity(
                        datetime.datetime.now(),
                        request.user,
                        get_project_by_id(project_id),
                        "Delete",
                        f"Test Plan Content Area {title}",
                        test_plan.title,
                    )
                    return CustomResponse.success(message="DELETED", status_code=204)
        return test_plan

    def get(
        self, request: Request, project_id: str, test_plan_id: str, title: str
    ) -> Response:
        """Get a content area from test plan"""
        test_plan = TestPlanHandling.validate(project_id, test_plan_id)
        response = []
        if isinstance(test_plan, TestPlan):
            contents = test_plan.temps
            for content in contents:
                for _title, value in content.items():
                    if content[_title].lower().find(title.lower()) != -1:
                        response.append({"title": content[_title], "content": value})
            return CustomResponse.success(
                message="Success",
                data=response,
            )
        return test_plan


class SearchTestPlanAPIView(GenericAPIView):
    """
    * Usage
    This class to filter all project test plans that matches the key word.
    """

    serializer_class = TestPlanDetailSerializer
    permission_classes = (HasProjectAccess,)

    def get(self, request: Request, project_id: str, key_word: str):
        """
        Search on any testsuite that matches this key word.
        """
        project = get_project_by_id(project_id)
        if project is None:
            return CustomResponse.not_found(message="Project not found")
        plans = TestPlan.objects.filter(
            title__icontains=key_word, project__id=project.id
        )
        return CustomResponse.success(
            message="Success plans found.",
            data=TestPlanDetailSerializer(plans, many=True).data,
        )

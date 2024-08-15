"""Everything related to the project test suites, test case"""

from django.urls import path

from test_tracker.views.test_cases import (
    GetAllProjectRequirementsAPIView,
    GetAllTestCasesAPIView,
    GetSingleTestCaseAPIView,
    SearchTestCaseAPIView,
    TestCaseDetailAPIView,
    TestCasesAPIView,
    UpdateTestCaseAfterRunAPIView,
)


urlpatterns = [
    path(
        "project/<str:project_id>/requirements/",
        GetAllProjectRequirementsAPIView.as_view(),
    ),
    path(
        "project/<str:project_id>/<str:test_case_id>/run/",
        UpdateTestCaseAfterRunAPIView.as_view(),
    ),
    path("<str:project_id>/search/<str:key_word>/", SearchTestCaseAPIView.as_view()),
    path("test_suite/<str:test_suite>/", GetAllTestCasesAPIView.as_view()),
    path("detail/<str:test_case>/", TestCaseDetailAPIView.as_view()),
    path("<str:test_case_id>/", GetSingleTestCaseAPIView.as_view()),
    path("suites/<str:test_suite>/", TestCasesAPIView.as_view()),
]

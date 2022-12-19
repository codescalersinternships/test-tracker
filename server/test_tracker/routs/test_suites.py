"""Everything related to the project test suites, test case"""

from django.urls import path
from server.test_tracker.views.project import TestSuitesSectionAPIView, GetTestSuitesSectionsAPIView

from server.test_tracker.views.test_suites import (
    SearchTestSuiteAPIView,
    TestSuitesAPIView,
    TestSuitesDetailAPIView,
)


urlpatterns = [
    path("<str:project_id>/section/", TestSuitesSectionAPIView.as_view()),
    path("<str:project_id>/section/<str:test_suite>/", GetTestSuitesSectionsAPIView.as_view()),
    path("<str:project_id>/", TestSuitesAPIView.as_view()),
    path(
        "<str:project_id>/actions/<str:test_suite_id>/",
        TestSuitesDetailAPIView.as_view(),
    ),
    path("<str:project_id>/search/<str:key_word>/", SearchTestSuiteAPIView.as_view()),
]

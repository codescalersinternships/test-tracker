"""Everything related to the project test suites, test case"""

from django.urls import path
from server.test_tracker.views.test_cases import *



urlpatterns = [
    path('test_suite/<str:test_suite>/<str:requirement_id>/', TestCasesAPIView.as_view()),
    path('test_suite/<str:test_suite>/', GetAllTestCasesAPIView.as_view()),
    path('detail/<str:test_case>/', TestCaseDetailAPIView.as_view()),
    path('<str:test_case_id>/', GetSingleTestCaseAPIView.as_view()),
]

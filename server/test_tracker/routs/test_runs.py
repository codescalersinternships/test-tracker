
"""Everything related to the project test case"""

from django.urls import path
from server.test_tracker.views.test_run import *



urlpatterns = [
    path('projects/<str:project_id>/', TestRunAPIView.as_view()),
    path('projects/<str:project_id>/last_week_report/', LastWeekTestRunReportSheetAPIView.as_view()),
    path('projects/<str:project_id>/runs/<str:test_run_id>/', TestRunDetailAPIView.as_view()),
    path('<str:project_id>/search/',SearchOnTestRunAPIView.as_view()),
    path('projects/<str:project_id>/runs/<str:test_run_id>/cases/', RunAllTestCasesAPIView.as_view()),
    path('projects/<str:project_id>/set-user/<str:test_run_id>/', SetAssignedUserTestRunAPIView.as_view()),
]
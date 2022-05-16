
"""Everything related to the project test case"""

from django.urls import path
from server.test_tracker.views.test_run import TestRunAPIView, TestRunDetailAPIView



urlpatterns = [
    path('', TestRunAPIView.as_view()),
    path('<str:test_run_id>/', TestRunDetailAPIView.as_view()),
]

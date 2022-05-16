"""Everything related to the project test suites, test case"""

from django.urls import path
from server.test_tracker.views.test_suites_test_cases import *



urlpatterns = [
    path('<str:project_id>/suites/', TestSuitesAPIView.as_view()),
    path('detail/<str:test_suite>/suites/', TestSuitesDetailAPIView.as_view()),

]

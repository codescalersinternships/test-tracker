"""Everything related to the requirements."""

from django.urls import path
from server.test_tracker.views.requirement import *



urlpatterns = [
    path('projects/<str:project_id>/', ProjectRequirementAPIView.as_view()),
    path('projects/<str:project_id>/get-all/', GetProjectRequirementAPIView.as_view()),
    path('projects/<str:project_id>/update/<str:requirement_id>', UpdateProjectRequirementAPIView.as_view()),
]

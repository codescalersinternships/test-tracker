"""Everything related to the project."""

from django.urls import path
from server.test_tracker.views.project import TestPlansAPIView



urlpatterns = [
    path('projects/<str:project_id>/test_plans/', TestPlansAPIView.as_view()),
]

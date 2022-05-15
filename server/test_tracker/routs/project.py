"""Everything related to the project."""

from django.urls import path
from server.test_tracker.views.project import *



urlpatterns = [
    path('activity/<str:project_id>/', ProjectActivityAPIView.as_view()),
    path('projects/<str:project_id>/', ProjectsDetailAPIView.as_view()),
]

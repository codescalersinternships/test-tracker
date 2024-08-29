"""Here will be any url for the dashboard."""
from django.urls import path

from test_tracker.views.dashboard import (
    GetProfileAPIView,
    GetRequestUserAPIView,
    MemberAPIView,
    MyProjectsAPIView,
    ProjectsAPIView,
)

urlpatterns = [
    path("my-projects/", MyProjectsAPIView.as_view()),
    path("projects/", ProjectsAPIView.as_view()),
    path("members/", MemberAPIView.as_view()),
    path("user/", GetRequestUserAPIView.as_view()),
    path("profile/<str:user_id>/", GetProfileAPIView.as_view()),
]

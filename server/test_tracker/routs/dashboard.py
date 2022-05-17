"""Here will be any url for the dashboard."""
from django.urls import path
from server.test_tracker.views.dashboard import *

urlpatterns = [
    path('total_projects/', GetTotalProjectsAPIView.as_view()),
    path('projects/', ProjectsAPIView.as_view()),
    path('members/', MemberAPIView.as_view()),

    path('profile/', UpdateProfileAPIView.as_view()),
    path('profile/<str:user_id>/', GetProfileAPIView.as_view()),
]

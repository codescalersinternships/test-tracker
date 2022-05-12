"""Here will be any url for the dashboard."""
from django.urls import path
from server.test_tracker.views.dashboard import *


urlpatterns = [
    path('projects/', ProjectsAPIView.as_view()),
    path('projects/<str:project_id>/', ProjectsDetailAPIView.as_view()),

    path('people/', PeopleAPIView.as_view()),
]

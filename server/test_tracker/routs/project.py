"""Everything related to the project."""

from django.urls import path
from server.test_tracker.views.project import *



urlpatterns = [
    path('<str:project_id>/account-members-not-in-project-members/', AccountMembersNotInProjectAPIView.as_view()),
    path('<str:project_id>/members/<str:member_id>/', AddMemberToProjectAPIView.as_view()),
    path('last-5-projects/', GetLast5ProjectsUpdatedAPIView.as_view()),
    path('last-5-projects/activity/', GetActivityOfLast5ProjectsAPIView.as_view()),
    path('activity/<str:project_id>/', ProjectActivityAPIView.as_view()),
    path('<str:project_id>/', ProjectsDetailAPIView.as_view()),
    path('search/<str:project_name>/', SearchProjectAPIView.as_view()),
]

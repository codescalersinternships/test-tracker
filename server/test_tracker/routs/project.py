"""Everything related to the project."""

from django.urls import path

from test_tracker.views.project import (
    AccountMembersNotInProjectAPIView,
    AddMemberToProjectAPIView,
    GetRecentProjectsActivityAPIView,
    GetRecentProjectsUpdatedAPIView,
    ProjectActivityAPIView,
    ProjectsDetailAPIView,
    SearchProjectAPIView,
)


urlpatterns = [
    path(
        "<str:project_id>/account-members-not-in-project-members/",
        AccountMembersNotInProjectAPIView.as_view(),
    ),
    path(
        "<str:project_id>/members/<str:member_id>/", AddMemberToProjectAPIView.as_view()
    ),
    path("recent/", GetRecentProjectsUpdatedAPIView.as_view()),
    path("recent/activity/", GetRecentProjectsActivityAPIView.as_view()),
    path("activity/<str:project_id>/", ProjectActivityAPIView.as_view()),
    path("<str:project_id>/", ProjectsDetailAPIView.as_view()),
    path("search/<str:project_name>/", SearchProjectAPIView.as_view()),
]

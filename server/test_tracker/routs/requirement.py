"""Everything related to the requirements."""

from django.urls import path

from test_tracker.views.requirement import (
    GetAllRequirementDocsAPIView,
    PostNewRequirementDocsAPIView,
    RequirementAPIView,
    RequirementDocsDetailsAPIView,
    RequirementsDetailAPIView,
    SearchRequirementDocssAPIView,
    SearchRequirementsInRequirementDocssAPIView,
)


urlpatterns = [
    path("projects/<str:project_id>/get-all/", GetAllRequirementDocsAPIView.as_view()),
    path(
        "projects/<str:project_id>/search/<str:key_word>/",
        SearchRequirementDocssAPIView.as_view(),
    ),
    path(
        "projects/<str:project_id>/search/requirements/<str:key_word>/",
        SearchRequirementsInRequirementDocssAPIView.as_view(),
    ),
    path(
        "projects/<str:project_id>/details/<str:requirement_id>/",
        RequirementDocsDetailsAPIView.as_view(),
    ),
    path("<str:project_id>/", PostNewRequirementDocsAPIView.as_view()),
    path(
        "projects/<str:project_id>/requirement/<str:requirements_id>/",
        RequirementAPIView.as_view(),
    ),
    path(
        "projects/<str:project_id>/<str:project_requirement_id>/<str:requirement_id>/",
        RequirementsDetailAPIView.as_view(),
    ),
]

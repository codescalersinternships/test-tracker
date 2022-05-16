"""Everything related to the requirements."""

from django.urls import path
from server.test_tracker.views.requirement import *



urlpatterns = [
    path('projects/<str:project_id>/', ProjectRequirementsAPIView.as_view()),
    path('projects/<str:project_id>/get-all/', GetProjectRequirementsAPIView.as_view()),
    path('projects/<str:project_id>/update/<str:requirement_id>/', UpdateProjectRequirementsAPIView.as_view()),

    path('<str:requirements_id>/', RequirementAPIView.as_view()),
    path('detail/<str:requirement_id>/', RequirementsDetailAPIView.as_view()),
]

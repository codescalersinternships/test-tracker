"""Everything related to the requirements."""

from django.urls import path
from server.test_tracker.views.requirement import *



urlpatterns = [
    path('projects/<str:project_id>/get-all/', GetAllRequirementDocssAPIView.as_view()),
    path('projects/<str:project_id>/search/<str:key_word>/', SearchRequirementDocssAPIView.as_view()),
    path('projects/<str:project_id>/search/requirements/<str:key_word>/', SearchRequirementsInRequirementDocssAPIView.as_view()),
    path('projects/<str:project_id>/details/<str:requirement_id>/', 
        RequirementDocssDetailsAPIView.as_view()
    ),

    path('projects/<str:project_id>/post/', PostNewRequirementDocssAPIView.as_view()),

    path('<str:requirements_id>/', RequirementAPIView.as_view()),
    path('projects/<str:project_id>/<str:project_requirement_id>/<str:requirement_id>/', 
        RequirementsDetailAPIView.as_view()
    ),
]

"""Everything related to the project."""

from django.urls import path
from server.test_tracker.views.project import *



urlpatterns = [
    path('<str:project_id>/test_plans/', TestPlansAPIView.as_view()),
    path(
        '<str:project_id>/test_plans/<str:test_plan_id>/',
        TestPlansDetailAPIView.as_view()
    ),
    path(
        '<str:project_id>/test_plans/<str:test_plan_id>/temps/',
        AddOrUpdateTempsAPIView.as_view()
    ),
    path(
        '<str:project_id>/test_plans/<str:test_plan_id>/temps/<str:title>/',
        DeleteContentAreaAPIView.as_view()
    ),
]

"""Everything related to the project."""

from django.urls import path
from server.test_tracker.views.test_plan import *



urlpatterns = [
    path('<str:project_id>/', TestPlansAPIView.as_view()),
    path(
        '<str:project_id>/actions/<str:test_plan_id>/',
        TestPlansDetailAPIView.as_view()
    ),
    path(
        '<str:project_id>/<str:test_plan_id>/update/',
        UpdateTestPlanAPIView.as_view()
    ),
    path(
        '<str:project_id>/<str:test_plan_id>/temps/',
        PostNewTestPlanContentAreaAPIView.as_view()
    ),
    path(
        '<str:project_id>/<str:test_plan_id>/temps/<str:title>/',
        TestPlanContentAreaAPIView.as_view()
    ),
    path(
        '<str:project_id>/search/<str:key_word>/',
        SearchTestPlanAPIView.as_view()
    ),
]

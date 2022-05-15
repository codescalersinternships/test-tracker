"""Here will be any url for the dashboard."""
from django.urls import path
from server.test_tracker.views.dashboard import *

urlpatterns = [
    path('all/', GetPersonApiView.as_view()),
    path('full_access/', FULLACCESSPermissionAPIView.as_view()),
    path('admin_access/', ADMINACCESSPermissionAPIView.as_view()),
    path('<str:person_email>/', PeopleDetailAPIView.as_view()),
]

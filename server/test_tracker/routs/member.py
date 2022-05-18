"""Here will be any url for the dashboard."""
from django.urls import path
from server.test_tracker.views.member import *

urlpatterns = [
    path('all/', GetMemberApiView.as_view()),
    path('search/<search_input>/', SearchMemberAPIView.as_view()),
    path('set_password/', MemberSetPasswordAPIView.as_view()), # When we use query_params we need to remove last slash
    path('full_access/', FULLACCESSPermissionAPIView.as_view()),
    path('admin_access/', ADMINACCESSPermissionAPIView.as_view()),
    path('<str:member_email>/', MemberDetailAPIView.as_view()),
]

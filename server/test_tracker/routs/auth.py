from django.urls import path
from server.test_tracker.views.auth import *


urlpatterns = [
    path('users/<str:email>/', GetUserAPIView.as_view()),
    path('signup/', RegisterAPIView.as_view()),
    path('login/', LoginByTokenAPIView.as_view()),
    path('token/refresh/', MyTokenRefreshView.as_view()),
    path('invitation/', DecodeAndVerifySignatureAPIView.as_view()),
]
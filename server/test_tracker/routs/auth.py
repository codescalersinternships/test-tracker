from django.urls import path

from server.test_tracker.views.auth import (
    DecodeAndVerifySignatureAPIView,
    GetUserAPIView,
    LoginByTokenAPIView,
    MyTokenRefreshView,
    RegisterAPIView,
    UpdateUserSettingsAPIView,
    GetHubAccessTokenAPIView,
    GetHubUserDataAPIView
)


urlpatterns = [
    path("users/<str:email>/", GetUserAPIView.as_view()),
    path("signup/", RegisterAPIView.as_view()),
    path("login/", LoginByTokenAPIView.as_view()),
    path("token/refresh/", MyTokenRefreshView.as_view()),
    path("invitation/", DecodeAndVerifySignatureAPIView.as_view()),
    path("settings/", UpdateUserSettingsAPIView.as_view()),
    path("github/access_token/", GetHubAccessTokenAPIView.as_view()),
    path("github/user/", GetHubUserDataAPIView.as_view()),
]

from django.urls import path
from server.test_tracker.utils.auth import MyTokenRefreshView
from server.test_tracker.views.auth import *


urlpatterns = [
    path('signup/', RegisterAPIView.as_view()),
    path('login/', LoginByTokenAPIView.as_view()),
    path('token/refresh/', MyTokenRefreshView.as_view()),
    
]
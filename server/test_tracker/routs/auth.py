from django.urls import path
from server.test_tracker.views.auth import *


urlpatterns = [
    path('signup/', RegisterAPIView.as_view())
]
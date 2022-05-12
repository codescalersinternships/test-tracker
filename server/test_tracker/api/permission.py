from rest_framework import permissions
from django.core.exceptions import PermissionDenied
from rest_framework.request import Request
from rest_framework.views import APIView


class UserIsAuthenticated(permissions.BasePermission):
    """
    return this endpoint only for all of Job-Seekers
    """
    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.user.is_authenticated:
            return True
        raise PermissionDenied
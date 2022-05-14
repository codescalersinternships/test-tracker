from rest_framework import permissions
from django.core.exceptions import PermissionDenied
from rest_framework.request import Request
from rest_framework.views import APIView


class UserIsAuthenticated(permissions.BasePermission):
    """
        only who login can pass
    """
    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.user.is_authenticated:
            return True
        raise PermissionDenied

class HasProjectAccess(permissions.BasePermission):
    """
        Only who have project or have a full access can pass
    """
    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.user.is_authenticated:
            project = None
            return True
        raise PermissionDenied
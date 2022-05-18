from rest_framework import permissions
from django.core.exceptions import PermissionDenied
from rest_framework.request import Request
from rest_framework.views import APIView

from server.test_tracker.models.dashboard import Project
from server.test_tracker.services.member import get_member_by_id


class UserIsAuthenticated(permissions.BasePermission):
    """
        only who login can pass
    """
    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.user.is_authenticated:
            return True
        raise PermissionDenied

class IsHost(permissions.BasePermission):
    """
        Only host user can use
    """
    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.user.is_authenticated:
            member = get_member_by_id(request.user.id)
            if member == None:
                return True
            raise PermissionDenied
        raise PermissionDenied

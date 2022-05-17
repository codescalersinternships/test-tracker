from rest_framework import permissions
from django.core.exceptions import PermissionDenied
from rest_framework.request import Request
from rest_framework.views import APIView

from server.test_tracker.models.dashboard import Project


class UserIsAuthenticated(permissions.BasePermission):
    """
        only who login can pass
    """
    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.user.is_authenticated:
            return True
        raise PermissionDenied

class HasAccess(permissions.BasePermission):
    """
        Only who have project or have a full access can pass
    """
    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.user.is_authenticated:
            projects = Project.objects.filter(user=request.user)
            
        #     from server.test_tracker.models.dashboard import People
        # print(project.user)
        # print(People.objects.filter(host_user=project.user).u)
from rest_framework import permissions
from django.core.exceptions import PermissionDenied
from rest_framework.request import Request
from rest_framework.views import APIView

from test_tracker.services.dashboard import get_project_by_id
from test_tracker.services.member import get_member_by_id


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
            if member is None:
                return True
            raise PermissionDenied
        raise PermissionDenied


class HasProjectAccess(permissions.BasePermission):
    """If request.user is a host or a member of the project can access"""

    def has_permission(
        self,
        request: Request,
        view: APIView,
    ) -> bool:
        if request.user.is_authenticated:
            if view.get_renderer_context().get("kwargs").get("project_id"):
                project_id = view.get_renderer_context().get("kwargs").get("project_id")
                if not project_id.isdigit():
                    raise PermissionDenied
                project = get_project_by_id(project_id)
                if project is not None:
                    if request.user.id == project.user.id:
                        return True
                    elif request.user.id in project.members.values_list(
                        "id", flat=True
                    ):
                        return True
                    raise PermissionDenied
                raise PermissionDenied
            raise PermissionDenied
        raise PermissionDenied

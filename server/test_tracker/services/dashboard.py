from typing import Dict
from uuid import UUID
from server.test_tracker.models.dashboard import PERMISSION_CHOICES, Member, Project
from server.test_tracker.models.project import TestPlan
from server.test_tracker.models.users import User
from server.test_tracker.services.member import get_member_by_id




def get_project_by_id(project_id: str) -> Project or None:
    """A service method to return a single project based on its id"""
    if not project_id.isdigit():
        return None
    try:
        return Project.objects.get(id=int(project_id))
    except Project.DoesNotExist:
        return None

def get_project_by_user(user: User) -> Project or None:
    """Returns the project based on the user"""
    projects = Project.objects.filter(members__id__in=[user.id])
    if len(projects) > 0:
        return projects
    else:
        projects = Project.objects.filter(user=user)
        return projects

def get_project_by_user_id(user_id: int) -> Project or None:
    """Returns the project based on the user id"""
    return Project.objects.filter(user_id=user_id)

def find_project_name_based_on_user(user: User, project_name: str) -> bool:
    """Get the project name based on the user"""
    try:
        Project.objects.get(user=user, name=project_name)
        return False
    except Project.DoesNotExist:
        return True

def get_member_based_on_user(user: User) -> Member:
    """Return all of Member based on the request user"""
    return Member.objects.filter(host_user=user)

def get_member_by_user_and_member_email(user: User, member_email: str) -> Member or None:
    """Return a single member based on the user and member email"""
    try:
        return Member.objects.get(host_user=user, email=str(member_email))
    except Member.DoesNotExist:
        return None

def get_full_access_permission_based_on_user(user: User) -> Member or None:
    """Returns the full permission based on the user"""
    return Member.objects.filter(host_user=user, permission=PERMISSION_CHOICES.FULL_ACCESS)

def get_admin_access_permission_based_on_user(user: User) -> Member or None:
    """Returns the full permission based on the user"""
    return Member.objects.filter(host_user=user, permission=PERMISSION_CHOICES.ADMIN_ACCESS)

def get_signature(signature: UUID) -> Member:
    """Try to return user data based on invitation signature"""
    try:
        return Member.objects.get(signature=signature)
    except Member.DoesNotExist:
        return None

def get_member_based_on_signature(signature: UUID):
    """Try to return Member based on signature"""
    try:
        return Member.objects.get(
            signature = signature
        )
    except Member.DoesNotExist:
        return None

def get_plans_based_on_project(project: Project) -> TestPlan:
    """Return all of test plans based on project"""
    return TestPlan.objects.filter(project=project)

def get_total_projects(user: User or Member) -> Dict or int:
    """Get total of projects based on user type"""
    total = None
    data = {}
    total = Project.objects.filter(members__id__in=[user.id]).count()
    if total > 0:
        user = get_member_by_id(str(user.id))
    else:
        total = Project.objects.filter(user=user).count()

    if total != 0:
        if hasattr(user, 'permission'):
            data['type'] = "member"
        else:
            data['type'] = "admin"
        data['total_projects'] = total
    return data
from typing import Dict
from uuid import UUID

from test_tracker.models.dashboard import PERMISSION_CHOICES, Member, Project
from test_tracker.models.project import TestPlan
from test_tracker.models.users import User
from test_tracker.services.member import get_member_by_id


def get_project_by_id(project_id: str) -> Project or None:
    """A service method to return a single project based on its id"""
    try:
        return Project.objects.get(id=int(project_id))
    except Project.DoesNotExist:
        return None


def get_projects_by_user(user: User or Member) -> Project or None:
    """Returns the project based on the user"""
    member = get_member_by_id(user.id)
    if member is not None:
        projects = Project.objects.filter(user=member.host_user, members__in=[member])
    else:
        projects = Project.objects.filter(user=user)
    return projects

def get_project_by_user_id(user_id: int) -> Project or None:
    """Returns the project based on the user id"""
    return Project.objects.filter(user_id=user_id)


def is_success_project(user: User, project: Project, new_title: str) -> bool:
    """Try to search if there are project have the same title"""
    projects = Project.objects.filter(user=user, title=new_title)
    if projects.count() == 1 and projects[0].id == project.id or projects.count() == 0:
        return True
    return False


def user_has_same_project_title(user: User, title: str):
    """Check if user has same project name"""
    try:
        Project.objects.get(user=user, title=title)
        return True
    except Project.DoesNotExist:
        return False


def get_member_based_on_user(user: User) -> Member:
    """Return all of Member based on the request user"""
    return Member.objects.filter(host_user=user)


def get_member_by_user_and_member_email(
    user: User, member_email: str
) -> Member or None:
    """Return a single member based on the user and member email"""
    try:
        return Member.objects.get(host_user=user, email=str(member_email))
    except Member.DoesNotExist:
        return None


def get_full_access_permission_based_on_user(user: User) -> Member or None:
    """Returns the full permission based on the user"""
    return Member.objects.filter(
        host_user=user, permission=PERMISSION_CHOICES.FULL_ACCESS
    )


def get_admin_access_permission_based_on_user(user: User) -> Member or None:
    """Returns the full permission based on the user"""
    return Member.objects.filter(
        host_user=user, permission=PERMISSION_CHOICES.ADMIN_ACCESS
    )


def get_signature(signature: UUID) -> Member:
    """Try to return user data based on invitation signature"""
    try:
        return Member.objects.get(signature=signature)
    except Member.DoesNotExist:
        return None


def get_member_based_on_signature(signature: UUID):
    """Try to return Member based on signature"""
    try:
        return Member.objects.get(signature=signature)
    except Member.DoesNotExist:
        return None


def get_plans_based_on_project(project: Project) -> TestPlan:
    """Return all of test plans based on project"""
    return TestPlan.objects.filter(project=project)


def my_projects(user: User or Member) -> Dict or int:
    """Get total of projects based on user type"""
    try:
        member = Member.objects.get(id=user.id)
        user = member.host_user
        projects = Project.objects.filter(members__in=[member], user=user)
    except Member.DoesNotExist:
        projects = Project.objects.filter(user=user)

    return projects

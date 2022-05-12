from server.test_tracker.models.dashboard import PERMISSION_CHOICES, People, Project
from server.test_tracker.models.users import User




def get_project_by_id(project_id: str) -> Project or None:
    """A service method to return a single project based on its id"""
    if not project_id.isdigit():
        return None
    try:
        return Project.objects.get(id=int(project_id))
    except Project.DoesNotExist:
        return None


def find_project_name_based_on_user(user: User, project_name: str):
    """Get the project name based on the user"""
    try:
        Project.objects.get(user=user, name=project_name)
        return False
    except Project.DoesNotExist:
        return True

def get_people_based_on_user(user: User) -> People:
    """Return all of people based on the request user"""
    return People.objects.filter(user=user)

def get_person_by_user_and_person_email(user: User, person_email: str) -> People or None:
    """Return a single person based on the user and person email"""
    try:
        return People.objects.get(user=user, email=person_email)
    except People.DoesNotExist:
        return None

def get_full_access_permission_based_on_user(user: User) -> People or None:
    """Returns the full permission based on the user"""
    return People.objects.filter(user=user, permission=PERMISSION_CHOICES.FULL_ACCESS)

def get_admin_access_permission_based_on_user(user: User) -> People or None:
    """Returns the full permission based on the user"""
    return People.objects.filter(user=user, permission=PERMISSION_CHOICES.ADMIN_ACCESS)
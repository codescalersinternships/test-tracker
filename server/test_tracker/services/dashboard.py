from server.test_tracker.models.dashboard import People, Project
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
    try:
        return People.objects.filter(user=user)
    except:
        return None
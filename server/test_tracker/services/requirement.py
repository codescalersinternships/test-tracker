"""Everything related to the project requirements"""

from server.test_tracker.models.dashboard import Project
from server.test_tracker.models.project import ProjectRequirement, Requirements

from typing import List



def filter_requirements_by_project(project : Project) -> List[ProjectRequirement]:
    """
    This method gets all Project requirements
    """
    return ProjectRequirement.objects.filter(project=project)

def get_requirements_by_id(requirements_id : str) -> ProjectRequirement:
    """
    This method gets all Project requirements
    """
    if not requirements_id.isdigit():
        return None
    try:
        return ProjectRequirement.objects.get(id=int(requirements_id))
    except:
        return None

def get_requirement_by_id(requirement_id : str) -> Requirements:
    """
    This method gets Requirements based on Project requirements
    """
    if not requirement_id.isdigit():
        return None
    try:
        return Requirements.objects.get(id=int(requirement_id))
    except:
        return None

def filter_requirements_based_on_project_requirement(requirement : ProjectRequirement) -> Requirements:
    """
    This method gets Requirements based on Project requirements
    """
    return Requirements.objects.filter(requirement=requirement)
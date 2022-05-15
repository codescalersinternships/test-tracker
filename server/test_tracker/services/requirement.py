"""Everything related to the project requirements"""

from server.test_tracker.models.dashboard import Project
from server.test_tracker.models.project import Requirements

from typing import List



def get_requirements_by_project(project : Project) -> List[Requirements]:
    """
    This method gets all requirements for a project
    """
    return Requirements.objects.filter(project=project)

def get_requirement_by_id(id : int) -> Requirements:
    """
    This method gets all requirements for a project
    """
    try:
        return Requirements.objects.get(id=id)
    except:
        return None
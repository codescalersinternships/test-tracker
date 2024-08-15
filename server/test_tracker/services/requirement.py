"""Everything related to the project requirements"""

from test_tracker.models.dashboard import Project
from test_tracker.models.project import RequirementDocs, Requirements

from typing import List


def filter_requirements_by_project(project: Project) -> List[RequirementDocs]:
    """
    This method gets all Project requirements
    """
    return RequirementDocs.objects.filter(project=project)


def get_project_requirement_by_id(requirements_id: str) -> RequirementDocs:
    """
    This method gets all Project requirements
    """
    if not requirements_id.isdigit():
        return None
    try:
        return RequirementDocs.objects.get(id=int(requirements_id))
    except RequirementDocs.DoesNotExist:
        return None


def get_requirement_doc_by_id(requirement_id: str) -> Requirements:
    """
    This method gets Requirements based on Project requirements
    """
    if not requirement_id.isdigit():
        return None
    try:
        return RequirementDocs.objects.get(id=int(requirement_id))
    except RequirementDocs.DoesNotExist:
        return None


def filter_requirements_based_on_project_requirement(
    requirement: RequirementDocs,
) -> Requirements:
    """
    This method gets Requirements based on Project requirements
    """
    return Requirements.objects.filter(requirement=requirement).order_by("-created")


def get_requirement_by_id(requirement_id: str) -> Requirements:
    """
    This method gets Requirements based on id
    """
    if not requirement_id.isdigit():
        return None
    try:
        return Requirements.objects.get(id=int(requirement_id))
    except Requirements.DoesNotExist:
        return None

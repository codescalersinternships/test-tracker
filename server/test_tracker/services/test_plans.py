"""All methods related to test plans"""

from server.test_tracker.models.dashboard import Project
from server.test_tracker.models.project import TestPlan


def filter_test_plans_based_on_project(project: Project) -> TestPlan:
    """Return all of test plans based on the project"""
    return TestPlan.objects.filter(project=project)
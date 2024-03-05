"""Everything related to the project."""


from datetime import datetime
from test_tracker.api.response import CustomResponse
from test_tracker.models.dashboard import Member, Project
from test_tracker.models.project import TestPlan, TestRun
from test_tracker.models.users import User


def get_test_plan_by_id(test_plan_id: str):
    if not test_plan_id.isdigit():
        return None
    try:
        return TestPlan.objects.get(id=int(test_plan_id))
    except TestPlan.DoesNotExist:
        return None


def update_activity(
    date_time: datetime, user: User, project: Project, event: str, on: str, name: str
):
    """
    This method to update the activity of a project,
    DateTime: Date and time of the activity
    User: Who user make this activity
    Project: Who project
    Event: What is the event e.g. ['updated', 'created', 'delete']
    ON: Name of the object
    """

    date_time = str(date_time.date())

    last_id = [id for id in project.activity.keys()]

    if len(last_id) == 0:
        last_id = 0
    else:
        last_id = last_id[-1]
    project.activity[int(last_id) + 1] = {
        "action": f"{user.full_name} {event} {on} '{name}'",
        "date": date_time,
    }

    return project.save()


def get_test_run_by_id(test_run_id: str):
    """Try to return a test run based on its id."""
    try:
        return TestRun.objects.get(id=int(test_run_id))
    except TestRun.DoesNotExist:
        return None


def project_member_validation(
    project: Project, member: Member, user: User, remove=False
):
    """Validate if the user is a member of the project."""
    if project is None:
        return CustomResponse.not_found(message="Project not found")
    if user != project.user:
        return CustomResponse.unauthorized()
    if member is None:
        return CustomResponse.not_found(message="Member not found")
    if not remove and member in project.members.all():
        return CustomResponse.bad_request(message="Member already in project")
    return True

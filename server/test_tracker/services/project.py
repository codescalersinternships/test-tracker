"""Everything related to the project."""


from datetime import datetime
from server.test_tracker.models.dashboard import Project
from server.test_tracker.models.project import TestPlan
from server.test_tracker.models.users import User


def get_test_plan_by_id(test_plan_id :str):
    if not test_plan_id.isdigit():
        return None
    try:
        return TestPlan.objects.get(id = int(test_plan_id))
    except TestPlan.DoesNotExist:
        return None

def update_activity(
    date_time: datetime, user: User,
    project: Project, event: str, on: str,
    name: str):
    """
        This method to update the activity of a project,
        DateTime: Date and time of the activity
        User: Who user make this activity
        Project: Who project
        Event: What is the event e.g. ['updated', 'created', 'delete']
        ON: Name of the object
    """
    if date_time.date() == datetime.today().date():
        date_time = "Today"
    else:
        date_time = str(datetime.date())
    last_id = [id for id in project.activity.keys()][-1]
    project.activity[int(last_id) +1] = {
        "action": f"{user.full_name} {event} {on} '{name}'",
        "date" : date_time
    }

    return project.save()
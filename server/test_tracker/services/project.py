"""Everything related to the project."""


from server.test_tracker.models.project import TestPlan


def get_test_plan_by_id(test_plan_id :str):
    if not test_plan_id.isdigit():
        return None
    try:
        return TestPlan.objects.get(id = int(test_plan_id))
    except TestPlan.DoesNotExist:
        return None
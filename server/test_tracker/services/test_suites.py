"""Everything related to test suites"""



from server.test_tracker.models.project import TestSuites


def get_test_suite_by_id(test_suite_id: str) -> TestSuites:
    """
        Use this endpoint to get a test suite by id
    """
    if not test_suite_id.isdigit():
        return None
    try:
        return TestSuites.objects.get(id=test_suite_id)
    except TestSuites.DoesNotExist:
        return None

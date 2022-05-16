"""Everything related to the test case"""



from server.test_tracker.models.project import TestCases


def get_test_case_by_id(test_case: str) -> TestCases:
    """Method to get the test case obj"""
    if not test_case.isdigit():
        return None
    try:
        return TestCases.objects.get(id=int(test_case))
    except:
        return None
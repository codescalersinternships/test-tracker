"""Everything related to the test case"""



from server.test_tracker.models.project import TestCases, TestSuites


def get_test_case_by_id(test_case: str) -> TestCases:
    """Method to get the test case obj"""
    if not test_case.isdigit():
        return None
    try:
        return TestCases.objects.get(id=int(test_case))
    except:
        return None

def get_test_cases_based_on_test_suites(test_suites: TestSuites) -> TestCases:
    """Receive a list of test cases and return a list of TestCases"""
    test_suites = test_suites.values_list('id', flat=True)
    test_cases = TestCases.objects.filter(test_suite__id__in=test_suites)
    return test_cases
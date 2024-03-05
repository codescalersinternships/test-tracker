"""Everything related to the test case"""
from test_tracker.models.project import TestCases, TestSuites


def get_test_case_by_id(test_case: str) -> TestCases:
    """Method to get the test case obj"""
    if not test_case.isdigit():
        return None
    try:
        return TestCases.objects.get(id=int(test_case))
    except TestCases.DoesNotExist:
        return None


def get_test_case_type(test_case: TestCases) -> str:
    """Method to get the test case type"""
    type = ""
    if test_case.passed:
        type = "passed"
    elif test_case.failed:
        type = "failed"
    elif test_case.skipped:
        type = "skipped"
    elif test_case.run:
        type = "run"
    return type if type != "" else None


def month_filter_test_cases_based_on_test_suites(
    test_suites: TestSuites, month: str
) -> TestCases:
    """Receive a list of test cases and return a list of TestCases"""
    test_suites = test_suites.values_list("id", flat=True)
    test_cases = TestCases.objects.filter(
        test_suite__id__in=list(test_suites),
        modified__month__gte=month,
    )
    passed = test_cases.filter(passed=True)
    failed = test_cases.filter(failed=True)
    skipped = test_cases.filter(skipped=True)

    response = {}
    for case in test_cases:
        case_type = get_test_case_type(case)
        if case_type is not None:
            response[case.modified.day] = {
                "total": len(
                    test_cases.filter(modified__day__gte=case.modified.day, run=True)
                ),
                "passed": len(
                    passed.filter(modified__day__gte=case.modified.day, run=True)
                ),
                "failed": len(
                    failed.filter(modified__day__gte=case.modified.day, run=True)
                ),
                "skipped": len(
                    skipped.filter(modified__day__gte=case.modified.day, run=True)
                ),
            }
    return response


def filter_test_cases_by_test_suite(test_suites: TestCases):
    """Recive test suites query_set and return test cases query_set"""
    test_cases = TestCases.objects.filter(test_suite__in=test_suites)
    return test_cases

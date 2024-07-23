"""Everything related to test suites"""
from test_tracker.models.project import TestSuites, TestSuitesSection


def get_test_suite_by_id(test_suite_id: str) -> TestSuites:
    """
    Use this endpoint to get a test suite by id
    """
    if not test_suite_id.isdigit():
        return None
    try:
        return TestSuites.objects.get(id=int(test_suite_id))
    except TestSuites.DoesNotExist:
        return None

def filter_sections_based_on_test_suite(test_suite: TestSuites) -> TestSuitesSection:
    """Filter sections based on test suite obj"""
    return TestSuitesSection.objects.filter(test_suites=test_suite)

def get_section_by_id(section_id: str) -> TestSuitesSection:
    """Get test suite section by id"""
    if not section_id.isdigit():
        return None
    try:
        return TestSuitesSection.objects.get(id=int(section_id))
    except TestSuites.DoesNotExist:
        return None
"""Everything related to TestSuites"""


from server.test_tracker.models.project import TestCases, TestSuites
from rest_framework.serializers import ModelSerializer, SerializerMethodField

class TestSuitesSerializer(ModelSerializer):
    """class TestSuitesSerializer to serialize the test suite obj"""
    created = SerializerMethodField()
    modified = SerializerMethodField()
    number_of_test_cases = SerializerMethodField()

    class Meta:
        model = TestSuites
        exclude = ('project',)

    def get_created(self, obj):
        """Method to get the created date"""
        return obj.created.date()
    
    def get_modified(self, obj):
        """Method to get the modified date"""
        return obj.modified.date()
    
    def get_number_of_test_cases(self, obj):
        """Method to get the number of test cases"""
        return TestCases.objects.filter(test_suite=obj).count()
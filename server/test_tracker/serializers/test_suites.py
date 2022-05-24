"""Everything related to TestSuites"""


from server.test_tracker.models.project import TestCases, TestSuites
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from server.test_tracker.serializers.test_cases import TestCaseSerializer

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

class TestSuitesDetailSerializer(ModelSerializer):
    """class TestSuitesSerializer to serialize the test suite obj"""
    created = SerializerMethodField()
    modified = SerializerMethodField()
    number_of_test_cases = SerializerMethodField()
    test_cases = SerializerMethodField()
    test_plan = SerializerMethodField()

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
    
    def get_test_cases(self, obj):
        """Method to get the test cases"""
        test_cases = TestCases.objects.filter(test_suite=obj).order_by('-created')
        return TestCaseSerializer(test_cases, many=True).data
    
    def get_test_plan(self, obj):
        """Method to get the test plan"""
        data = {
            'id': obj.test_plan.id,
            'title': obj.test_plan.title,
        }
        return data
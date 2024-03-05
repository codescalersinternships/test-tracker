"""Everything related to the project."""
from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField

from test_tracker.models.project import TestPlan, TestSuitesSection
from test_tracker.serializers.test_cases import TestCaseSerializer


class TestPlanSerializer(ModelSerializer):
    created = SerializerMethodField()
    modified = SerializerMethodField()

    class Meta:
        model = TestPlan
        exclude = ("temps", "project")

    def get_created(self, obj):
        return obj.created.date()

    def get_modified(self, obj):
        return obj.modified.date()


class TestPlanDetailSerializer(ModelSerializer):
    created = SerializerMethodField()
    modified = SerializerMethodField()
    temps = SerializerMethodField()

    class Meta:
        model = TestPlan
        exclude = ("project",)

    def get_created(self, obj):
        return obj.created.date()

    def get_modified(self, obj):
        return obj.modified.date()

    def get_temps(self, obj):
        if obj.type == "blank":
            return obj.temps[::-1]
        return obj.temps


class UpdateTestPlanSerializer(ModelSerializer):
    class Meta:
        model = TestPlan
        fields = ("title",)


class TestPlanTempsSerializer(ModelSerializer):
    title = CharField()
    content = CharField()

    class Meta:
        model = TestPlan
        fields = ("title", "content")

class TestSuiteSectionSerializer(ModelSerializer):
    
    class Meta:
        model = TestSuitesSection
        fields = ("id", "title", "test_suites",)

class GetTestSuiteSectionSerializer(ModelSerializer):
    test_cases = SerializerMethodField()
    class Meta:
        model = TestSuitesSection
        fields = ("id", "title", "test_suites","test_cases")
        
    def get_test_cases(self, obj):
        return TestCaseSerializer(obj.test_cases, many=True).data
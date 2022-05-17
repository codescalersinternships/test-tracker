"""Everything related to the project."""
from datetime import datetime
from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField
from server.test_tracker.models.dashboard import Project

from server.test_tracker.models.project import TestPlan



class TestPlanSerializer(ModelSerializer):
    class Meta:
        model = TestPlan
        exclude = ('temps','project')

class TestPlanDetailSerializer(ModelSerializer):
    class Meta:
        model = TestPlan
        exclude = ('project',)

class UpdateTestPlanSerializer(ModelSerializer):
    class Meta:
        model = TestPlan
        fields = ('title',)

class AddOrUpdateTempsSerializer(ModelSerializer):
    title = CharField()
    content = CharField()

    class Meta:
        model = TestPlan
        fields = ('title','content')

class ActivitySerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ('activity',)

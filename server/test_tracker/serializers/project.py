"""Everything related to the project."""
from rest_framework.serializers import ModelSerializer

from server.test_tracker.models.project import TestPlan



class TestPlanSerializer(ModelSerializer):
    class Meta:
        model = TestPlan
        fields = ('name','type',)

"""Everything related to requirements"""
from rest_framework.serializers import ModelSerializer

from server.test_tracker.models.project import Requirements

class ProjectRequirementSerializer(ModelSerializer):
    """class ProjectRequirementSerializer to serialize the project requirement"""
    class Meta:
        """class meta"""
        model = Requirements
        fields = ['id', 'title']
"""Everything related to requirements"""
from rest_framework.serializers import ModelSerializer

from server.test_tracker.models.project import Requirements, ProjectRequirement

class ProjectRequirementSerializer(ModelSerializer):
    """class RequirementsSerializer to serialize the project requirement"""
    class Meta:
        """class meta"""
        model = ProjectRequirement
        fields = ['id', 'title']

class RequirementsSerializer(ModelSerializer):
    """This serializer is a sub requirement of ProjectRequirementSerializer"""
    class Meta:
        """class meta"""
        model = Requirements
        fields = ['id', 'title', 'description']

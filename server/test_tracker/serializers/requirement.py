"""Everything related to requirements"""
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from server.test_tracker.models.project import Requirements, ProjectRequirement

class ProjectRequirementSerializer(ModelSerializer):
    """class RequirementsSerializer to serialize the project requirement"""
    created = SerializerMethodField()
    updated = SerializerMethodField()
    requirements = SerializerMethodField()

    class Meta:
        """class meta"""
        model = ProjectRequirement
        fields = ['id', 'title', 'created', 'updated', 'requirements']
    
    def get_created(self, obj):return obj.created.date()
    def get_updated(self, obj):return obj.modified.date()
    def get_requirements(self, obj):
        return RequirementsSerializer(obj.project_requirement, many=True).data


class RequirementsSerializer(ModelSerializer):
    """This serializer is a sub requirement of ProjectRequirementSerializer"""
    created = SerializerMethodField()
    updated = SerializerMethodField()

    class Meta:
        """class meta"""
        model = Requirements
        fields = ['id', 'title', 'description', 'created', 'updated',]

    def get_created(self, obj):return obj.created.date()
    def get_updated(self, obj):return obj.modified.date()

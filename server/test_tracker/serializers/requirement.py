"""Everything related to requirements"""
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from test_tracker.models.project import Requirements, RequirementDocs


class RequirementDocsSerializer(ModelSerializer):
    """class RequirementsSerializer to serialize the project requirement"""

    created = SerializerMethodField()
    updated = SerializerMethodField()
    requirements = SerializerMethodField()

    class Meta:
        """class meta"""

        model = RequirementDocs
        fields = ["id", "title", "created", "updated", "requirements"]

    def get_created(self, obj):
        return obj.created.date()

    def get_updated(self, obj):
        return obj.modified.date()

    def get_requirements(self, obj):
        return RequirementsSerializer(
            obj.project_requirement.order_by("-created"), many=True
        ).data


class RequirementsSerializer(ModelSerializer):
    """This serializer is a sub requirement of RequirementDocsSerializer"""

    created = SerializerMethodField()
    updated = SerializerMethodField()
    requirement_title = SerializerMethodField()
    requirement_doc = SerializerMethodField()

    class Meta:
        """class meta"""

        model = Requirements
        fields = [
            "id",
            "title",
            "description",
            "created",
            "updated",
            "requirement_title",
            "requirement_doc",
        ]

    def get_created(self, obj):
        return obj.created.date()

    def get_updated(self, obj):
        return obj.modified.date()

    def get_requirement_title(self, obj):
        return obj.requirement_title

    def get_requirement_doc(self, obj):
        return obj.requirement.id

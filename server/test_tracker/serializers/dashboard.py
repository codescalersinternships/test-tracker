from rest_framework.serializers import ModelSerializer
from server.test_tracker.models.dashboard import People, Project


class ProjectsSerializer(ModelSerializer):
    """class ProjectsSerializer to serialize the project obj"""
    class Meta:
        model = Project
        exclude = ('user',)

class PeopleSerializer(ModelSerializer):
    """class PeopleSerializer to serialize the people obj"""
    class Meta:
        model = People
        exclude = ('user',)
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from server.test_tracker.models.dashboard import People, Project
from server.test_tracker.models.users import Notification, User


class ProjectsSerializer(ModelSerializer):
    """class ProjectsSerializer to serialize the project obj"""
    class Meta:
        model = Project
        exclude = ('user',)

class NotificationSerializer(ModelSerializer):
    """class Notification to serialize the Notification obj"""
    class Meta:
        model = Notification
        exclude = 'user'

class PeopleSerializer(ModelSerializer):
    """class PeopleSerializer to serialize the people obj"""
    class Meta:
        model = People
        exclude = ('user','invited','accepted',)

class ProfileSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id','first_name','last_name', 'email',
            'phone'
        ]
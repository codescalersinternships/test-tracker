from rest_framework.serializers import ModelSerializer, SerializerMethodField
from server.test_tracker.models.dashboard import Member, Project
from server.test_tracker.models.users import User


class ProjectsSerializer(ModelSerializer):
    """class ProjectsSerializer to serialize the project obj"""
    created = SerializerMethodField()
    class Meta:
        model = Project
        exclude = ('user', 'activity', 'members',)
    
    def get_created(self, obj):
        return obj.created.date()

class MemberSerializer(ModelSerializer):
    """class MemberSerializer to serialize the Member obj"""
    class Meta:
        model = Member
        fields = ('first_name', 'last_name', 'email','permission')

class GetMemberSerializer(ModelSerializer):
    """class GetMemberSerializer to serialize the Member obj"""
    member = SerializerMethodField(read_only=True)

    class Meta:
        model = Member
        fields = ('permission','member')

    def get_member(self, obj):
        member = obj.invited_user
        if member is None:
            return MemberSerializer(obj.signature.json_data).data
        return ProfileSerializers(obj.invited_user).data

class ProfileSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id','first_name','last_name', 'email',
            'phone'
        ]
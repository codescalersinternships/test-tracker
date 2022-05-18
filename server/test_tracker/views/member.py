"""Everything related to Member"""


from django.contrib.auth.hashers import make_password

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from server.test_tracker.api.permission import UserIsAuthenticated

from server.test_tracker.api.response import CustomResponse
from server.test_tracker.models.dashboard import Member
from server.test_tracker.serializers.dashboard import GetMemberSerializer, MemberSerializer
from server.test_tracker.serializers.member import MemberSetPasswordSerializer
from server.test_tracker.services.dashboard import *


class GetMemberApiView(GenericAPIView):
    """
        You may have to use this class when you want to get all of your Member
        You must be authenticated to access this view
    """
    serializer_class = GetMemberSerializer
    permission_classes = (UserIsAuthenticated,)

    def get(self, request: Request) -> Response:
        """Use this method to get all of member based on request user"""
        member = get_member_by_id(request.user.id)
        if member != None:
            return CustomResponse.unauthorized()
        member: Member = get_member_based_on_user(request.user)
        if len(member) > 0:
            return CustomResponse.success(
                data=GetMemberSerializer(member, many=True).data,
                message="Member found successfully",
            )
        return CustomResponse.success(
            [],
            message="There are no Member yet, try tp add one",
        )

class MemberSetPasswordAPIView(GenericAPIView):
    """This class to set password for member on Member table"""
    serializer_class = MemberSetPasswordSerializer

    def put(self, request: Request) -> Response:
        """Method to set password for member on Member table"""
        signature = request.query_params.get('signature')
        if signature:
            member = get_signature(signature)
            if member is not None:
                serializer = self.get_serializer(member, data=request.data)
                if serializer.is_valid():
                    password = serializer.validated_data.get('password')
                    serializer.save(password = make_password(password))
                    return CustomResponse.success(
                        message="Password updated successfully",
                        status_code=203
                    )
                return CustomResponse.bad_request(
                    message = 'Please make sure that you entered a valid data',
                    error = serializer.errors
                )
            return CustomResponse.not_found(message = 'Invalid signature')
        return CustomResponse.bad_request(message = 'Missing signature')

class MemberDetailAPIView(GenericAPIView):
    """
        Class MemberDetailAPIView has all the functionality based on the Member added
        Methods [GET, PUT, DELETE]
    """
    serializer_class = MemberSerializer
    permission_classes = (UserIsAuthenticated,)

    def get(self, request: Request, member_email: str) -> Response:
        """Return a single member based on the request user, member_email"""
        member: Member = get_member_by_user_and_member_email(
            request.user, member_email
        )
        if member is not None:
            return CustomResponse.success(
                data=MemberSerializer(member).data,
                message="User found successfully",
            )
        return CustomResponse.not_found(
            message="User not found",
        )

    def delete(self, request: Request, member_email: str) -> Response:
        """
            The host can delete the member, 
            but it will not deleted from the whole system (only from access)
        """
        member: Member = get_member_by_user_and_member_email(
            request.user, member_email
        )
        if member is not None:
            member.delete()
            return CustomResponse.success(
                message="User deleted successfully",
                status_code=204
            )
        return CustomResponse.not_found(
            message="User not found",
        )

class FULLACCESSPermissionAPIView(GenericAPIView):
    """
        Class MemberPermissionAPIView have all the functionality based on the Member added
    """
    serializer_class = MemberSerializer
    permission_classes = (UserIsAuthenticated,)

    def get(self, request: Request) -> Response:
        member = get_full_access_permission_based_on_user(request.user)
        return CustomResponse.success(
            data=MemberSerializer(member, many=True).data,
            message="Member found successfully",
        )

class ADMINACCESSPermissionAPIView(GenericAPIView):
    """
        Class MemberPermissionAPIView have all the functionality based on the Member added
    """
    serializer_class = MemberSerializer
    permission_classes = (UserIsAuthenticated,)

    def get(self, request: Request) -> Response:
        member = get_admin_access_permission_based_on_user(request.user)
        return CustomResponse.success(
            data=MemberSerializer(member, many=True).data,
            message="Member found successfully",
        )
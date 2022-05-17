"""Everything related to Member"""


from django.contrib.auth.hashers import make_password

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from server.test_tracker.api.response import CustomResponse
from server.test_tracker.serializers.member import MemberSetPasswordSerializer
from server.test_tracker.services.dashboard import get_signature



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
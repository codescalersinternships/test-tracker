"""Everything related to people"""


from django.contrib.auth.hashers import make_password

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from server.test_tracker.api.response import CustomResponse
from server.test_tracker.serializers.people import PeopleSetPasswordSerializer
from server.test_tracker.services.dashboard import get_signature





class PeopleSetPasswordAPIView(GenericAPIView):
    """This class to set password for person on people table"""
    serializer_class = PeopleSetPasswordSerializer

    def put(self, request: Request) -> Response:
        """Method to set password for person on people table"""
        signature = request.query_params.get('signature')
        if signature:
            person = get_signature(signature)
            if person is not None:
                serializer = self.get_serializer(person, data=request.data)
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
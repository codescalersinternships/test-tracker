from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from server.test_tracker.api.response import CustomResponse

from server.test_tracker.serializers.auth import RegisterSerializer


class RegisterAPIView(GenericAPIView):
    """Class RegisterAPIView to register a new user into database"""
    serializer_class = RegisterSerializer
    def post(self, request: Request) -> Response:
        """Method to register a new user"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return CustomResponse.success(
                data = serializer.data,
                message = "User created successfully"
            )
        return CustomResponse.bad_request(
            error = serializer.errors,
            message = "User creation failed"
        )

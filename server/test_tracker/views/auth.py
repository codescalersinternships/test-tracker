"""Everything related to authentication."""
from ast import Dict
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from server.test_tracker.api.response import CustomResponse
from server.test_tracker.models.users import User

from server.test_tracker.serializers.auth import LoginSerializer, RegisterSerializer
from server.test_tracker.services.dashboard import get_people_based_on_signature, get_signature
from server.test_tracker.services.users import get_user_by_email_for_login
from server.test_tracker.utils.auth import get_tokens_for_user
from server.test_tracker.utils.validations import Validator


class RegisterAPIView(GenericAPIView):
    """Class RegisterAPIView to register a new user into database"""
    serializer_class = RegisterSerializer
    def post(self, request: Request) -> Response:
        """Method to register a new user"""
        print(request.query_params)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                data = serializer.data,
                message = "User created successfully",
                status_code=201
            )
        return CustomResponse.bad_request(
            error = serializer.errors,
            message = "User creation failed"
        )

class LoginByTokenAPIView(GenericAPIView):
    """Class LoginByTokenAPIView to login a user by jwt token"""
    serializer_class = LoginSerializer

    def post(self, request: Request) -> Response:
        """Method to login a user by jwt token"""
        serializer: Dict = self.get_serializer(data=request.data)
        email: str = request.data.get('email')
        if serializer.is_valid() and Validator().validate_email(email):
            password: str = serializer.validated_data.get('password')
            user: User = get_user_by_email_for_login(email)
            if user is not None:
                if user.check_password(password) or user.password == password:
                    return CustomResponse.success(
                        message="Valid email in our system.",
                        data=get_tokens_for_user(user)
                    )
                return CustomResponse.bad_request(message = 'Wrong Credential!')
            return CustomResponse.not_found(message = 'There are no user with this email.')
        return CustomResponse.bad_request(error=serializer.errors)

class DecodeAndVerifySignatureAPIView(APIView):
    """Decode signature of a person invited"""

    def get(self, request: Request) -> Response:
        """Method to decode signature of a person invited"""
        try:
            return CustomResponse.success(
                data=get_signature(request.query_params.get('signature')).json_data
            )
        except:
            return CustomResponse.not_found(
                message = 'Signature could not be decoded, Make sure that you have a valid signature'
            )

    def put(self, request: Request) -> Response:
        """This endpoint to create a new user into database after success registration invited"""
        # Get the new user by his signature and 
        # put on people table to have access on the projects based on his permission.
        signature = get_signature(request.query_params.get('signature'))
        if signature is not None:
            invited_user_email = signature.json_data.get('email')
            user = get_user_by_email_for_login(invited_user_email)
            if user is not None:
                people = get_people_based_on_signature(signature)
                if people is not None:
                    people.invited_user = user
                    people.accepted = True
                    people.signature = None
                    people.save()
                    signature.delete() # We dont want to use this signature anymore
                    return CustomResponse.success(
                        message = 'Person added successfully',
                    )
                return CustomResponse.not_found(
                    message = 'There are no people related by this signature'
                )
            return CustomResponse.not_found(
                message = f"signature '{signature}' not found"
            )
        return CustomResponse.not_found(
            message = 'Signature could not be decoded, Make sure that you have a valid signature'
        )

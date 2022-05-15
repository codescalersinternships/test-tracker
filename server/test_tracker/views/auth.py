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
from server.test_tracker.services.users import get_user_by_email_for_login, success_login_user
from server.test_tracker.utils.auth import get_tokens_for_user
from server.test_tracker.utils.validations import Validator
from django.contrib.auth.hashers import make_password



class RegisterAPIView(GenericAPIView):
    """Class RegisterAPIView to register a new user into database"""
    serializer_class = RegisterSerializer
    def post(self, request: Request) -> Response:
        """Method to register a new user"""
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
            user: User = success_login_user(email, password)
            if user:
                tokens: Dict = get_tokens_for_user(user)
                return CustomResponse.success(
                    data = tokens,
                    message = "User logged in successfully",
                    status_code = 200
                )
            return CustomResponse.bad_request(
                message = "User not found",
                status_code = 400
            )
        return CustomResponse.bad_request(
            message = "Please make sure your email is valid",
            error=serializer.errors
        )

class DecodeAndVerifySignatureAPIView(APIView):
    """Decode signature of a person invited"""

    def get(self, request: Request) -> Response:
        """Method to decode signature of a person invited"""
        try:
            signature = get_signature(request.query_params.get('signature'))
            data = {
                'email': signature.email,
                'first_name': signature.first_name,
                'last_name': signature.last_name,
            }
            print(signature)
            return CustomResponse.success(
                data = data
            )
        except:
            return CustomResponse.not_found(
                message = 'Signature could not be decoded, Make sure that you have a valid signature'
            )

    def put(self, request: Request) -> Response:
        """Update person obj"""
        person_signature = get_signature(request.query_params.get('signature'))
        if person_signature is not None:
            person_signature.accepted = True
            person_signature.signature = None # Remove signature from db
            person_signature.save()
            return CustomResponse.success(
                message = 'Person updated successfully',
            )
        return CustomResponse.not_found(
            message = 'Signature could not be decoded, Make sure that you have a valid signature'
        )

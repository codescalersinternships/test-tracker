"""Everything related to authentication."""
import json
from django.contrib.auth.hashers import make_password
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from test_tracker.api.permission import UserIsAuthenticated
from test_tracker.api.response import CustomResponse
from test_tracker.models.users import User
from test_tracker.serializers.auth import (
    GitHubRequestToGetAccessTokenSerializers,
    GitHubUserDataSerializers,
    MyTokenObtainPairSerializer,
    MyTokenRefreshSerializer,
    RegisterSerializer,
    UpdateUserSettingsSerializer,
    UserSerializer,
)
from test_tracker.services.dashboard import get_signature
from test_tracker.services.users import get_user_by_id, get_user_or_member
from urllib import parse
import requests
from components import config

from test_tracker.utils.generate_password import generate_password


class RegisterAPIView(GenericAPIView):
    """Class RegisterAPIView to register a new user into database"""

    serializer_class = RegisterSerializer

    def post(self, request: Request) -> Response:
        """Method to register a new user"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                data=serializer.data,
                message="User created successfully",
                status_code=201,
            )
        return CustomResponse.bad_request(
            error=serializer.errors, message="User creation failed"
        )


class LoginByTokenAPIView(TokenObtainPairView):
    """Class LoginByTokenAPIView to login a user by jwt token"""

    serializer_class = MyTokenObtainPairSerializer


class MyTokenRefreshView(TokenRefreshView):
    """
    An end point to refresh the user token
    """

    serializer_class = MyTokenRefreshSerializer


class DecodeAndVerifySignatureAPIView(APIView):
    """Decode signature of a member invited"""

    def get(self, request: Request) -> Response:
        """Method to decode signature of a member invited"""
        signature = get_signature(request.query_params.get("signature"))
        if signature is None:
            return CustomResponse.not_found(
                message="Signature could not be decoded, Make sure that you have a valid signature"
            )
        data = {
            "email": signature.email,
            "first_name": signature.first_name,
            "last_name": signature.last_name,
        }
        return CustomResponse.success(data=data)

    def put(self, request: Request) -> Response:
        """Update member obj"""
        member_signature = get_signature(request.query_params.get("signature"))
        if member_signature is not None:
            member_signature.accepted = True
            member_signature.signature = None  # Remove signature from db
            member_signature.save()
            return CustomResponse.success(
                message="Member updated successfully",
            )
        return CustomResponse.not_found(
            message="Signature could not be decoded, Make sure that you have a valid signature"
        )


class GetUserAPIView(GenericAPIView):
    serializer_class = UserSerializer

    def get(self, request: Request, email: str) -> Response:
        user = get_user_or_member(email)
        if user is not None:
            return CustomResponse.success(
                data=self.get_serializer(user).data,
                message="User found",
                status_code=200,
            )
        return CustomResponse.not_found(
            message="User not found",
        )


class UpdateUserSettingsAPIView(GenericAPIView):
    """This class to update profile info"""

    serializer_class = UpdateUserSettingsSerializer
    permission_classes = (UserIsAuthenticated,)

    def put(self, request: Request) -> Response:
        """Update user settings"""
        user = get_user_by_id(request.user.id)
        serializer = self.get_serializer(user, data=request.data)
        if not request.data.get("password"):
            request.data["password"] = user.password
        else:
            request.data["password"] = make_password(request.data["password"])
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                data=serializer.data,
                message="Profile updated successfully.",
                status_code=201,
            )
        return CustomResponse.bad_request(
            error=serializer.errors,
            message="Profile update failed.",
        )

class GithubAccessTokenAPIView(GenericAPIView):
    serializer_class = GitHubRequestToGetAccessTokenSerializers
    
    def post(self, request: Request) -> CustomResponse:
        """Request to get user access token from github"""
        serializer = self.get_serializer(data=request.data)
        token_url: str = "https://github.com/login/oauth/access_token"
        if serializer.is_valid():
            response = requests.post(token_url, data=serializer.data)
            token_url = token_url + "?" + str(response.content).replace("b'", "").replace("'","")
            data = dict(parse.parse_qsl(parse.urlsplit(token_url).query))
            return CustomResponse.success(data=data, message="Success")
        return CustomResponse.bad_request(
            message="Please make sure that you entered a vaild data", 
            errors=serializer.errors
        )

class GithubUserDataAPIView(GenericAPIView):
    serializer_class = GitHubUserDataSerializers

    def post(self, request: Request) -> CustomResponse:
        """Request to get user info"""
        serializer = self.get_serializer(data=request.data)
        user_url: str = "https://api.github.com/user"
        if serializer.is_valid():
            response = requests.get(user_url, data=serializer.data, headers={
                "Authorization": f"Bearer {serializer.data.get('access_token')}"
            })
            response = response.json()
            try:
                User.objects.get(email=response.get("email"))
            except:
                User.objects.create(
                    email = response.get("email"),
                    first_name = response.get("name"),
                    password = make_password(serializer.data.get('access_token')),
                    github_token = serializer.data.get('access_token')
                )
            sys_user = User.objects.get(email=response.get("email"))
            sys_user.github_token = serializer.data.get('access_token')
            sys_user.password = make_password(sys_user.github_token)
            sys_user.save()
            cerds = {
                "email" : sys_user.email,
                "password" : sys_user.github_token
            }
            login_response = requests.post(
                f"http://{config('SERVER_DOMAIN_NAME')}/api/auth/login/",
                data=json.dumps(cerds),
                headers={
                    "Content-Type": "application/json"
                }
            )
            return CustomResponse.success(data=login_response.json(), message="User found")
        return CustomResponse.bad_request(
            message="Please make sure that you entered a vaild data", 
            error=serializer.errors
        )

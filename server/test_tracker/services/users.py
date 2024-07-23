from test_tracker.models.dashboard import Member
from test_tracker.models.users import User
from test_tracker.services.member import get_member_by_email
from django.contrib.auth.hashers import check_password


def get_user_by_id(id: str) -> User:
    """Return user who have the same id"""
    try:
        return User.objects.get(id=int(id))
    except User.DoesNotExist:
        return None


def get_user_by_email_for_login(email: str) -> User:
    """Return user who have the same email"""
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None


def success_login_user(email, password) -> User or Member:
    """Return user who have the same email and password"""
    try:
        user: User = User.objects.get(email=email)
    except User.DoesNotExist:
        user: Member = get_member_by_email(email)
    if user:
        if check_password(password, user.password):
            return user
    return None


def get_user_or_member(email: str) -> User or Member:
    """Return user who have the same email and password"""
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = Member.objects.get(email=email)
    return user if user is not None else None

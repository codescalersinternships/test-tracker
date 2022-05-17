from server.test_tracker.models.dashboard import People
from server.test_tracker.models.users import User
from server.test_tracker.services.people import get_person_by_email, get_person_by_id
from django.contrib.auth.hashers import check_password

def get_user_by_id(id: str) -> User:
    """Return user who have the same id"""
    if id.isdigit():
        try:
            return User.objects.get(id=int(id))
        except:
            return None
    return None

def get_user_by_email_for_login(email: str) -> User:
    """Return user who have the same email"""
    try:
        return User.objects.get(email=email)
    except:
        return None

def success_login_user(email, password) -> User or People:
    """Return user who have the same email and password"""
    try:
        user: User = User.objects.get(email=email)
    except:
        user: People = get_person_by_email(email)
    if user:
        if check_password(password, user.password):
            return user
    return None

def get_user_or_people(email: str) -> User or People:
    """Return user who have the same email and password"""
    try:
        user = User.objects.get(email = email)
    except:
        user = People.objects.get(email = email)
    return user if user is not None else None

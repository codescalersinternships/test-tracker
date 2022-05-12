from server.test_tracker.models.users import User


def get_user_by_id(id: int) -> User:
    """Return user who have the same id"""
    try:
        return User.objects.get(id=id)
    except:
        return None

def get_user_by_email_for_login(email: str) -> User:
    """Return user who have the same email"""
    try:
        return User.objects.get(email=email)
    except:
        return None
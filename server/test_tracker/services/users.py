from server.test_tracker.models.users import User


def get_user_by_id(id: int) -> User:
    """Return user who have the same id"""
    try:
        return User.objects.get(id=id)
    except:
        return None
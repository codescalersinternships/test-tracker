"""Everything related to Member"""


from server.test_tracker.models.dashboard import Member


def get_member_by_email(email: str) -> Member:
    """Try to return a member who have same email"""
    try:
        return Member.objects.get(email=email)
    except Member.DoesNotExist:
        return None

def get_member_by_id(member_id: int) -> Member:
    """Try to return a member who have same email"""
    try:
        return Member.objects.get(id = member_id)
    except Member.DoesNotExist:
        return None
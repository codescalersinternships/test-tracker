"""Everything related to people"""


from server.test_tracker.models.dashboard import People


def get_person_by_email(email: str) -> People:
    """Try to return a person who have same email"""
    try:
        return People.objects.get(email=email)
    except People.DoesNotExist:
        return None

def get_person_by_id(person_id: str) -> People:
    """Try to return a person who have same email"""
    if person_id.isdigit():
        try:
            return People.objects.get(id = int(person_id))
        except People.DoesNotExist:
            return None
    return None
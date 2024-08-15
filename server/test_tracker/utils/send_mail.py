from settings import EMAIL_HOST_USER
from django.core.mail import send_mail


def send_email(
    invited_user_first_name, host_user, invited_user_email: str, redirect_link=None
):
    """Send an email to the specified user"""
    title = (
        f"TestTracker - {host_user.first_name} has invited you to join their account"
    )
    content = f"""
        Hi {invited_user_first_name}

        {host_user.first_name} has just invited you to join their TestTracker account.

        TestTracker is an online test management tool,
        that allows you to manage your test plans, requirements, test cases and test runs with ease.

        To get started, accept this invite using the activation link below:
        {redirect_link}

        Thanks,
        The TestTracker Team
        """
    return send_mail(title, content, str(EMAIL_HOST_USER), [invited_user_email])

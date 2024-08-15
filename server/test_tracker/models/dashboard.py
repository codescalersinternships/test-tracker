from django.db import models

from test_tracker.models.abstracts import TimeStampedModel
from test_tracker.models.users import User

import uuid


class PERMISSION_CHOICES(models.TextChoices):
    FULL_ACCESS = "full_access", "Full access"
    ADMIN_ACCESS = "admin_access", "Admin access"


class Project(TimeStampedModel):
    """Class project model for adding a new project to the database"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_projects"
    )
    members = models.ManyToManyField("Member", related_name="project_members")
    title = models.CharField(max_length=100)
    repo_link = models.CharField(max_length=300, null=True, blank=True)
    short_description = models.TextField(max_length=500)
    activity = models.JSONField(default=dict)
    TC_Title = models.JSONField(default=list)
    REQ_Title = models.JSONField(default=list)

    def __str__(self):
        return self.title


class Member(User):
    """
    Class Member model to add a new member to accessing the project
    based on the permission type
    - To use this model you need to have already project
    """

    host_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="host_user_manager"
    )

    permission = models.CharField(
        max_length=100,
        choices=PERMISSION_CHOICES.choices,
        default=PERMISSION_CHOICES.FULL_ACCESS,
    )

    signature = models.UUIDField(default=uuid.uuid4, null=True)

    invited = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.email)

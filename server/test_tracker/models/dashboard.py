from django.db import models

from server.test_tracker.models.abstracts import (
    TimeStampedModel
)
from server.test_tracker.models.users import User

import uuid



class PERMISSION_CHOICES(models.TextChoices):
    FULL_ACCESS = "full_access", "Full access"
    ADMIN_ACCESS = "admin_access", "Admin access"


class Project(TimeStampedModel):
    """Class project model for adding a new project to the database"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_projects")
    name = models.CharField(max_length=100)
    activity = models.JSONField(default=dict)

    def __str__(self):
        return self.name


class People(TimeStampedModel):
    """
    Class people model to add a new person to accessing the project
    based on the permission type
    - To use this model you need to have already project
    """
    host_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='host_user')

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=70, unique=True)

    permission = models.CharField(
        max_length=100,
        choices=PERMISSION_CHOICES.choices,
        default=PERMISSION_CHOICES.FULL_ACCESS
    )

    signature = models.UUIDField(default=uuid.uuid4, null=True)
    password = models.CharField(max_length=50, null=True)

    invited = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return str("{} -> {}".format(self.host_user , self.email))

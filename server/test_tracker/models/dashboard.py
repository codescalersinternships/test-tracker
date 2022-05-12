from django.db import models

from server.test_tracker.models.abstracts import (
    TimeStampedModel
)
from server.test_tracker.models.users import User



class PERMISSION_CHOICES(models.TextChoices):
    FULL_ACCESS = "full_access", "Full access"
    ADMIN_ACCESS = "admin_access", "Admin access"


class Project(TimeStampedModel):
    """Class project model for adding a new project to the database"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_projects")
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class People(TimeStampedModel):
    """
    Class people model to add a new person to accessing the project
    based on the permission type
    - To use this model you need to have already project
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=70, unique=True)
    permission = models.CharField(
        max_length=100,
        choices=PERMISSION_CHOICES.choices,
        default=PERMISSION_CHOICES.FULL_ACCESS
    )

    def __str__(self):
        return self.full_name


class Settings(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='media/logo')

    def __str__(self):
        return self.user.full_name

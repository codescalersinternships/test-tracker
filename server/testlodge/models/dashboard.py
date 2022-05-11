from django.db import models
from enum import Enum

from server.testlodge.models.abstracts import (
    TimeStampedModel, BaseUserInfo
)
from server.testlodge.models.users import User



class PERMISSION_CHOICES(Enum):
    FULL_ACCESS = "full access", "full access"
    ADMIN_ACCESS = "admin access", "admin access"


class Project(TimeStampedModel):
    """Class project model for adding a new project to the database"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class People(TimeStampedModel, BaseUserInfo):
    """
    Class people model to add a new person to accessing the project
    based on the permission type
    - To use this model you need to have already project
    """
    permission = models.CharField(
        max_length=100,
        choices=PERMISSION_CHOICES,
        default=PERMISSION_CHOICES.FULL_ACCESS
    )

    def __str__(self):
        return self.full_name


class Settings(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='media/logo')

    def __str__(self):
        return self.user.full_name

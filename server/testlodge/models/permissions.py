"""This file contains user permissions"""

from django.db import models
from server.testlodge.models.abstracts import TimeStampedModel
from server.testlodge.models.users import User


class Administrator(TimeStampedModel):
    """
    Administrators can:

    - Create, edit and delete projects
    - Create, manage and assign people
    - Update account settings
    - Access all projects
    """
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="AdministratorAuthor"
    )
    users = models.ManyToManyField(User)

    def __str__(self):
        return str(self.author.full_name)

class AccountHolders(TimeStampedModel):
    """
    Account holders can:

    - Do everything that you can
    - Manage all projects and people
    - Manage payment details and receipts
    - Manage and cancel this account
    """
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="AccountHoldersAuthor"
    )
    users = models.ManyToManyField(User)

    def __str__(self):
        return str(self.author.full_name)

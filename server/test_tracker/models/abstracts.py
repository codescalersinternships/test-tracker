"""abstract model for created, updated timestamps"""
from django.db import models


class TimeStampedModel(models.Model):
    """
    database model for created at and updated at fields
    """
    created  = models.DateTimeField(db_index=True, auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseUserInfo(models.Model):
    """
    database model for user information
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=70)

    @property
    def full_name(self) -> str:
        """Normal method to concatonate first_name and last_name"""
        return f'{self.first_name} {self.last_name}'
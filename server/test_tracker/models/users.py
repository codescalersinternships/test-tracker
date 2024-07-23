"""Base user models"""
from typing import Any, Union

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    AnonymousUser,
)

from test_tracker.models.abstracts import (
    TimeStampedModel,
)


class TestTrackerBaseUserManger(BaseUserManager):
    """This is the main class for user manger"""

    def create_user(self, email: str, password: str) -> "User":
        """DMC method to create user"""
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str):
        """Create super user [admin]"""
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, TimeStampedModel):
    """Main user model"""

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=70, unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    github_token = models.CharField(max_length=250, null=True, blank=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = TestTrackerBaseUserManger()
    USERNAME_FIELD = "email"

    @property
    def full_name(self) -> str:
        """Normal method to concatonate first_name and last_name"""
        return f"{self.first_name.title()} {self.last_name.title()}"

    def has_perm(
        self, perm: str, obj: Union[models.Model, AnonymousUser, None] = None
    ) -> bool:
        """For checking permissions. to keep it simple all admin have ALL permissions"""
        return self.is_admin

    @staticmethod
    def has_module_perms(app_label: Any) -> bool:
        """Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)"""
        return True

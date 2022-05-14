"""This file contains all sub tables based on the project table on 'models/dashboard' """
from email.policy import default
from django.db import models
from enum import Enum

from server.test_tracker.models.abstracts import TimeStampedModel
from server.test_tracker.models.dashboard import Project



class PLAN_CHOICES(models.TextChoices):
    TEMPLATE = "template", "template"
    BLANK = "blank", "blank"

class TestPlan(TimeStampedModel):
    """
    Class test plan model for adding a new test plan to the database
    based on the project    
    """
    project = models.ForeignKey(
        Project, related_name="project_test_plans",
        on_delete=models.CASCADE, null=True
    )
    name = models.CharField(max_length=150)
    type = models.CharField(
        max_length=100,
        choices=PLAN_CHOICES.choices,
        default=PLAN_CHOICES.TEMPLATE
    )
    temps = models.JSONField(default=dict)

    def __str__(self):
        return self.name
    
    def add_or_update_temps(self, title: str, content: str) -> None:
        """
        This method adds or updates the temps of the test plan
        """
        self.temps[title] = content
        self.save()

    def delete_temp(self, title: str) -> None:
        """
        This method delete_content of the temps of the test plan
        """
        if self.temps.get(title):
            del self.temps[title]
            self.save()
            return True
        return False

class Requirement(TimeStampedModel):
    """
    Class test requirement model for adding a new requirement to the database
    based on the testplan
    """
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title
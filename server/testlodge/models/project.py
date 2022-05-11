"""This file contains all sub tables based on the project table on 'models/dashboard' """
from django.db import models
from enum import Enum

from server.testlodge.models.abstracts import TimeStampedModel



class PLAN_CHOICES(Enum):
    TEMPLATE = "template", "template"
    BLANK = "blank", "blank"


class TestPlan(TimeStampedModel):
    """
    Class test plan model for adding a new test plan to the database
    based on the project    
    """
    name = models.CharField(max_length=150)
    type = models.CharField(
        max_length=100,
        choices=PLAN_CHOICES,
        default=PLAN_CHOICES.TEMPLATE
    )

    def __str__(self):
        return self.name


class TestPlanDetail(TimeStampedModel):
    """
    Class test plan model for adding a new test plan to the database
    based on the project    
    """
    name = models.CharField(max_length=150)
    content = models.TextField()

    def __str__(self):
        return self.name


class Requirement(TimeStampedModel):
    """
    Class test requirement model for adding a new requirement to the database
    based on the testplan
    """
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title
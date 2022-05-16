"""This file contains all sub tables based on the project table on 'models/dashboard' """
from django.db import models
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

class ProjectRequirement(TimeStampedModel):
    """
    Class test requirements model for adding a new requirements to the database
    based on the project
    """
    project = models.ForeignKey(Project, related_name="project_requirements", on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    
    def __str__(self):
        return self.title
    

class Requirements(TimeStampedModel):
    """
    Class test requirement model for adding a new requirement to the database
    based on the project
    """
    requirement = models.ForeignKey(ProjectRequirement, related_name="project_requirement", on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField(default="")

    class Meta:
        verbose_name = "Requirement"
        verbose_name_plural = "Requirements"

    def __str__(self):
        return self.title

class TestSuites(TimeStampedModel):
    """
        Class test suite model for create a new test suite for the project
    """
    project = models.ForeignKey(Project, related_name="project_test_suites", on_delete=models.CASCADE)
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title

class TestCases(TimeStampedModel):
    """
        Class test suite model for create a new test suite for the project
    """
    title = models.CharField(max_length=150)
    description = models.TextField(default="")
    test_steps = models.TextField(default="A list of steps to perform along with any sample data.")
    expected_result = models.TextField(default="Details of what the final result should be.")
    verifies_requirements = models.ManyToManyField(Requirements, related_name="verifies_requirements")

    def __str__(self):
        return self.title


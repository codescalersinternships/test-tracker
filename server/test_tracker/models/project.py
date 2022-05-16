"""This file contains all sub tables based on the project table on 'models/dashboard' """
from django.db import models
from server.test_tracker.models.abstracts import TimeStampedModel
from server.test_tracker.models.dashboard import Project
from server.test_tracker.models.users import User



class PLAN_CHOICES(models.TextChoices):
    TEMPLATE = "template", "template"
    BLANK = "blank", "blank"

class TEST_RUN_STATUS_CHOICES(models.TextChoices):
    NONE = '',''
    NOT_STARTED = "not_started", "not started"
    IN_PROGRESS = "in_progress", "in progress"
    COMPLETED = "completed", "completed"

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
    test_suite = models.ForeignKey(TestSuites, related_name="test_suite_test_cases", on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField(default="")
    test_steps = models.TextField(default="A list of steps to perform along with any sample data.")
    expected_result = models.TextField(default="Details of what the final result should be.")
    verify_requirement = models.ForeignKey(Requirements, related_name="verifies_requirements", on_delete=models.CASCADE)
    comments = models.TextField(default="")
    passed = models.BooleanField(default=False)
    failed = models.BooleanField(default=False)
    skipped = models.BooleanField(default=False)

    class Meta:
        verbose_name = "TestCase"
        verbose_name_plural = "TestCases"

    def __str__(self):
        return self.title

class TestRun(TimeStampedModel):
    """Test run model to run all of test cases based on test suites"""
    assigned_user = models.ForeignKey(User, related_name="assigned_user", on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    suites = models.ManyToManyField(TestSuites, related_name="run_suites")
    status =  models.CharField(
        max_length=100,
        choices=TEST_RUN_STATUS_CHOICES.choices,
        default=TEST_RUN_STATUS_CHOICES.NONE
    )
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title



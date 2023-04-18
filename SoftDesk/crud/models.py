from django.db import models
from django.contrib.auth.models import User


class Contributor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    PERMISSION_CHOICES = [("admin", "Admin"), ("user", "User")]
    permission = models.CharField(max_length=5, choices=PERMISSION_CHOICES)
    role = models.CharField(max_length=10)

    class Meta:
        unique_together = ("user", "project")


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    type = models.CharField(max_length=10)
    author_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="projects"
    )
    contributors = models.ManyToManyField(
        User, through=Contributor, related_name="contributed_projects"
    )


class Issue(models.Model):
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=1000)
    TAG_CHOICES = [("bug", "Bug"), ("feature", "Feature"), ("task", "Task")]
    tag = models.CharField(max_length=100, choices=TAG_CHOICES)
    PRIORITY_CHOICES = [("low", "Low"), ("medium", "Medium"), ("high", "High")]
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ("open", "Open"),
        ("in progress", "In Progress"),
        ("closed", "Closed"),
    ]
    status = models.CharField(max_length=12, choices=STATUS_CHOICES)
    author_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author_issues"
    )
    assignee_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="assignee_issues"
    )
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    author_user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

from django.db import models
from django.contrib.auth.models import User


class Contributor(models.Model):
    user_id = models.IntegerField()
    project_id = models.IntegerField()
    PERMISSION_CHOICES = [("admin", "Admin"), ("user", "User")]
    permission = models.CharField(max_length=5, choices=PERMISSION_CHOICES)
    role = models.CharField(max_length=10)


class Project(models.Model):
    project_id = models.IntegerField()
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    type = models.CharField(max_length=10)
    author_user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Issue(models.Model):
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=1000)
    TAG_CHOICES = [("bug", "Bug"), ("feature", "Feature"), ("task", "Task")]
    tag = models.CharField(max_length=100, choices=TAG_CHOICES)
    PRIORITY_CHOICES = [("low", "Low"), ("medium", "Medium"), ("high", "High")]
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    project_id = models.IntegerField()
    STATUS_CHOICES = [
        ("open", "Open"),
        ("in progress", "In Progress"),
        ("closed", "Closed"),
    ]
    status = models.CharField(max_length=12, choices=STATUS_CHOICES)
    author_user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author_issues"
    )
    assignee_user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="assignee_issues"
    )
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    comment_id = models.IntegerField()
    description = models.CharField(max_length=1000)
    author_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    issue_id = models.ForeignKey(Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

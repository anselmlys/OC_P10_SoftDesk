import uuid
from django.conf import settings
from django.db import models

from projects.models import Project


class Issue(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('inprogress', 'In Progress'),
        ('finished', 'Finished')
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ]

    TAG_CHOICES = [
        ('bug', 'Bug'),
        ('feature', 'Feature'),
        ('task', 'Task')
    ]

    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)

    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name='issues'
    )

    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='todo')
    priority = models.CharField(max_length=30, choices=PRIORITY_CHOICES)
    tag = models.CharField(max_length=30, choices=TAG_CHOICES)

    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='issues_created'
    )
    assigned_to = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='assigned_issues',
        blank=True,
        null=True,
    )

    created_time = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    description = models.TextField()
    issue = models.ForeignKey(
        to=Issue,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posted_comments'
    )
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

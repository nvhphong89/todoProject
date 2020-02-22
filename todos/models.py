from django.db import models
from django.utils import timezone
from datetime import date
from django.contrib.auth.models import User


class todos(models.Model):
    content = models.TextField()
    createdDate = models.DateTimeField(default=timezone.now)
    isCompleted = models.BooleanField(default=False)
    dueDate = models.DateField(default=None, null=True, blank=True)
    note = models.TextField(default='')
    starred = models.BooleanField(default=False)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)

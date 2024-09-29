from django.db import models
from user.models import User

# Create your models here.
# apparently the created_by is not CASCADE
# try getting to know about this
class Event(models.Model):
    title = models.CharField(max_length=150, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=150, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True) 
from django.db import models
from user.models import User
from event.models import Event

# Create your models here.
# Fields: user, event, registered_at.
class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    registered_at = models.DateField(auto_now_add=True)
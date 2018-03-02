from django.db import models
from roster.models import Student
from django.contrib.auth.models import User

# Create your models here.
class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL)

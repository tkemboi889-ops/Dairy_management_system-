from django.db import models
from django.contrib.auth.models import AbstractUser

class Management(AbstractUser):
   phone_number = models.CharField(max_length=15, null=True, blank=True)

 
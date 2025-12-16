from django import models
from django.conf import Settings
from django.contrib.auth.models import AbstractUser
user=Settings.AUTH_USER_MODEL

class user(AbstractUser):
 phone_number=models.IntegerField()
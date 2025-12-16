from django.db import models
from django.contrib.auth.models import AbstractUser

class management(AbstractUser):
 phone_number=models.IntegerField()

 
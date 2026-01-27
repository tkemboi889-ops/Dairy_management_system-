from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class ManagementManager(BaseUserManager):
    def create_user(self, username, password=None, phone_number=None, **extra_fields):
        if not username:
            raise ValueError("The username must be set")

        user = self.model(
            username=username,
            phone_number=phone_number,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(username, password, **extra_fields)


class Management(AbstractUser):
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    objects = ManagementManager()



 

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class ManagementManager(BaseUserManager):
    def create_user(self, username, password=None, phone_number=None, **extra_fields):
        if not username:
            raise ValueError("Username is required.")

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

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(
            username=username,
            password=password,
            **extra_fields
        )


class Management(AbstractUser):
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        blank=True
    )

    objects = ManagementManager()

    def __str__(self):
        return self.username


 
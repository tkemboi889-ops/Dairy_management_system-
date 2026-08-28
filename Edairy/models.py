from django.db import models

# Create your models here.

from django.conf import settings # Import settings

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from datetime import date

# farm_manager model
class farm_manager(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    phone_number = models.CharField(
        max_length=15,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user.username

# cow model
class Cow(models.Model):

    SEX_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
    ]

    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("PREGNANT", "Pregnant"),
        ("SICK", "Sick"),
        ("DRY", "Dry"),
        ("SOLD", "Sold"),
        ("DEAD", "Dead"),
    ]

    name = models.CharField(max_length=50)

    breed = models.CharField(max_length=20)

    sex = models.CharField(
        choices=SEX_CHOICES,
        max_length=1
    )

    date_of_birth = models.DateField(null=True,blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ACTIVE"
    )

    farm_manager = models.ForeignKey(
        farm_manager,
        on_delete=models.CASCADE,
        related_name="cows"
    )
    def clean(self):

     if self.status == "PREGNANT" and self.sex != "F":
        raise ValidationError(
            "Only female cows can be pregnant."
        )
    def get_age(self):
        today = date.today()

        age = today.year - self.date_of_birth.year

        if (
            today.month,
            today.day
        ) < (
            self.date_of_birth.month,
            self.date_of_birth.day
        ):
            age -= 1

        return age

    def __str__(self):
        return self.name

    

# 3. Calf Model
class Calf(models.Model):

    SEX_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
    ]

    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("SICK", "Sick"),
        ("SOLD", "Sold"),
        ("DEAD", "Dead"),
    ]

    name = models.CharField(max_length=20)

    breed = models.CharField(max_length=20)

    sex = models.CharField(
        choices=SEX_CHOICES,
        max_length=1
    )

    date_of_birth = models.DateField(null=True,blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ACTIVE"
    )

    cow = models.ForeignKey(
        Cow,
        on_delete=models.CASCADE,
        related_name="calves"
    )

    def get_age(self):

        today = date.today()

        age = today.year - self.date_of_birth.year

        if (
            today.month,
            today.day
        ) < (
            self.date_of_birth.month,
            self.date_of_birth.day
        ):
            age -= 1

        return age

    def __str__(self):
        return self.name

# 4. Milk Model
class Milk(models.Model):
    amount_in_litres = models.FloatField()
    date_collected = models.DateField(auto_now_add=True)
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE, related_name='milk_records')

    def __str__(self):
        return f"{self.amount_in_litres} L from {self.cow.name}"

# 5. Feed Model
class Feed(models.Model):
    name = models.CharField(max_length=20)
    store_number = models.IntegerField()
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE, related_name='feeds')

    def __str__(self):
        return self.name

# 6. Worker Profile
class Worker(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    # A worker can be assigned to multiple cows
    cows = models.ManyToManyField(Cow, blank=True, related_name='workers')

    def __str__(self):
        return self.user.username
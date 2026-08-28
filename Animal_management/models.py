from django.db import models
from Edairy .models import Cow
from django.core.exceptions import ValidationError

# Create your models here.
class BreedingRecord(models.Model):

    cow = models.ForeignKey(
        Cow,
        on_delete=models.CASCADE,
        related_name="breeding_records"
    )

    breeding_date = models.DateField()

    expected_calving_date = models.DateField()

    is_successful = models.BooleanField(
        default=False
    )

    notes = models.TextField(
        blank=True
    )

    def clean(self):

        if self.cow.sex != "F":
            raise ValidationError(
                "Only female cows can have breeding records."
            )

        if self.cow.status in ["DEAD", "SOLD"]:
            raise ValidationError(
                "Cannot breed a dead or sold cow."
            )

    def __str__(self):
        return f"{self.cow.name} - {self.breeding_date}"
    
    # animal health recording
class AnimalHealthRecord(models.Model):

    HEALTH_STATUS = [
        ("HEALTHY", "Healthy"),
        ("SICK", "Sick"),
        ("RECOVERED", "Recovered"),
    ]

    cow = models.ForeignKey(
        Cow,
        on_delete=models.CASCADE,
        related_name="health_records"
    )

    diagnosis = models.CharField(
        max_length=200
    )

    treatment = models.TextField()

    date_recorded = models.DateField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=20,
        choices=HEALTH_STATUS,
        default="SICK"
    )

    def __str__(self):
        return f"{self.cow.name} - {self.diagnosis}"
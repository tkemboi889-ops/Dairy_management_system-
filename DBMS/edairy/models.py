from django.db import models
from django.conf import settings # Import settings

# 1. Owner Profile
class Owner(models.Model):
    # Link to the centralized User model
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.user.username

# 2. Cow Model
class Cow(models.Model):
    SEX_CHOICES = [("M", "Male"), ("F", "Female")]
    
    name = models.CharField(max_length=50)
    breed = models.CharField(max_length=20)
    sex = models.CharField(choices=SEX_CHOICES, max_length=1)
    age = models.IntegerField()
    # Link Cow to Owner
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='cows')

    def __str__(self):
        return self.name

# 3. Calf Model
class Calf(models.Model):
    SEX_CHOICES = [("M", "Male"), ("F", "Female")]
    
    name = models.CharField(max_length=20)
    breed = models.CharField(max_length=20)
    sex = models.CharField(choices=SEX_CHOICES, max_length=1)
    age = models.IntegerField()
    # Link Calf to Mother Cow
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE, related_name='calves')

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
    phone_number = models.CharField(max_length=15)
    # A worker can be assigned to multiple cows
    cows = models.ManyToManyField(Cow, blank=True, related_name='workers')

    def __str__(self):
        return self.user.username
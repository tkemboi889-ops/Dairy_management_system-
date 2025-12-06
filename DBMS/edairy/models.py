from django.db import models
from django.contrib.auth.models import User

class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Cow(models.Model):
    name = models.CharField(max_length=50)
    breed = models.CharField(max_length=20)
    sex = models.CharField(choices=[("M","Male"),("F","Female")],max_length=20)
    age = models.IntegerField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.name


class Calf(models.Model):
    name = models.CharField(max_length=20)
    breed = models.CharField(max_length=20)
    sex = models.CharField(choices=[("M","Male"),("F","Female")],max_length=20)
    age = models.IntegerField()
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Milk(models.Model):
    amount_in_litres = models.FloatField()
    date_collected = models.DateField(auto_now_add=True)
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.amount_in_litres} L from {self.cow.name}"


class Feed(models.Model):
    name = models.CharField(max_length=20)
    store_number = models.IntegerField()
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Worker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    cow = models.ManyToManyField(Cow,blank=True )

    def __str__(self):
        return self.user.username

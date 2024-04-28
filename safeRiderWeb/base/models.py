from django.contrib.auth.models import AbstractUser
from django.db import models


class City(models.Model):
    city_name = models.CharField(max_length=50, unique=True, null=True)

    def __str__(self):
        return self.city_name


class Location(models.Model):
    location_name = models.CharField(max_length=50, unique=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
    latitude = models.CharField(max_length=50, unique=True, null=True)
    longitude = models.CharField(max_length=50, unique=True, null=True)

    def __str__(self):
        return self.location_name


class Gender(models.Model):
    gender_name = models.CharField(max_length=50, unique=True, null=True)

    def __str__(self):
        return self.gender_name


class Stage(models.Model):
    stage_name = models.CharField(max_length=50, unique=True, null=True)
    stage_number = models.CharField(max_length=10, unique=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.stage_name


class StageAdmin(models.Model):
    name = models.CharField(max_length=20, unique=True, null=True)
    id_number = models.CharField(max_length=20, unique=True, null=True)

    def __str__(self):
        return self.id_number


class User(AbstractUser):
    first_name = models.CharField(max_length=200, null=True)
    second_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, null=True)
    email = models.EmailField(unique=True, null=True)
    phone_number = models.CharField(max_length=12, unique=True, null=True)
    id_number = models.CharField(max_length=20, unique=True, null=True)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, null=True)
    motorbike_reg_number = models.CharField(max_length=20, unique=True, null=True)
    is_emergency_contact = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.upper()
        self.second_name = self.second_name.upper()
        self.last_name = self.last_name.upper()
        self.motorbike_reg_number = self.motorbike_reg_number.upper()
        super().save(*args, **kwargs)


class EmergencyContact(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name.username


class Customer(models.Model):
    boda_name = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    customer_phone_number = models.CharField(max_length=12, null=True)
    fare_transaction_id = models.CharField(max_length=20, null=True)
    amount = models.CharField(max_length=20, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.amount


class Emergency(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    lon = models.CharField(max_length=20, null=True)
    lat = models.CharField(max_length=20, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    is_read = models.BooleanField(default=False, null=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.sender.email

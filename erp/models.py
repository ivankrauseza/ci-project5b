from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    website = models.URLField()
    tax_id = models.CharField(max_length=50, unique=True)
    vat_id = models.CharField(max_length=50, unique=True)
    reg_id = models.CharField(max_length=50, unique=True)
    incorporation_date = models.DateField()

    def __str__(self):
        return self.name


class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}'s Staff Profile"
    

# class Downloads(models.Model):

# class Department(models.Model):

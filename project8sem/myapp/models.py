from django.db import models
from django.conf import settings
from django.conf.urls.static import static
import os 

# Create your models here.
class Test(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Use CharField for storing passwords

    class Meta:
        db_table = 'test'

class UserRegistration(models.Model):
    firstname = models.CharField(max_length=50)
    middlename = models.CharField(max_length=50, blank=True, null=True)

    lastname = models.CharField(max_length=50)
    phonenumber = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()

    class Meta:
        db_table = 'user_registration'

class UserProfile(models.Model):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)


    class Meta:
        db_table = 'usersignup'

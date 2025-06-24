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
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


        
def get_notice_image_upload_path(instance, filename):
    return f'notices/{instance.id}/{filename}'

class Notice(models.Model):
    notice_header = models.CharField(max_length=255)
    notice_img = models.ImageField(upload_to=get_notice_image_upload_path)
    notice_description = models.TextField()
    

    class Meta:
        db_table='notices'


    def __str__(self):
        return self.notice_header
    


    
def profile_picture_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/candidates/<email>/<filename>
    return f'profile_picture/{instance.email}/{filename}'


class ProfilePicture(models.Model):

    email = models.EmailField()
    photo_front = models.ImageField(upload_to=profile_picture_path)

    class Meta:
        db_table='profilepicture'


    def __str__(self):
        return self.email

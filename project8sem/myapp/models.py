from django.db import models
from django.conf import settings
from django.conf.urls.static import static
import os 


class UserRegistration(models.Model):
    firstname = models.CharField(max_length=50)
    middlename = models.CharField(max_length=50, blank=True, null=True)

    lastname = models.CharField(max_length=50)
    phonenumber = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()

    class Meta:
        db_table = 'user_registration'

class Test(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Use CharField for storing passwords

    class Meta:
        db_table = 'test'




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


class EmailVerification(models.Model):
    email = models.EmailField()
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta: 
        db_table = 'emailverification'





def kyc_photo_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/candidates/<email>/<filename>
    return f'kyc_verification_photos/{instance.email}/{filename}'




class KycRegistration(models.Model):
    email = models.EmailField()
    citizenship_number = models.CharField(max_length=20)
    voter_id = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('others', 'Others'),
    ])
    country = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    municipality = models.CharField(max_length=100)
    ward_no = models.IntegerField()
    photo_front = models.ImageField(upload_to=kyc_photo_path)
    photo_voter = models.ImageField(upload_to=kyc_photo_path)
    photo_citizenship_front = models.ImageField(upload_to=kyc_photo_path)
    photo_citizenship_back = models.ImageField(upload_to=kyc_photo_path)
    face_coordinates = models.JSONField(null=True, blank=True)  # Added for facial coordinates
    face_descriptor = models.JSONField(null=True, blank=True)
    class Meta:
        db_table = 'kycregistration'

    def __str__(self):
        return f'Registration {self.id} - {self.citizenship_number}' 
    



def candidate_photo_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/candidates/<email>/<filename>
    return f'candidates/{instance.email}/{filename}'

class CandidateProfile(models.Model):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    ROLE_CHOICES = [
        ('MP', 'Member of Parliament'),
        ('Mayor', 'Mayor'),
        ('Deputy Mayor', 'Deputy Mayor'),
        ('Ward Chairperson', 'Ward Chairperson'),
    ]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)

    POLITICAL_PARTY_CHOICES = [
        ('CPN-UML', 'CPN-UML'),
        ('Nepali Congress', 'Nepali Congress'),
        ('Maoist', 'Communist Party of Nepal (Maoist Centre)'),
        ('Samajwadi', 'Samajwadi Party Nepal'),
    ]
    political_party = models.CharField(max_length=100, choices=POLITICAL_PARTY_CHOICES)
    
    district = models.CharField(max_length=100)
    municipality = models.CharField(max_length=100)
    ward = models.IntegerField()
    profile_picture = models.ImageField(upload_to=candidate_photo_path )
    citizenship_front = models.ImageField(upload_to=candidate_photo_path)
    citizenship_back = models.ImageField(upload_to=candidate_photo_path)


    class Meta:
        db_table='candidateprofile'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'  


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
    

class Kycverified(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    verified_time = models.DateTimeField(auto_now_add=True)
    verified_by = models.EmailField(max_length=254)

    class Meta:
        db_table='kycverified'

    def __str__(self):
        return self.email 
    

    

class KycRequest(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=15)
    citizenship_number = models.CharField(max_length=20)
    voter_id = models.CharField(max_length=20)

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'kycrequests'



class KycRejected(models.Model):
    email = models.EmailField(max_length=254)
    date_rejected = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'kycrejected'

    def __str__(self):
        return self.email


def profile_picture_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/candidates/<email>/<filename>
    return f'profile_picture/{instance.email}/{filename}'


class ProfilePicture(models.Model):
    

    email = models.EmailField(unique=True)
    photo_front = models.ImageField(upload_to=kyc_photo_path)


    class Meta:
        db_table='profilepicture'


    def __str__(self):
        return self.email
    

class VoteStatus(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table='votestatus'

    def __str__(self):
        return self.email
    
class MpVote(models.Model):
    voter_email = models.EmailField(null=True, blank=True)  
    candidate_email = models.EmailField(null=True, blank=True)
    district = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Mpvote'
        unique_together = ('voter_email',)

class MayorVote(models.Model):
    voter_email = models.EmailField(max_length=254, unique=True)  # voter_email for the voter (unique)
    candidate_email = models.EmailField(null=True, blank=True)
    municipality = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Mayourvote'

    def __str__(self):
        return f'{self.voter_email} - {self.municipality}'


class DeputymayorVote(models.Model):
    voter_email = models.EmailField(max_length=254, unique=True)
    candidate_email = models.EmailField(null=True, blank=True)
    municipality = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Deputyvote'

    def __str__(self):
        return f'{self.voter_email} - {self.municipality}'


class WardVote(models.Model):
    voter_email = models.EmailField(max_length=254, unique=True)
    candidate_email = models.EmailField(null=True, blank=True)
    wardno = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Wardvote'

    def __str__(self):
        return f'{self.voter_email} - Ward {self.wardno}'

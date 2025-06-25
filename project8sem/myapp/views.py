from django.shortcuts import render, redirect,get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login as auth_login

from django.contrib import messages
from .models import Test
from .models import UserRegistration

from .models import UserProfile
from .models import CandidateProfile
from .models import Notice
from .models import Kycverified
from .models import KycRequest
from .models import KycRejected
from .models import ProfilePicture
from .models import MpVote
from .models import MayorVote
from .models import DeputymayorVote
from .models import WardVote
from .models import VoteStatus



#from .models import candidate_photo_path

from .models import KycRegistration

from datetime import datetime
from django.contrib.auth.hashers import make_password

from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.utils.dateparse import parse_date
from django.db.models import Count








from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.utils import timezone
from .models import EmailVerification


import io
from io import BytesIO
import base64
from datetime import date

import matplotlib.pyplot as plt

from django.conf import settings

import os




def register_user(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        date_of_birth = request.POST.get('date_of_birth')

        user = UserRegistration(
            firstname=first_name,
            middlename=middle_name,
            lastname=last_name,
            phonenumber=phone_number,
            email=email,
            date_of_birth=date_of_birth
        )
        user.save()
        return redirect('user_signup')  # Ensure 'success_page' is a valid URL name
    return render(request, 'myapp/register.html') 




#####Login Authentication (Backup Code)
'''def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            admin = Test.objects.get(email=email)

            # Check if the provided password matches the stored password
            if password == admin.password:
                # Passwords match, login successful
                request.session['admin_id'] = admin.id
                messages.success(request, 'Login successful!')
                return redirect('base')
            else:
                # Passwords do not match
                messages.error(request, 'Invalid email or password.')
        except Test.DoesNotExist:
            # User with the provided email does not exist
            messages.error(request, 'Invalid email or password.')

    return render(request, 'myapp/admin_login.html')

'''


##### New Code 

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:  # Check if email or password is empty
            messages.error(request, 'Email or Password cannot be empty.')
            return render(request, 'myapp/admin_login.html')  # Render the login page with the error message

        try:
            admin = Test.objects.get(email=email)

            # Check if the provided password matches the stored password
            if password == admin.password:

                request.session['admin_verified'] = True
                request.session['admin_id'] = admin.id
                request.session['email']=admin.email
                messages.success(request, 'You Are Logged In')
                return redirect('base')
            else:
                # Passwords do not match
                messages.error(request, 'Invalid email or password.')
        except Test.DoesNotExist:
            # User with the provided email does not exist
            messages.error(request, 'Invalid email or password.')

    return render(request, 'myapp/admin_login.html')



def adminlogout(request):
    request.session.flush()
  # Delete the admin_id session variable
    return render(request,'myapp/admin_login.html')













####String login is successfull 

'''
def userlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:  # Check if email or password is empty
            messages.error(request, 'Email or Password cannot be empty.')
            return render(request, 'myapp/admin_login.html')  # Render the login page with the error message

        try:
            admin = UserProfile.objects.get(email=email)

            # Check if the provided password matches the stored password
            if password == admin.password:
                # Passwords match, login successful
                request.session['admin_id'] = admin.id
                messages.success(request, 'You Are Logged In')
                return redirect('home')
            else:
                # Passwords do not match
                messages.error(request, 'Invalid email or password.')
        except UserProfile.DoesNotExist:
            # User with the provided email does not exist
            messages.error(request, 'Invalid email or password.')

    return render(request, 'myapp/user_login.html')  '''







def userlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:  # Check if email or password is empty
            messages.error(request, 'Email or Password cannot be empty.')
            return render(request,'myapp/user_login.html') # Render the login page with the error message

        try:
            admin = UserProfile.objects.get(email=email)

            

             # Check if the provided password matches the stored hashed password
            if check_password(password, admin.password):
                request.session['user_verified'] = True
                # Passwords match, login successful
                request.session['admin_id'] = admin.id
                request.session['email']=admin.email
                messages.success(request, 'You Are Logged In')
                return redirect('home')
            else:
                # Passwords do not match
                messages.error(request, 'Invalid email or password.')
        except UserProfile.DoesNotExist:
            # User with the provided email does not exist
            messages.error(request, 'Email is not Registered.')

    return render(request, 'myapp/user_login.html')



def base(request):
    if not request.session.get('admin_verified'):
        return redirect('login')  # Redirect to verify_email if page_a is not completed
    return render(request,'myapp/base.html')


def hello(request):
    return render(request,'myapp/hello.html')




def admin_login(request):
    return render(request,'myapp/admin_login.html')

def add_user(request):
    return render(request,'myapp/add_user.html')

def home(request):
    users = UserProfile.objects.all()
    return render(request ,'myapp/home.html', {'users': users})




def signup(request):
    if request.method == 'POST':
        # Retrieve form data
        first_name = request.POST.get('first_name')  # Update to match your HTML form field name
        middle_name = request.POST.get('middle_name', '')  # Update to match your HTML form field name
        last_name = request.POST.get('last_name')  # Update to match your HTML form field name
        dob = request.POST.get('dob')  # Update to match your HTML form field name
        phone_number = request.POST.get('phonenumber')  # Update to match your HTML form field name
        email = request.POST.get('email')  # Update to match your HTML form field name
        password = request.POST.get('password')  # Update to match your HTML form field name
        confirm_password = request.POST.get('cpassword')  # Update to match your HTML form field name

        # Check if email or phone number is already registered
        if UserProfile.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return redirect('signup')  # Redirect to the signup page
        elif UserProfile.objects.filter(phone_number=phone_number).exists():
            messages.error(request, 'Phone number is already registered.')
            return redirect('signup')  # Redirect to the signup page

        # Save the user profile
        user_profile = UserProfile.objects.create(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            dob=dob,
            phone_number=phone_number,
            email=email,
            password=make_password(password)  # Hash the password before storing
        )
        # Optionally, you might want to hash the password before saving it in the database

        # Redirect to the home page
        messages.success(request, 'Register successful!')
        return redirect('userlogin')

    return render(request, 'myapp/user_signup.html')





def adduser(request):
    if not request.session.get('admin_verified'):
        return redirect('login')
    if request.method == 'POST':
        # Retrieve form data
        first_name = request.POST.get('first_name')  # Update to match your HTML form field name
        middle_name = request.POST.get('middle_name', '')  # Update to match your HTML form field name
        last_name = request.POST.get('last_name')  # Update to match your HTML form field name
        dob = request.POST.get('dob')  # Update to match your HTML form field name
        phone_number = request.POST.get('phonenumber')  # Update to match your HTML form field name
        email = request.POST.get('email')  # Update to match your HTML form field name
        password = request.POST.get('password')  # Update to match your HTML form field name
        confirm_password = request.POST.get('cpassword')  # Update to match your HTML form field name

        # Check if email or phone number is already registered
        if UserProfile.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return redirect('adduser')  # Redirect to the signup page
        elif UserProfile.objects.filter(phone_number=phone_number).exists():
            messages.error(request, 'Phone number is already registered.')
            return redirect('adduser')  # Redirect to the signup page

        # Save the user profile
        user_profile = UserProfile.objects.create(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            dob=dob,
            phone_number=phone_number,
            email=email,
           password=make_password(password)  # Hash the password before storing
        )
        # Optionally, you might want to hash the password before saving it in the database

        # Redirect to the home page
        messages.success(request, 'User Added  successful!')
        return redirect('base')

    return render(request, 'myapp/add_user.html')



'''
def search_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = UserProfile.objects.get(email=email)
            return render(request, 'myapp/edit_user.html', {'user': user})
        except UserProfile.DoesNotExist:
            messages.error(request, 'Email is not  registered.')
            return redirect('edituser')  
    return render(request, 'myapp/edit_user.html')  '''


'''def updateuser(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = UserProfile.objects.get(email=email)
        user.first_name = request.POST.get('first_name')  # Update to match your HTML form field name
        user.middle_name = request.POST.get('middle_name', '')  # Update to match your HTML form field name
        user.last_name = request.POST.get('last_name')  # Update to match your HTML form field name
        user.dob = request.POST.get('dob')  # Update to match your HTML form field name
        user.phone_number = request.POST.get('phonenumber')  # Update to match your HTML form field name
        user.email = request.POST.get('email')  # Update to match your HTML form field name
        user.password = request.POST.get('password')  # Update to match your HTML form field name
        user.confirm_password = request.POST.get('cpassword')  # Update to match your HTML form field name

        # Update other fields similarly
        user.save()
        messages.success(request, 'User has been edited')
        return redirect('dashboard')  # Redirect to dashboard or any other page after updating
    return redirect('edit_user')'''







'''

def update_user(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        dob = request.POST.get('dob')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        

        try:
            user = UserProfile.objects.get(email=email)
            user.first_name = first_name
            user.middle_name = middle_name
            user.last_name = last_name
            user.dob = dob
            user.phone_number = phone_number##hashing it
            user.password = make_password(password)  # Note: In a real application, you'd hash the password
            user.save()
            messages.success(request, 'User updated successfully')
        except UserProfile.DoesNotExist:
            messages.error(request, 'User does not exist')

        return redirect('edituser')

    return render(request, 'myapp/edit_user.html')  '''



#### 1st step of Edit the User using admin code or to search email exist in the database or not code 
def edituser(request):
    
    if not request.session.get('admin_verified'):
        return redirect('login') 
    if request.method == 'POST':
        email = request.POST.get('semail')
        try:
            user = UserProfile.objects.get(email=email)
            messages.success(request, 'User with this email does  exist.')
            return render(request, 'myapp/edit_user.html', {'user': user})
        except UserProfile.DoesNotExist:
            messages.error(request, 'User with this email does not exist.')
            return redirect('edituser')
    return render(request, 'myapp/edit_user.html', {'email_exists': False})



#### update the user information  using admin code 
def update_user(request):
     
    if not request.session.get('admin_verified'):
        return redirect('login') 
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        dob = request.POST.get('dob')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')

        # Validate email
        if not email:
            messages.error(request, 'Email field cannot be empty.')
            return redirect('edituser')

        # Validate other fields (similar validation logic can be applied here)
        if not first_name or not last_name or not dob or not phone_number:
            messages.error(request, 'All fields except middle name must be filled.')
            return redirect('edituser')

        try:
            user = UserProfile.objects.get(email=email)
            
            # Update only the specified fields
            user.first_name = first_name
            user.middle_name = middle_name
            user.last_name = last_name
            user.dob = dob
            user.phone_number = phone_number
            
            user.save()
            messages.success(request, 'User details updated successfully.')
        except UserProfile.DoesNotExist:
            messages.error(request, 'User with this email does not exist.')
            return redirect('edituser')

        return redirect('edituser')
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('edituser')


#### 1st step of Delete the User using admin code or to search email exist in the database or not code 
def deleteuser(request):
     
    if not request.session.get('admin_verified'):
        return redirect('login') 
    if request.method == 'POST':
        email = request.POST.get('semail')


        try:
            user = UserProfile.objects.get(email=email)
            messages.success(request, 'User with this email does  exist.')
            return render(request, 'myapp/delete_user.html', {'user': user})
        except UserProfile.DoesNotExist:
            messages.error(request, 'User with this email does not exist.')
            return redirect('deleteuser')
    return render(request, 'myapp/delete_user.html', {'email_exists': False})


#### update the user information  using admin code 
def delete_user_confirm(request):
    if request.method == 'POST':
        email = request.POST.get('email')


        if not email:
            messages.error(request, 'Email field cannot be empty.')
            return redirect('deleteuser')


        try:
            user = UserProfile.objects.get(email=email)
            user.delete()
            messages.success(request, 'User has been successfully deleted.')
            return redirect('deleteuser')
        except UserProfile.DoesNotExist:
            messages.error(request, 'User with this email does not exist.')
            return redirect('deleteuser')
    return redirect('deleteuser')




##### To view the data of all user of database code 
def view_users(request):
     
    if not request.session.get('admin_verified'):
        return redirect('login') 
    users = UserProfile.objects.all()
    return render(request, 'myapp/view_user.html', {'users': users}) 

#### 1st step of forgot password  to verify email and sent the code to the user email and save otp and email the data in the database in EmailVerification table
# View for verifying email and sending OTP
# View for verifying email and generating OTP
def verify_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if UserProfile.objects.filter(email=email).exists():
            # Email exists in the database
            otp_code = get_random_string(length=6, allowed_chars='1234567890')
            EmailVerification.objects.create(email=email, otp_code=otp_code)
            send_mail(
                'OTP for Email Verification',
                f'Your OTP code to verify your email for Online voting system is: {otp_code}',
                'theapocalypseitproject@gmail.com',
                [email],
                fail_silently=False,
            )

            # Store email and verification status in session
            request.session['email'] = email
            request.session['page_a_completed'] = True
            request.session['page_b_completed'] = False

            messages.success(request, 'User has been successfully verified. Please check your email for the OTP.')
            return redirect('verify_otp')  # Redirect to verify_otp.html
        else:
            messages.error(request, 'User with this email is not registered.')
            return redirect('verify_email')
    return render(request, 'myapp/verify_email.html')

# View for verifying OTP and redirecting to update password page
def verify_otp(request):
    if not request.session.get('page_a_completed'):
        return redirect('userlogin')  # Redirect to verify_email if page_a is not completed

    email = request.session.get('email')
    if request.method == 'POST':
        otp = request.POST.get('otp')
        email_verification = EmailVerification.objects.filter(email=email, otp_code=otp).first()
        if email_verification:
            # OTP is correct
            request.session['page_b_completed'] = True
            request.session['page_a_completed'] = False  # Clear Page A session data
            messages.success(request, 'Email verified successfully.')
            return redirect('update_password')  # Redirect to update_password.html
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
    return render(request, 'myapp/verify_otp.html')

# View for updating the password after validation
def update_password(request):
    if not request.session.get('page_b_completed'):
        return redirect('userlogin')  # Redirect to verify_otp if page_b is not completed

    email = request.session.get('email')
    if request.method == 'POST':
        new_password = request.POST.get('npassword')
        confirm_password = request.POST.get('ncpassword')

        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match. Please try again.')
            return render(request, 'myapp/update_password.html')

        user = UserProfile.objects.get(email=email)  # Retrieve the user object
        hashed_password = make_password(new_password)  # Hash the new password
        user.password = hashed_password  # Set the hashed password
        user.save()

        # Clear all session data after successful password update
        request.session.flush()

        messages.success(request, 'Your password was successfully updated!')
        return redirect('userlogin')  # Redirect to login page
    return render(request, 'myapp/update_password.html')


def view_otp(request):
    users = EmailVerification.objects.all()
    return render(request, 'myapp/view_otp.html', {'users': users}) 








def home(request):
    users = UserProfile.objects.all()
    user_profile_picture = None
    user_full_name = None

    email = request.session.get('email')
    if email:
        try:
            user_profile = get_object_or_404(UserProfile, email=email)
            user_full_name = f"{user_profile.first_name} {user_profile.middle_name} {user_profile.last_name}"

            try:
                profile_picture = ProfilePicture.objects.get(email=email)
                user_profile_picture = profile_picture.photo_front.url
            except ProfilePicture.DoesNotExist:
                pass

        except UserProfile.DoesNotExist:
            pass

    return render(request, 'myapp/home.html', {
        'users': users,
        'user_profile_picture': user_profile_picture,
        'user_full_name': user_full_name,
    })

def contact(request):
    if not request.session.get('user_verified'):
        return redirect('userlogin')
  
    users = UserProfile.objects.all()
    user_profile_picture = None
    user_full_name = None

    email = request.session.get('email')
    if email:
        try:
            profile_picture = ProfilePicture.objects.get(email=email)
            user_profile_picture = profile_picture.photo_front.url
        except ProfilePicture.DoesNotExist:
            pass

        try:
            user_profile = UserProfile.objects.get(email=email)
            user_full_name = f"{user_profile.first_name} {user_profile.middle_name} {user_profile.last_name}"
        except UserProfile.DoesNotExist:
            pass

    return render(request, 'myapp/contact.html', {
        'users': users,
        'user_profile_picture': user_profile_picture,
        'user_full_name': user_full_name,
    })

def notices(request):
    if not request.session.get('user_verified'):
        return redirect('userlogin')

    notices = Notice.objects.all()
    user_profile_picture = None
    user_full_name = None

    email = request.session.get('email')
    if email:
        try:
            profile_picture = ProfilePicture.objects.get(email=email)
            user_profile_picture = profile_picture.photo_front.url
        except ProfilePicture.DoesNotExist:
            pass

        try:
            user_profile = UserProfile.objects.get(email=email)
            user_full_name = f"{user_profile.first_name} {user_profile.middle_name} {user_profile.last_name}"
        except UserProfile.DoesNotExist:
            pass

    return render(request, 'myapp/notices.html', {
        'notices': notices,
        'user_profile_picture': user_profile_picture,
        'user_full_name': user_full_name,
    })


'''def vote_here(request):
    if not request.session.get('user_verified'):
        return redirect('userlogin')
    return render(request,'myapp/vote.html') '''








def verify_kyc(request):
    if not request.session.get('user_verified'):
        return redirect('userlogin')
    
    emailuser = request.session.get('email')
    user = UserProfile.objects.get(email=emailuser)
    
    # Check if the user's email is already in KycRegistration model
    if KycRegistration.objects.filter(email=emailuser).exists():
        messages.success(request, 'Your KYC has already been submitted')
        return redirect('vote')  # Redirect to vote view with a message
    
    user_full_name = f"{user.first_name} {user.last_name}"
    user_profile_picture = ProfilePicture.objects.filter(email=emailuser).first()

    if request.method == 'POST':
        # Process the form submission
        email = request.POST.get('email')
        citizenship_number = request.POST.get('citizenship_number')
        voter_id = request.POST.get('voter_id')
        gender = request.POST.get('gender')
        country = request.POST.get('country')
        province = request.POST.get('province')
        district = request.POST.get('district')
        municipality = request.POST.get('municipality')
        ward_no = request.POST.get('ward_no')

        # Access the uploaded files
        photo_front = request.FILES.get('photo_front')
        photo_voter = request.FILES.get('photo_voter')
        photo_citizenship_front = request.FILES.get('photo_citizenship_front')
        photo_citizenship_back = request.FILES.get('photo_citizenship_back')

        kyc_request = KycRequest.objects.create(
            email=email,
            phone_number=user.phone_number,  # Assuming phone_number is in UserProfile
            citizenship_number=citizenship_number,
            voter_id=voter_id
        )

        profile_picture = ProfilePicture.objects.create(
            email=email,
            photo_front=photo_front,
        )

        # Save the data to the Registration model
        registration = KycRegistration.objects.create(
            email=email,
            citizenship_number=citizenship_number,
            voter_id=voter_id,
            gender=gender,
            country=country,
            province=province,
            district=district,
            municipality=municipality,
            ward_no=ward_no,
            photo_front=photo_front,
            photo_voter=photo_voter,
            photo_citizenship_front=photo_citizenship_front,
            photo_citizenship_back=photo_citizenship_back
        )

        messages.success(request, 'Your KYC has been submitted successfully')

        # Redirect or return success response
        return redirect('home')

    return render(request, 'myapp/kkyc.html', {'user': user, 'user_full_name': user_full_name, 'user_profile_picture': user_profile_picture})

def get_provinces(request):
    country = request.GET.get('country')
    provinces = {
        "country1": ["Koshi Pradesh", "Madesh Pradesh", "Bagmati Province", "Gandaki Province", "Lumbini Province", "Karnali Province", "Sudurpaschim Province"]
    }
    return JsonResponse(provinces.get(country, []), safe=False)

def get_districts(request):
    province = request.GET.get('province')
    districts = {
        "Koshi Pradesh": ["Bhojpur", "Dhankuta", "Ilam", "Jhapa", "Khotang", "Morang", "Okhaldhunga", "Panchthar", "Sankhuwasabha", "Solukhumbu", "Sunsari", "Taplejung", "Terhathum", "Udayapur"],
        "Madesh Pradesh": ["Saptari", "Siraha", "Dhanusha", "Mahottari", "Sarlahi", "Bara", "Parsa", "Rautahat"],
        "Bagmati Province": ["Bhaktapur", "Chitwan", "Dhading", "Dolakha", "Kathmandu", "Kavrepalanchok", "Lalitpur", "Makwanpur", "Nuwakot", "Ramechhap", "Rasuwa", "Sindhuli", "Sindhupalchok"],
        "Gandaki Province": ["Baglung", "Gorkha", "Kaski", "Lamjung", "Manang", "Mustang", "Myagdi", "Nawalpur", "Parbat", "Syangja", "Tanahun"],
        "Lumbini Province": ["Arghakhanchi", "Banke", "Bardiya", "Dang", "Eastern Rukum", "Gulmi", "Kapilvastu", "Parasi", "Palpa", "Pyuthan", "Rolpa", "Rupandehi"],
        "Karnali Province": ["Dailekh", "Dolpa", "Humla", "Jajarkot", "Jumla", "Kalikot", "Mugu", "Salyan", "Surkhet", "Western Rukum"],
        "Sudurpaschim Province": ["Achham", "Baitadi", "Bajhang", "Bajura", "Dadeldhura", "Darchula", "Doti", "Kailali", "Kanchanpur"]
    }
    return JsonResponse(districts.get(province, []), safe=False) 






def addcandidate(request):
    if not request.session.get('admin_verified'):
        return redirect('login')
     
    if request.method == 'POST':
        # Fetch data from the form
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        role = request.POST.get('role')
        political_party = request.POST.get('political_party')
        district = request.POST.get('district')
        municipality = request.POST.get('municipality')
        ward = request.POST.get('ward')
        pp_photo = request.FILES.get('pp_photo')
        front_citizenship = request.FILES.get('front_citizenship')
        back_citizenship = request.FILES.get('back_citizenship')

        if UserProfile.objects.filter(email=email).exists():
            messages.error(request, 'Candidate with email is already registered.')
            return redirect('addcandidate')  # Redirect to the signup page


        # Create a CandidateProfile instance
        candidate_profile = CandidateProfile(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            date_of_birth=dob,
            email=email,
            phone_number=phone,
            role=role,
            political_party=political_party,
            district=district,
            municipality=municipality,
            ward=ward,
            profile_picture=pp_photo,
            citizenship_front=front_citizenship,
           citizenship_back=back_citizenship,
        )


        # Save the candidate profile instance
        candidate_profile.save()

        # Optionally, you can add a success message
        messages.success(request, 'Candidate added successfully.')

        # Redirect to a success page or wherever needed
        return redirect('base')  # Replace 'home' with the URL name of your home page

    # If GET request or form is not valid, render the form again
    return render(request, 'myapp/add_candidate.html') 




def viewcandidate(request):
    if not request.session.get('admin_verified'):
        return redirect('login')
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            candidate = CandidateProfile.objects.get(email=email)
            messages.success(request, 'Candidate has been found')
            return render(request, 'myapp/view_candidate.html', {'candidate': candidate})
        except CandidateProfile.DoesNotExist:
            messages.error(request, 'Candidate with that email doesnot exist')
            return render(request, 'myapp/view_candidate.html', {'error': 'Candidate not found'})
    return render(request, 'myapp/view_candidate.html')



def candidates(request):
    candidates = CandidateProfile.objects.all()
    user_profile_picture = None
    user_full_name = None

    email = request.session.get('email')
    if email:
        try:
            profile_picture = ProfilePicture.objects.get(email=email)
            user_profile_picture = profile_picture.photo_front.url
        except ProfilePicture.DoesNotExist:
            pass

        try:
            user_profile = UserProfile.objects.get(email=email)
            user_full_name = f"{user_profile.first_name} {user_profile.middle_name} {user_profile.last_name}"
        except UserProfile.DoesNotExist:
            pass

    return render(request, 'myapp/candidates.html', {
        'candidates': candidates,
        'user_profile_picture': user_profile_picture,
        'user_full_name': user_full_name,
    })



'''def vote_here(request):
    mp_candidates = CandidateProfile.objects.filter(role='MP')
    mayor_candidates = CandidateProfile.objects.filter(role='Mayor')
    deputy_mayor_candidates = CandidateProfile.objects.filter(role='Deputy Mayor')

    ward_candidate = CandidateProfile.objects.filter(role='Ward Chairperson')

    context = {
        'mp_candidates': mp_candidates,
        'mayor_candidates': mayor_candidates,
        'deputy_mayor_candidates': deputy_mayor_candidates,
        'ward_candidate': ward_candidate,
    }

    return render(request, 'myapp/vote.html', context) '''


def user_logout(request):

    request.session.flush()

    messages.success(request,'you have been successfully logout')

    return redirect('userlogin')


def viewall_candidate(request):
    users = CandidateProfile.objects.all()
    return render(request, 'myapp/viewall_candidate.html', {'users': users})




#### 1st step of Edit the User using admin code or to search email exist in the database or not code 
def editcandidate(request):
    
    if not request.session.get('admin_verified'):
        return redirect('login') 
    if request.method == 'POST':
        email = request.POST.get('semail')
        try:
            user = CandidateProfile.objects.get(email=email)
            messages.success(request, 'Candidate with this email does  exist.')
            return render(request, 'myapp/edit_candidate.html', {'user': user})
        except CandidateProfile.DoesNotExist:
            messages.error(request, 'Candidate with this email does not exist.')
            return redirect('editcandidate')
    return render(request, 'myapp/edit_candidate.html', {'email_exists': False})



#### update the candidate information  using admin code 


def update_candidate(request):
    if not request.session.get('admin_verified'):
        return redirect('login')
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        dob = request.POST.get('dob')
        phone = request.POST.get('phone')
        role = request.POST.get('role')
        political_party = request.POST.get('political_party')
        email = request.POST.get('email')
        district = request.POST.get('district')
        municipality = request.POST.get('municipality')
        ward = request.POST.get('ward')

        # Validate email
        if not email:
            messages.error(request, 'Email field cannot be empty.')
            return redirect('editcandidate')

        # Parse date of birth
        parsed_dob = parse_date(dob)
        if not parsed_dob:
            messages.error(request, 'Invalid date format for date of birth.')
            return redirect('editcandidate')

        try:
            user = CandidateProfile.objects.get(email=email)
            
            # Update only the specified fields
            user.first_name = first_name
            user.middle_name = middle_name
            user.last_name = last_name
            user.date_of_birth = parsed_dob
            user.email = email
            user.phone_number = phone
            user.role = role
            user.political_party = political_party
            user.district = district
            user.municipality = municipality
            user.ward = ward
            
            user.save()
            messages.success(request, 'Candidate details updated successfully.')
        except CandidateProfile.DoesNotExist:
            messages.error(request, 'Candidate with this email does not exist.')
            return redirect('editcandidate')

        return redirect('editcandidate')
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('editcandidate')
    


#### 1st step of Delete the User using admin code or to search email exist in the database or not code 
def deletecandidate(request):
     
    if not request.session.get('admin_verified'):
        return redirect('login') 
    if request.method == 'POST':
        email = request.POST.get('semail')


        try:
            user = CandidateProfile.objects.get(email=email)
            messages.success(request, 'Candidate with this email does  exist.')
            return render(request, 'myapp/delete_candidate.html', {'user': user})
        except CandidateProfile.DoesNotExist:
            messages.error(request, 'Candidate with this email does not exist.')
            return redirect('deletecandidate')
    return render(request, 'myapp/delete_candidate.html', {'email_exists': False})


#### update the user information  using admin code 
def delete_candidate_confirm(request):
    if request.method == 'POST':
        email = request.POST.get('email')


        if not email:
            messages.error(request, 'Email field cannot be empty.')
            return redirect('deletecandidate')


        try:
            user = CandidateProfile.objects.get(email=email)
            user.delete()
            messages.success(request, 'Candidate has been successfully deleted.')
            return redirect('deletecandidate')
        except UserProfile.DoesNotExist:
            messages.error(request, 'Candidate with this email does not exist.')
            return redirect('deletecandidate')
    return redirect('deletecandidate')



def add_notices(request):
    if request.method == 'POST':
        notice_header = request.POST.get('notice_header')
        notice_img = request.FILES.get('notice_img')
        notice_description = request.POST.get('notice_description')
        
        if notice_header and notice_img and notice_description:
            # Create a new Notice instance
            notice = Notice(
                notice_header=notice_header,
                notice_img=notice_img,
                notice_description=notice_description
            )
            notice.save()  # Save the notice to the database
            messages.success(request, 'Notice added successfully.')
            return redirect('add_notices')
        else:
            messages.error(request, 'All fields are required. Please try again.')
    
    return render(request, 'myapp/add_notices.html')



def view_notices(request):
    notices = Notice.objects.all()
    return render(request, 'myapp/view_notices.html', {'notices': notices})


def editnotices(request):
    if not request.session.get('admin_verified'):
        return redirect('login')
    
    if request.method == 'POST':
        id = request.POST.get('semail')
        try:
            notice = Notice.objects.get(id=id)
            messages.success(request, 'Notice with that Id does exist.')
            return render(request, 'myapp/edit_notices.html', {'notice': notice})
        except Notice.DoesNotExist:
            messages.error(request, 'Notice with that Id does not exist.')
            return redirect('editnotices')
    return render(request, 'myapp/edit_notices.html', {'email_exists': False})





def update_notices(request):
    if not request.session.get('admin_verified'):
        return redirect('login')
    
    if request.method == 'POST':
        notice_header = request.POST.get('notice_header')
        notice_img = request.FILES.get('notice_img')
        notice_description = request.POST.get('notice_description')
        notice_id = request.POST.get('id')

        # Validate notice ID
        if not notice_id:
            messages.error(request, 'Id field cannot be empty.')
            return redirect('editnotices')

        try:
            notice = Notice.objects.get(id=notice_id)
            
            # Update the fields
            notice.notice_header = notice_header
            if notice_img:
                notice.notice_img = notice_img
            notice.notice_description = notice_description
            
            notice.save()
            messages.success(request, 'Notice details updated successfully.')
            return redirect('editnotices')
        except Notice.DoesNotExist:
            messages.error(request, 'Notice with this id does not exist.')
            return redirect('editnotices')

        return redirect('editnotices')
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('editnotices')


def deletenotices(request):
    if not request.session.get('admin_verified'):
        return redirect('login')
    
    if request.method == 'POST':
        id = request.POST.get('semail')

        try:
            notice = Notice.objects.get(id=id)
            messages.success(request, 'Notice with that ID exists.')
            return render(request, 'myapp/delete_notices.html', {'notice': notice})
        except Notice.DoesNotExist:
            messages.error(request, 'Notice with that ID does not exist.')
            return redirect('deletenotices')

    return render(request, 'myapp/delete_notices.html', {'email_exists': False})


def delete_notices_confirm(request):
    if request.method == 'POST':
        id = request.POST.get('id')  # Assuming 'notice_id' is the name of the hidden input in your form

        if not id:
            messages.error(request, 'ID field cannot be empty.')
            return redirect('deletenotices')

        try:
            notice = Notice.objects.get(id=id)
            notice.delete()
            messages.success(request, 'Notice has been successfully deleted.')
        except Notice.DoesNotExist:
            messages.error(request, 'Notice with this ID does not exist.')

    return redirect('deletenotices')


def vote(request):
    if not request.session.get('user_verified'):
        return redirect('userlogin')
    
    email = request.session.get('email')
    user = UserProfile.objects.get(email=email)
    
    try:
        profile_picture = ProfilePicture.objects.get(email=email)
        user_profile_picture = profile_picture.photo_front.url if profile_picture.photo_front else None
    except ObjectDoesNotExist:
        user_profile_picture = None  # Handle case where profile picture doesn't exist
    
    user_verified = Kycverified.objects.filter(email=email).exists()
    kycrequest = KycRequest.objects.filter(email=email).exists()
    kycreject = KycRejected.objects.filter(email=email).exists()
    votestatus = VoteStatus.objects.filter(email=email).exists()

    try:
        kyc_details = KycRegistration.objects.get(email=email)
        mp_candidates = CandidateProfile.objects.filter(role='MP', district=kyc_details.district)
        mayor_candidates = CandidateProfile.objects.filter(role='Mayor', municipality=kyc_details.municipality)
        deputy_mayor_candidates = CandidateProfile.objects.filter(role='Deputy Mayor', municipality=kyc_details.municipality)
        ward_candidate = CandidateProfile.objects.filter(role='Ward Chairperson', ward=kyc_details.ward_no)
    except KycRegistration.DoesNotExist:

        messages.error(request,"Submit your Kyc First")
        # Handle the case where KycRegistration doesn't exist
        return redirect('verify_kyc')  # Redirect to an error page or display a message



    context = {
        'votestatus': votestatus,
        'kycreject': kycreject,
        'kycrequest': kycrequest,
        'user_verified': user_verified,
        'mp_candidates': mp_candidates,
        'mayor_candidates': mayor_candidates,
        'deputy_mayor_candidates': deputy_mayor_candidates,
        'ward_candidate': ward_candidate,
        'user_full_name': f"{user.first_name} {user.last_name}",
        'user_profile_picture': user_profile_picture,
    }

    return render(request, 'myapp/vote_here.html', context)



def view_kycrequest(request):
    requests = KycRequest.objects.all()
    return render(request, 'myapp/view_kycrequest.html', {'requests': requests})


def view_kyc(request, request_id):
    kyc_request = get_object_or_404(KycRequest, pk=request_id)
    kyc_registration = get_object_or_404(KycRegistration, email=kyc_request.email)
    user_profile = get_object_or_404(UserProfile, email=kyc_registration.email)
    
    return render(request, 'myapp/view_kyc.html', {
        'kyc_registration': kyc_registration,
        'user_profile': user_profile,
        'kyc_request': kyc_request,
    })


def accept_kyc(request, request_id):
    kyc_request = get_object_or_404(KycRequest, pk=request_id)
    
    # Create KycVerified instance
    Kycverified.objects.create(
        email=kyc_request.email,
        verified_by=request.session['email'],  # Assuming admin email is in session
    )
    
    # Delete KycRequest instance
    kyc_request.delete()

    messages.success(request,"KYC accepted succesfully")
    
    return redirect('view_kycrequest') 



def reject_kyc(request, request_id):
    kyc_request = get_object_or_404(KycRequest, pk=request_id)
    
    # Create KycVerified instance
    KycRejected.objects.create(
        email=kyc_request.email,
        
    )
    
    # Delete KycRequest instance
    kyc_request.delete()

    messages.error(request,"KYC rejected succesfully")
    
    return redirect('view_kycrequest') 



def view_verifiedkyc(request):
    users = Kycverified.objects.all()
    return render(request, 'myapp/view_verifiedkyc.html', {'users': users})

def view_rejectedkyc(request):
    users = KycRejected.objects.all()
    return render(request, 'myapp/view_rejectedkyc.html', {'users': users})

def edit_profile(request):
    if not request.session.get('user_verified'):
        return redirect('userlogin')

    email = request.session.get('email')

    kyc_verified = Kycverified.objects.filter(email=email).first()
    kyc_reject = KycRejected.objects.filter(email=email).first()
    kyc_registration = KycRegistration.objects.filter(email=email).first()
    vote_status = VoteStatus.objects.filter(email=email).first()
    
    user_profile = UserProfile.objects.filter(email=email).first()
    if user_profile:
        user_full_name = f"{user_profile.first_name} {user_profile.middle_name} {user_profile.last_name}"
    else:
        user_full_name = None

    profile_picture = ProfilePicture.objects.filter(email=email).first()
    if profile_picture:
        user_profile_picture = profile_picture.photo_front.url
    else:
        user_profile_picture = None

    if request.method == 'POST':
        if 'photo_front' in request.FILES:
            photo_front = request.FILES['photo_front']
            # Update or create profile picture
            if profile_picture:
                profile_picture.photo_front = photo_front
                profile_picture.save()
            else:
                ProfilePicture.objects.create(email=email, photo_front=photo_front)
            messages.success(request, 'Profile picture updated successfully.')
            return redirect('edit_profile')
        else:
            messages.error(request, 'Select the Profile Picture First')

    return render(request, 'myapp/edit_profile.html', {
        'user_profile': user_profile,
        'user_full_name': user_full_name,
        'user_profile_picture': user_profile_picture,
        'kyc_registration': kyc_registration,
        'kyc_reject': kyc_reject,
        'kyc_verified': kyc_verified,
        'vote_status': vote_status,
    })




def update_kyc(request):
    if not request.session.get('user_verified'):
        return redirect('userlogin')
    
    emailuser = request.session.get('email')
    user = UserProfile.objects.get(email=emailuser)
    kyc = KycRegistration.objects.get(email=emailuser)

    user_full_name = f"{user.first_name} {user.last_name}"
    user_profile_picture = ProfilePicture.objects.filter(email=emailuser).first()

    if request.method == 'POST':
        # Process the form submission
        email = request.POST.get('email')
        citizenship_number = request.POST.get('citizenship_number')
        voter_id = request.POST.get('voter_id')
        gender = request.POST.get('gender')
        country = request.POST.get('country')
        province = request.POST.get('province')
        district = request.POST.get('district')
        municipality = request.POST.get('municipality')
        ward_no = request.POST.get('ward_no')

        # Access the uploaded files
        photo_front = request.FILES.get('photo_front')
        photo_voter = request.FILES.get('photo_voter')
        photo_citizenship_front = request.FILES.get('photo_citizenship_front')
        photo_citizenship_back = request.FILES.get('photo_citizenship_back')

        # Update KycRequest if exists
        try:
            kyc_request = KycRequest.objects.get(email=emailuser)
            kyc_request.email = email
            kyc_request.phone_number = user.phone_number  # Assuming phone_number is in UserProfile
            kyc_request.citizenship_number = citizenship_number
            kyc_request.voter_id = voter_id
            kyc_request.save()
        except KycRequest.DoesNotExist:
            kyc_request = KycRequest.objects.create(
                email=emailuser,
                phone_number=user.phone_number,
                citizenship_number=citizenship_number,
                voter_id=voter_id
            )

        # Update ProfilePicture if exists
        try:
            profile_picture = ProfilePicture.objects.get(email=emailuser)
            profile_picture.email = email
            if photo_front:
                profile_picture.photo_front = photo_front
            profile_picture.save()
        except ProfilePicture.DoesNotExist:
            profile_picture = ProfilePicture.objects.create(
                email=emailuser,
                photo_front=photo_front  # Assuming only updating photo_front
            )

        # Update KycRegistration
        try:
            kyc.email = email
            kyc.citizenship_number = citizenship_number
            kyc.voter_id = voter_id
            kyc.gender = gender
            kyc.country = country
            kyc.province = province
            kyc.district = district
            kyc.municipality = municipality
            kyc.ward_no = ward_no
            kyc.photo_front = photo_front
            kyc.photo_voter = photo_voter
            kyc.photo_citizenship_front = photo_citizenship_front
            kyc.photo_citizenship_back = photo_citizenship_back
            kyc.save()

            messages.success(request, 'KYC details updated successfully.')
            return redirect('edit_profile')
        except KycRegistration.DoesNotExist:
            messages.error(request, 'User with this email does not exist.')

    context = {
        'user': user,
        'user_full_name': user_full_name,
        'user_profile_picture': user_profile_picture,
        'kyc': kyc,
        'selected_country': kyc.country,
        'selected_province': kyc.province,
        'selected_district': kyc.district,
        'selected_gender': kyc.gender
    }

    return render(request, 'myapp/update_kyc.html', context)



def submit_vote(request):
    if request.method == 'POST':
        user_email = request.session.get('email')
        if not user_email:
            messages.error(request, "User email not found in session.")
            return redirect('vote')

        try:
            kyc_data = KycRegistration.objects.get(email=user_email)
        except KycRegistration.DoesNotExist:
            messages.error(request, "KYC data not found for the user.")
            return redirect('vote')

        district = kyc_data.district
        municipality = kyc_data.municipality
        ward = kyc_data.ward_no

        mp_vote = request.POST.get('mp_vote')
        mayor_vote = request.POST.get('mayor_vote')
        deputy_mayor_vote = request.POST.get('deputy_mayor_vote')
        ward_chairperson_vote = request.POST.get('ward_chairperson_vote')

        if mp_vote:
            MpVote.objects.create(email=mp_vote, district=district)
        if mayor_vote:
            MayorVote.objects.create(email=mayor_vote, municipality=municipality)
        if deputy_mayor_vote:
            DeputymayorVote.objects.create(email=deputy_mayor_vote, municipality=municipality)
        if ward_chairperson_vote:
            WardVote.objects.create(email=ward_chairperson_vote, wardno=ward)

        VoteStatus.objects.create(email=user_email)

        messages.success(request, "Your votes have been submitted successfully.")
        return redirect('vote')

    return render(request, 'vote_here.html')


def dashboard(request):
    total_users = UserProfile.objects.count()
    total_candidates = CandidateProfile.objects.count()
    kyc_requests = KycRequest.objects.count()
    kyc_verified = Kycverified.objects.count()

    context = {
        'total_users': total_users,
        'total_candidates': total_candidates,
        'kyc_requests': kyc_requests,
        'kyc_verified': kyc_verified,
    }

    return render(request, 'myapp/dashboard.html', context)

def calculate_age(dob):
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

'''def user_age_distribution(request):
    users = UserProfile.objects.all()  # Fetch all user profiles
    age_groups = {'18-25': 0, '26-45': 0, '46-70': 0, '71-100': 0}

    # Calculate age distribution
    for user in users:
        age = calculate_age(user.date_of_birth)
        if 18 <= age <= 25:
            age_groups['18-25'] += 1
        elif 26 <= age <= 45:
            age_groups['26-45'] += 1
        elif 46 <= age <= 70:
            age_groups['46-70'] += 1
        elif 71 <= age <= 100:
            age_groups['71-100'] += 1

    # Generate the graph
    fig, ax = plt.subplots()
    ax.bar(age_groups.keys(), age_groups.values())
    ax.set_xlabel('Age Groups')
    ax.set_ylabel('Number of Users')
    ax.set_title('User Age Distribution')

    # Save the plot to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close(fig)
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Encode the PNG image to base64 string
    graph = base64.b64encode(image_png).decode('utf-8')

    # Pass the graph data to the template
    context = {'graph': graph}
    return render(request, 'myapp/dashboard.html', context) '''



def candidates_by_party(request):
    # Query to get the count of candidates per political party
    party_counts = CandidateProfile.objects.values('political_party').annotate(total=Count('id'))

    # Prepare data for the graph
    parties = [item['political_party'] for item in party_counts]
    counts = [item['total'] for item in party_counts]

    # Generate the graph
    fig, ax = plt.subplots()
    ax.bar(parties, counts)
    ax.set_xlabel('Political Party')
    ax.set_ylabel('Number of Candidates')
    ax.set_title('Number of Candidates by Political Party')
    ax.tick_params(axis='x', rotation=45)  # Rotate x-axis labels for better readability

    # Save the plot to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close(fig)
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # Encode the PNG image to base64 string
    graph = base64.b64encode(image_png).decode('utf-8')

    # Debugging output
    print("Graph data:", graph)

    return render(request, 'myapp/candidate_party_graph.html', {'graph': graph})


def vote_timing(request):
    return render(request,'myapp/vote_timing.html')





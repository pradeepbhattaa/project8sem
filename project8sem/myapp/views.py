import json
import math
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.http import JsonResponse
from .models import CandidateProfile, VoteStatus, MpVote, MayorVote, DeputymayorVote, KycRequest, UserProfile, KycRegistration, ProfilePicture, Test, UserRegistration, Notice, Kycverified, KycRejected, WardVote, EmailVerification
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from django.utils.dateparse import parse_date
from django.db.models import Count
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
        return redirect('user_signup')
    return render(request, 'myapp/register.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not email or not password:
            messages.error(request, 'Email or Password cannot be empty.')
            return render(request, 'myapp/admin_login.html')
        try:
            admin = Test.objects.get(email=email)
            if password == admin.password:
                request.session['admin_verified'] = True
                request.session['admin_id'] = admin.id
                request.session['email'] = admin.email
                messages.success(request, 'You Are Logged In')
                return redirect('base')
            else:
                messages.error(request, 'Invalid email or password.')
        except Test.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'myapp/admin_login.html')

def adminlogout(request):
    request.session.flush()
    return render(request, 'myapp/admin_login.html')

def userlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not email or not password:
            messages.error(request, 'Email or Password cannot be empty.')
            return render(request, 'myapp/user_login.html')
        try:
            user = UserProfile.objects.get(email=email)
            if check_password(password, user.password):
                request.session['user_verified'] = True
                request.session['user_id'] = user.id
                request.session['email'] = user.email
                messages.success(request, 'You Are Logged In')
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password.')
        except UserProfile.DoesNotExist:
            messages.error(request, 'Email is not Registered.')
    return render(request, 'myapp/user_login.html')

def base(request):
    if not request.session.get('admin_verified'):
        return redirect('login')
    return render(request, 'myapp/base.html')

def hello(request):
    return render(request, 'myapp/hello.html')

def admin_login(request):
    return render(request, 'myapp/admin_login.html')

def add_user(request):
    return render(request, 'myapp/add_user.html')

def home(request):
    users = UserProfile.objects.all()
    user_profile_picture = None
    user_full_name = None
    email = request.session.get('email')
    if email:
        try:
            user_profile = get_object_or_404(UserProfile, email=email)
            user_full_name = f"{user_profile.first_name} {user_profile.middle_name or ''} {user_profile.last_name}".strip()
            try:
                profile_picture = ProfilePicture.objects.get(email=email)
                user_profile_picture = profile_picture.photo_front.url
            except ProfilePicture.DoesNotExist:
                user_profile_picture = None
        except UserProfile.DoesNotExist:
            pass
    return render(request, 'myapp/home.html', {
        'users': users,
        'user_profile_picture': user_profile_picture,
        'user_full_name': user_full_name,
    })

def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name', '')
        last_name = request.POST.get('last_name')
        dob = request.POST.get('dob')
        phone_number = request.POST.get('phonenumber')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('cpassword')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')

        if UserProfile.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return redirect('signup')
        elif UserProfile.objects.filter(phone_number=phone_number).exists():
            messages.error(request, 'Phone number is already registered.')
            return redirect('signup')

        user_profile = UserProfile.objects.create(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            dob=dob,
            phone_number=phone_number,
            email=email,
            password=make_password(password)
        )
        messages.success(request, 'Register successful!')
        return redirect('userlogin')
    return render(request, 'myapp/user_signup.html')

def adduser(request):
    if not request.session.get('admin_verified'):
        return redirect('login')
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name', '')
        last_name = request.POST.get('last_name')
        dob = request.POST.get('dob')
        phone_number = request.POST.get('phonenumber')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('cpassword')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('adduser')

        if UserProfile.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return redirect('adduser')
        elif UserProfile.objects.filter(phone_number=phone_number).exists():
            messages.error(request, 'Phone number is already registered.')
            return redirect('adduser')

        user_profile = UserProfile.objects.create(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            dob=dob,
            phone_number=phone_number,
            email=email,
            password=make_password(password)
        )
        messages.success(request, 'User Added successfully!')
        return redirect('base')
    return render(request, 'myapp/add_user.html')

def edituser(request):
    if not request.session.get('admin_verified'):
        return redirect('login')
    if request.method == 'POST':
        email = request.POST.get('semail')
        try:
            user = UserProfile.objects.get(email=email)
            messages.success(request, 'User with this email exists.')
            return render(request, 'myapp/edit_user.html', {'user': user})
        except UserProfile.DoesNotExist:
            messages.error(request, 'User with this email does not exist.')
            return redirect('edituser')
    return render(request, 'myapp/edit_user.html', {'email_exists': False})

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

        if not email:
            messages.error(request, 'Email field cannot be empty.')
            return redirect('edituser')
        if not first_name or not last_name or not dob or not phone_number:
            messages.error(request, 'All fields except middle name must be filled.')
            return redirect('edituser')

        try:
            user = UserProfile.objects.get(email=email)
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

def deleteuser(request):
    if not request.session.get('admin_verified'):
        return redirect('login')
    if request.method == 'POST':
        email = request.POST.get('semail')
        try:
            user = UserProfile.objects.get(email=email)
            messages.success(request, 'User with this email exists.')
            return render(request, 'myapp/delete_user.html', {'user': user})
        except UserProfile.DoesNotExist:
            messages.error(request, 'User with this email does not exist.')
            return redirect('deleteuser')
    return render(request, 'myapp/delete_user.html', {'email_exists': False})

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

def view_users(request):
    if not request.session.get('admin_verified'):
        return redirect('login')
    users = UserProfile.objects.all()
    return render(request, 'myapp/view_user.html', {'users': users})

def verify_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if UserProfile.objects.filter(email=email).exists():
            otp_code = get_random_string(length=6, allowed_chars='1234567890')
            EmailVerification.objects.create(email=email, otp_code=otp_code)
            send_mail(
                'OTP for Email Verification',
                f'Your OTP code to verify your email for Online voting system is: {otp_code}',
                'theapocalypseitproject@gmail.com',
                [email],
                fail_silently=False,
            )
            request.session['email'] = email
            request.session['page_a_completed'] = True
            request.session['page_b_completed'] = False
            messages.success(request, 'User has been successfully verified. Please check your email for the OTP.')
            return redirect('verify_otp')
        else:
            messages.error(request, 'User with this email is not registered.')
            return redirect('verify_email')
    return render(request, 'myapp/verify_email.html')

def verify_otp(request):
    if not request.session.get('page_a_completed'):
        return redirect('userlogin')
    email = request.session.get('email')
    if request.method == 'POST':
        otp = request.POST.get('otp')
        email_verification = EmailVerification.objects.filter(email=email, otp_code=otp).first()
        if email_verification:
            request.session['page_b_completed'] = True
            request.session['page_a_completed'] = False
            messages.success(request, 'Email verified successfully.')
            return redirect('update_password')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
    return render(request, 'myapp/verify_otp.html')

def update_password(request):
    if not request.session.get('page_b_completed'):
        return redirect('userlogin')
    email = request.session.get('email')
    if request.method == 'POST':
        new_password = request.POST.get('npassword')
        confirm_password = request.POST.get('ncpassword')
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match. Please try again.')
            return render(request, 'myapp/update_password.html')
        user = UserProfile.objects.get(email=email)
        user.password = make_password(new_password)
        user.save()
        request.session.flush()
        messages.success(request, 'Your password was successfully updated!')
        return redirect('userlogin')
    return render(request, 'myapp/update_password.html')

def view_otp(request):
    users = EmailVerification.objects.all()
    return render(request, 'myapp/view_otp.html', {'users': users})

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
            user_profile_picture = None
        try:
            user_profile = UserProfile.objects.get(email=email)
            user_full_name = f"{user_profile.first_name} {user_profile.middle_name or ''} {user_profile.last_name}".strip()
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
            user_profile_picture = None
        try:
            user_profile = UserProfile.objects.get(email=email)
            user_full_name = f"{user_profile.first_name} {user_profile.middle_name or ''} {user_profile.last_name}".strip()
        except UserProfile.DoesNotExist:
            pass
    return render(request, 'myapp/notices.html', {
        'notices': notices,
        'user_profile_picture': user_profile_picture,
        'user_full_name': user_full_name,
    })
# views.py  – replace the whole verify_kyc view with this version
from django.shortcuts import redirect, render
from django.contrib import messages
import json
from .models import (
    UserProfile, ProfilePicture, KycRequest,
    KycRegistration,
)

def verify_kyc(request):
    if not request.session.get('user_verified'):
        return redirect('userlogin')

    emailuser = request.session.get('email')
    user = UserProfile.objects.get(email=emailuser)

    # already submitted?
    if KycRegistration.objects.filter(email=emailuser).exists():
        messages.success(request, 'Your KYC has already been submitted')
        return redirect('vote')

    user_full_name        = f"{user.first_name} {user.last_name}"
    user_profile_picture  = ProfilePicture.objects.filter(email=emailuser).first()

    if request.method == 'POST':
        # ------------------------------------------------------------------ #
        #                    1.  PLAIN FORM FIELDS                            #
        # ------------------------------------------------------------------ #
        email              = request.POST.get('email')
        citizenship_number = request.POST.get('citizenship_number')
        voter_id           = request.POST.get('voter_id')
        gender             = request.POST.get('gender')
        country            = request.POST.get('country')
        province           = request.POST.get('province')
        district           = request.POST.get('district')
        municipality       = request.POST.get('municipality')
        ward_no            = request.POST.get('ward_no')

        # ------------------------------------------------------------------ #
        #                    2.  FILE UPLOADS                                 #
        # ------------------------------------------------------------------ #
        photo_front             = request.FILES.get('photo_front')
        photo_voter             = request.FILES.get('photo_voter')
        photo_citizenship_front = request.FILES.get('photo_citizenship_front')
        photo_citizenship_back  = request.FILES.get('photo_citizenship_back')

        # ------------------------------------------------------------------ #
        #                    3.  FACE DESCRIPTOR (hidden input)               #
        # ------------------------------------------------------------------ #
        raw_descriptor = request.POST.get('face_descriptor')  # hidden input name
        try:
            face_descriptor = json.loads(raw_descriptor) if raw_descriptor else None
        except json.JSONDecodeError:
            messages.error(request, 'Face descriptor is not valid JSON.')
            return redirect('verify_kyc')

        # ------------------------------------------------------------------ #
        #                    4.  KYC REQUEST LOG                              #
        # ------------------------------------------------------------------ #
        KycRequest.objects.update_or_create(
            email=email,
            defaults={
                'phone_number': user.phone_number,
                'citizenship_number': citizenship_number,
                'voter_id': voter_id
            }
        )

        # ------------------------------------------------------------------ #
        #                    5.  PROFILE PICTURE                              #
        # ------------------------------------------------------------------ #
        if photo_front:
            ProfilePicture.objects.update_or_create(
                email=email,
                defaults={'photo_front': photo_front}
            )

        # ------------------------------------------------------------------ #
        #                    6.  MAIN KYC REGISTRATION                        #
        # ------------------------------------------------------------------ #
        KycRegistration.objects.create(
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
            photo_citizenship_back=photo_citizenship_back,
            face_descriptor=face_descriptor,          # <-- STORED HERE
        )

        messages.success(request, 'Your KYC has been submitted successfully')
        return redirect('home')

    # GET request – render page
    return render(
        request,
        'myapp/kkyc.html',
        {
            'user'                : user,
            'user_full_name'      : user_full_name,
            'user_profile_picture': user_profile_picture,
        }
    )

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
            return redirect('addcandidate')
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
        candidate_profile.save()
        messages.success(request, 'Candidate added successfully.')
        return redirect('base')
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
            user_profile_picture = profile_picture.photo_front.url if profile_picture.photo_front else None
        except ProfilePicture.DoesNotExist:
            user_profile_picture = None
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

def user_logout(request):
    request.session.flush()
    messages.success(request, 'you have been successfully logout')
    return redirect('userlogin')

def viewall_candidate(request):
    users = CandidateProfile.objects.all()
    return render(request, 'myapp/viewall_candidate.html', {'users': users})

def editcandidate(request):
    if not request.session.get('admin_verified'):
        return redirect('login')
    if request.method == 'POST':
        email = request.POST.get('semail')
        try:
            user = CandidateProfile.objects.get(email=email)
            messages.success(request, 'Candidate with this email does exist.')
            return render(request, 'myapp/edit_candidate.html', {'user': user})
        except CandidateProfile.DoesNotExist:
            messages.error(request, 'Candidate with this email does not exist.')
            return redirect('editcandidate')
    return render(request, 'myapp/edit_candidate.html', {'email_exists': False})

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
        if not email:
            messages.error(request, 'Email field cannot be empty.')
            return redirect('editcandidate')
        parsed_dob = parse_date(dob)
        if not parsed_dob:
            messages.error(request, 'Invalid date format for date of birth.')
            return redirect('editcandidate')
        try:
            user = CandidateProfile.objects.get(email=email)
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

def deletecandidate(request):
    if not request.session.get('admin_verified'):
        return redirect('login')
    if request.method == 'POST':
        email = request.POST.get('semail')
        try:
            user = CandidateProfile.objects.get(email=email)
            messages.success(request, 'Candidate with this email does exist.')
            return render(request, 'myapp/delete_candidate.html', {'user': user})
        except CandidateProfile.DoesNotExist:
            messages.error(request, 'Candidate with this email does not exist.')
            return redirect('deletecandidate')
    return render(request, 'myapp/delete_candidate.html', {'email_exists': False})

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
            notice = Notice(
                notice_header=notice_header,
                notice_img=notice_img,
                notice_description=notice_description
            )
            notice.save()
            messages.success(request, 'Notice added successfully.')
            return redirect('add_notices')
        else:
            messages.error(request, 'All fields are required. Please try again.')
    return render(request, 'myapp/add_notices.html')

def view_notices(request):
    notices = Notice.objects.all()
    return render(request, 'anyapp/view_notices.html', {'notices': notices})

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
        if not notice_id:
            messages.error(request, 'Id field cannot be empty.')
            return redirect('editnotices')
        try:
            notice = Notice.objects.get(id=notice_id)
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
        id = request.POST.get('id')
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
    return redirect('deletenotices')

def vote(request):
    if not request.session.get('user_verified'):
        return redirect('userlogin')
    email = request.session.get('email')
    user = UserProfile.objects.get(email=email)
    try:
        profile_picture = ProfilePicture.objects.get(email=email)
        user_profile_picture = profile_picture.photo_front.url if profile_picture.photo_front else None
    except ProfilePicture.DoesNotExist:
        user_profile_picture = None
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
        messages.error(request, "Submit your Kyc First")
        return redirect('verify_kyc')
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
        'face_verified': request.session.get('face_verified', False),
    }
    return render(request, 'myapp/vote_here.html', context)

import numpy as np
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import KycRegistration

def verify_face(request):
    if not request.session.get('user_verified'):
        return JsonResponse({'success': False, 'message': 'User not authenticated'}, status=401)

    email = request.session.get('email')

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            live_desc_list = data.get('live_descriptor')
            if live_desc_list is None:
                return JsonResponse({'success': False, 'message': 'No live descriptor provided'}, status=400)

            kyc_registration = KycRegistration.objects.filter(email=email).first()
            if not kyc_registration or not kyc_registration.face_descriptor:
                return JsonResponse({'success': False, 'message': 'No stored face descriptor found'}, status=400)

            stored_desc = np.array(kyc_registration.face_descriptor, dtype=float)
            live_desc = np.array(live_desc_list, dtype=float)

            THRESHOLD = 0.60
            dist = np.linalg.norm(live_desc - stored_desc)

            if dist < THRESHOLD:
                request.session['face_verified'] = True
                return JsonResponse({'success': True, 'message': 'Facial verification successful'})
            else:
                return JsonResponse({'success': False, 'message': 'Faces do not match'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error verifying face: {str(e)}'}, status=500)

    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)


def submit_vote(request):
    print(f"submit_vote: Method: {request.method}, Session: {request.session.session_key}, CSRF Token: {request.POST.get('csrfmiddlewaretoken')}, Cookies: {request.COOKIES}, Session email: {request.session.get('email')}")
    
    if not request.session.get('user_verified'):
        messages.error(request, 'You need to log in to vote.')
        print("submit_vote: Redirecting to userlogin due to unauthenticated user")
        return redirect('userlogin')
    
    email = request.session.get('email')
    user_profile = UserProfile.objects.filter(email=email).first()
    if not user_profile:
        messages.error(request, 'User profile not found.')
        print("submit_vote: Redirecting to userlogin due to missing user profile")
        return redirect('userlogin')
    
    kyc_verified = Kycverified.objects.filter(email=email).first()
    if not kyc_verified:
        messages.error(request, 'Your KYC is not verified. Please submit and verify your KYC.')
        print("submit_vote: Redirecting to verify_kyc due to unverified KYC")
        return redirect('verify_kyc')
    
    kyc_request = KycRequest.objects.filter(email=email).first()
    if kyc_request and kyc_request.status == 'rejected':
        messages.error(request, 'Your KYC has been rejected. Please update your KYC.')
        print("submit_vote: Redirecting to update_kyc due to rejected KYC")
        return redirect('update_kyc')
    
    if kyc_request and kyc_request.status == 'pending':
        messages.warning(request, 'Your KYC verification is in progress. Please wait for approval.')
        print("submit_vote: Redirecting to vote due to pending KYC")
        return redirect('vote')
    
    vote_status = VoteStatus.objects.filter(email=email).first()
    if vote_status:
        messages.error(request, 'You have already voted.')
        print("submit_vote: Redirecting to vote due to existing vote")
        return redirect('vote')
    
    if not request.session.get('face_verified'):
        messages.error(request, 'Please complete facial verification before voting.')
        print("submit_vote: Redirecting to vote due to missing facial verification")
        return redirect('vote')
    
    if request.method == 'POST':
        print(f"submit_vote: POST data: {request.POST}")
        
        if not request.POST.get('csrfmiddlewaretoken'):
            messages.error(request, 'Invalid form submission. Please try again.')
            print("submit_vote: Redirecting to vote due to missing CSRF token")
            return redirect('vote')
        
        try:
            mp_vote = request.POST.get('mp_vote')
            mayor_vote = request.POST.get('mayor_vote')
            deputy_mayor_vote = request.POST.get('deputy_mayor_vote')
            ward_chairperson_vote = request.POST.get('ward_chairperson_vote')
            
            if not (mp_vote or mayor_vote or deputy_mayor_vote or ward_chairperson_vote):
                messages.error(request, 'Please select at least one candidate to vote for.')
                print("submit_vote: Redirecting to vote due to no candidate selected")
                return redirect('vote')
            
            kyc = KycRegistration.objects.get(email=email)
            
            # MP Vote
            if mp_vote:
                if MpVote.objects.filter(voter_email=email).exists():
                    messages.error(request, 'You have already voted for MP.')
                    return redirect('vote')
                MpVote.objects.create(voter_email=email, candidate_email=mp_vote, district=kyc.district)
            
            # Mayor Vote
            if mayor_vote:
                if MayorVote.objects.filter(voter_email=email).exists():
                    messages.error(request, 'You have already voted for Mayor.')
                    return redirect('vote')
                MayorVote.objects.create(voter_email=email, candidate_email=mayor_vote, municipality=kyc.municipality)
            
            # Deputy Mayor Vote
            if deputy_mayor_vote:
                if DeputymayorVote.objects.filter(voter_email=email).exists():
                    messages.error(request, 'You have already voted for Deputy Mayor.')
                    return redirect('vote')
                DeputymayorVote.objects.create(voter_email=email, candidate_email=deputy_mayor_vote, municipality=kyc.municipality)
            
            # Ward Chairperson Vote
            if ward_chairperson_vote:
                if WardVote.objects.filter(voter_email=email).exists():
                    messages.error(request, 'You have already voted for Ward Chairperson.')
                    return redirect('vote')
                WardVote.objects.create(voter_email=email, candidate_email=ward_chairperson_vote, wardno=kyc.ward_no)
            
            # Mark user as voted
            VoteStatus.objects.create(email=email)
            
            # Reset face verification session flag
            request.session['face_verified'] = False
            
            messages.success(request, 'Your vote has been submitted successfully!')
            print("submit_vote: Vote submitted successfully")
            return redirect('vote')
        
        except Exception as e:
            messages.error(request, f'Error submitting vote: {str(e)}')
            print(f"submit_vote: Error: {str(e)}")
            return redirect('vote')
    
    # GET request - prepare context for voting page
    mp_candidates = CandidateProfile.objects.filter(role='MP')
    mayor_candidates = CandidateProfile.objects.filter(role='Mayor')
    deputy_mayor_candidates = CandidateProfile.objects.filter(role='Deputy Mayor')
    ward_candidate = CandidateProfile.objects.filter(role='Ward Chairperson')
    
    profile_picture_obj = ProfilePicture.objects.filter(email=email).first()
    user_profile_picture = profile_picture_obj.photo_front.url if profile_picture_obj and profile_picture_obj.photo_front else None
    
    context = {
        'user_full_name': f"{user_profile.first_name} {user_profile.last_name}" if user_profile else None,
        'user_profile_picture': user_profile_picture,
        'mp_candidates': mp_candidates,
        'mayor_candidates': mayor_candidates,
        'deputy_mayor_candidates': deputy_mayor_candidates,
        'ward_candidate': ward_candidate,
        'votestatus': vote_status,
        'kycreject': kyc_request.status == 'rejected' if kyc_request else False,
        'kycrequest': kyc_request.status == 'pending' if kyc_request else False,
        'user_verified': kyc_verified is not None,
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
    Kycverified.objects.create(
        email=kyc_request.email,
        verified_by=request.session.get('email'),
    )
    kyc_request.delete()
    messages.success(request, "KYC accepted succesfully")
    return redirect('view_kycrequest')

def reject_kyc(request, request_id):
    kyc_request = get_object_or_404(KycRequest, pk=request_id)
    KycRejected.objects.create(
        email=kyc_request.email,
    )
    kyc_request.delete()
    messages.error(request, "KYC rejected succesfully")
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
    if profile_picture and profile_picture.photo_front:
        user_profile_picture = profile_picture.photo_front.url
    else:
        user_profile_picture = None
    if request.method == 'POST':
        if 'photo_front' in request.FILES:
            photo_front = request.FILES['photo_front']
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
    profile_picture_obj = ProfilePicture.objects.filter(email=emailuser).first()
    if profile_picture_obj and profile_picture_obj.photo_front:
        user_profile_picture = profile_picture_obj.photo_front.url
    else:
        user_profile_picture = None
    if request.method == 'POST':
        email = request.POST.get('email')
        citizenship_number = request.POST.get('citizenship_number')
        voter_id = request.POST.get('voter_id')
        gender = request.POST.get('gender')
        country = request.POST.get('country')
        province = request.POST.get('province')
        district = request.POST.get('district')
        municipality = request.POST.get('municipality')
        ward_no = request.POST.get('ward_no')
        photo_front = request.FILES.get('photo_front')
        photo_voter = request.FILES.get('photo_voter')
        photo_citizenship_front = request.FILES.get('photo_citizenship_front')
        photo_citizenship_back = request.FILES.get('photo_citizenship_back')
        try:
            kyc_request = KycRequest.objects.get(email=emailuser)
            kyc_request.email = email
            kyc_request.phone_number = user.phone_number
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
        try:
            profile_picture = ProfilePicture.objects.get(email=emailuser)
            profile_picture.email = email
            if photo_front:
                profile_picture.photo_front = photo_front
            profile_picture.save()
        except ProfilePicture.DoesNotExist:
            ProfilePicture.objects.create(
                email=emailuser,
                photo_front=photo_front
            )
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
            if photo_front:
                kyc.photo_front = photo_front
            if photo_voter:
                kyc.photo_voter = photo_voter
            if photo_citizenship_front:
                kyc.photo_citizenship_front = photo_citizenship_front
            if photo_citizenship_back:
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

def candidates_by_party(request):
    party_counts = CandidateProfile.objects.values('political_party').annotate(total=Count('id'))
    parties = [item['political_party'] for item in party_counts]
    counts = [item['total'] for item in party_counts]
    fig, ax = plt.subplots()
    ax.bar(parties, counts)
    ax.set_xlabel('Political Party')
    ax.set_ylabel('Number of Candidates')
    ax.set_title('Number of Candidates by Political Party')
    ax.tick_params(axis='x', rotation=45)
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close(fig)
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graph = base64.b64encode(image_png).decode('utf-8')
    print("Graph data:", graph)
    return render(request, 'myapp/candidate_party_graph.html', {'graph': graph})

def vote_timing(request):
    return render(request, 'myapp/vote_timing.html')

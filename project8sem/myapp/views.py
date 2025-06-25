from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login as auth_login
from .models import Test
from .models import UserRegistration
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from .models import UserProfile
from .models import ProfilePicture
from .models import Notice

from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .models import EmailVerification


# Create your views here.
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

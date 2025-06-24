from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login as auth_login
from .models import Test

# Create your views here.
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


def base(request):
    if not request.session.get('admin_verified'):
        return redirect('login')  # Redirect to verify_email if page_a is not completed
    return render(request,'myapp/base.html')

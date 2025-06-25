from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    
    path('base/', views.base, name='base'),
    path('hello/',views.hello, name='hello'),

    path('register/',views.register_user, name='register_user'),



     path('user_login/',views.userlogin, name='userlogin'),


    path('admin_login/',views.login, name='login'),
    path('adminlogout/',views.adminlogout, name='adminlogout'),

    
        path('home/',views.home,name="home"),



 
         path('user_signup/', views.signup, name='signup'),

         path('add_user/', views.adduser, name='adduser'),


           path('edit_user/', views.edituser, name='edituser'),



    ]

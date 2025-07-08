# myapp/urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [

    #path('user_registration/', views.register_user, name='user_registration'),

    
    #path('login/', views.login, name='login'),



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


            path('update_user/', views.update_user, name='update_user'),

              
              path('delete_user/', views.deleteuser, name='deleteuser'),


                path('delete_user_confirm/', views.delete_user_confirm, name='delete_user_confirm'),

                  path('view_users/', views.view_users, name='view_users'),

                  path('view_otp/', views.view_otp, name='view_otp'),

                  path('verify_email/',views.verify_email,name="verify_email"),

                  path('verify_otp/',views.verify_otp,name="verify_otp"),

                  path('update_password/',views.update_password,name="update_password"),

                  #$path('admin_dashboard/',views.admin_dashboard,name="admin_dashboard"),

                  path('home/',views.home,name="home"),

                  path('candidates/',views.candidates,name="candidates"),

                  path('notices/',views.notices,name="notices"),

                  #path('vote_here/',views.vote_here,name="vote_here"),

                  path('contact/',views.contact,name="contact"),
                  path('verify_kyc/',views.verify_kyc,name="verify_kyc"),

                     
                    path('get_provinces/', views.get_provinces, name='get_provinces'),
                       path('get_districts/', views.get_districts, name='get_districts'),


                       path('add_candidate/',views.addcandidate,name="addcandidate"),

                       path('view_candidate/',views.viewcandidate,name="viewcandidate"),

                       path('viewall_candidate/',views.viewall_candidate,name="viewall_candidate"),

                       path('edit_candidate/',views.editcandidate,name="editcandidate"),

                       path('update_candidate/',views.update_candidate,name="update_candidate"),

                       path('delete_candidate/',views.deletecandidate,name="deletecandidate"),

                       path('delete_candidate_confirm/', views.delete_candidate_confirm, name='delete_candidate_confirm'),



                       path('add_notices/',views.add_notices,name="add_notices"),

                       path('view_notices/',views.view_notices,name="view_notices"),

                       path('edit_notices/',views.editnotices,name="editnotices"),

                        path('update_notices/',views.update_notices,name="update_notices"),

                        path('delete_notices/',views.deletenotices,name="deletenotices"),

                        path('delete_notices_confirm/', views.delete_notices_confirm, name='delete_notices_confirm'),


                        path('vote/',views.vote,name="vote"),

                         path('view_kycrequest/',views.view_kycrequest,name="view_kycrequest"),

                         path('kyc/<int:request_id>/', views.view_kyc, name='view_kyc'),

                         path('accept_kyc/<int:request_id>/', views.accept_kyc, name='accept_kyc'),

                         path('reject_kyc/<int:request_id>/', views.reject_kyc, name='reject_kyc'),

                         path('view_verifiedkyc/',views.view_verifiedkyc,name="view_verifiedkyc"),

                         path('view_rejectedkyc/',views.view_rejectedkyc,name="view_rejectedkyc"),

                         path('edit_profile/',views.edit_profile,name="edit_profile"),

                         path('update_kyc/',views.update_kyc,name="update_kyc"),

                         path('submit_vote/',views.submit_vote,name="submit_vote"),

                         path('dashboard/',views.dashboard,name="dashboard"),



                       path('user_logout/',views.user_logout,name="user_logout"),
                       path('verify_face/', views.verify_face, name='verify_face'),



                  



            





     






    
  
    
  

   
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


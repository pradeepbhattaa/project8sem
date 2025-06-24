from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    
    path('base/', views.base, name='base'),
    path('admin_login/',views.login, name='login')
]

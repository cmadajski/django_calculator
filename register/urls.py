from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('check_register/', views.check_register, name='check_register'),
    path('check_registration_email/', views.check_registration_email, name='check_registration_email'),
    path('check_registration_password/', views.check_registration_password, name='check_registration_password'),
    path('check_registration_password_repeat/', views.check_registration_password_repeat, name='check_registration_password_repeat'),
    path('enable_register_button/', views.enable_register_button, name='enable_register_button'),
]
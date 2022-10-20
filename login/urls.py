from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('check_login/', views.check_login, name='check_login'),
    path('logout/', views.logout, name="logout"),
    path('check_login_email', views.check_login_email, name='check_login_email'),
    path('check_login_password', views.check_login_password, name='check_login_password'),
    path('enable_login_button/', views.enable_login_button, name='enable_login_button'),
]

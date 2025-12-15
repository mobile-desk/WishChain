from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    HomeView, LoginView, logout_view, profile,
    DonorRegisterView, WisherRegisterView, RegistrationTypeView
)
from .views.registration.views_ajax import GetCitiesView

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    
    # Authentication URLs
    path('register/', RegistrationTypeView.as_view(), name='register'),
    path('register/donor/', DonorRegisterView.as_view(), name='register_donor'),
    path('register/wisher/', WisherRegisterView.as_view(), name='register_wisher'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    
    # Profile
    path('profile/', profile, name='profile'),
    
    # AJAX endpoints
    path('get-cities/', GetCitiesView.as_view(), name='get_cities'),
    
    # Password Reset (you can customize these later)
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='core/auth/password_reset.html',
             email_template_name='core/auth/emails/password_reset_email.html',
             subject_template_name='core/auth/emails/password_reset_subject.txt'
         ), 
         name='password_reset'),
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='core/auth/password_reset_done.html'
         ), 
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='core/auth/password_reset_confirm.html'
         ), 
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='core/auth/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
]

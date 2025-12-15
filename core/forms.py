from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('wisher', 'I want to make a wish'),
        ('donor', 'I want to help fulfill wishes'),
    ]
    
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect,
        required=True
    )
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'country', 'password1', 'password2', 'role')
        widgets = {
            'country': forms.Select(attrs={'class': 'form-select'}),
        }

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        label='Email'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label='Password'
    )
    
    class Meta:
        fields = ('email', 'password')

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, FormView, TemplateView
from django.urls import reverse_lazy, reverse
from .models import User

# Import forms
from .forms import (
    DonorRegistrationForm,
    WisherRegistrationForm,
    UserRegistrationForm,
    UserLoginForm
)


def home(request):
    """
    Home page view.
    Displays different content based on user authentication status.
    """
    context = {}
    if request.user.is_authenticated:
        # Add any user-specific context here
        context['user'] = request.user
    return render(request, 'core/home.html', context)

class RegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'core/auth/register.html'
    success_url = reverse_lazy('core:home')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save(commit=False)
        user.role = form.cleaned_data.get('role')
        user.save()
        login(self.request, user)
        messages.success(self.request, 'Registration successful!')
        return response

class LoginView(FormView):
    form_class = UserLoginForm
    template_name = 'core/auth/login.html'
    success_url = reverse_lazy('core:home')
    
    def form_valid(self, form):
        email = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        
        if user is not None:
            login(self.request, user)
            messages.success(self.request, 'You have been logged in successfully.')
            return super().form_valid(form)
        else:
            messages.error(self.request, 'Invalid email or password.')
            return self.form_invalid(form)

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('core:home')

@login_required
def profile(request):
    return render(request, 'core/profile.html')

# Registration Views
class BaseRegisterView(CreateView):
    """Base view for registration."""
    template_name = 'core/auth/register_base.html'
    success_url = reverse_lazy('core:home')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, 'Registration successful! Welcome to WishChain.')
        return response

class DonorRegisterView(BaseRegisterView):
    """
    View for donor registration.
    URL: /register/donor/
    """
    form_class = DonorRegistrationForm
    template_name = 'core/auth/register_donor.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_donor'] = True
        return context

class WisherRegisterView(BaseRegisterView):
    """
    View for wisher registration.
    URL: /register/wisher/
    """
    form_class = WisherRegistrationForm
    template_name = 'core/auth/register_wisher.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_wisher'] = True
        return context

class RegistrationTypeView(TemplateView):
    """
    View to select registration type (Donor or Wisher).
    URL: /register/
    """
    template_name = 'core/auth/register_choice.html'

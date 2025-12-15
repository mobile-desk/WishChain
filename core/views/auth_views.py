from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views.generic import CreateView, FormView, View
from django.urls import reverse_lazy
from ..forms import DonorRegistrationForm, WisherRegistrationForm, BaseRegistrationForm, UserLoginForm
from ..models import User

class RegisterView(CreateView):
    model = User
    template_name = 'core/auth/register.html'
    success_url = reverse_lazy('core:home')
    
    def get_form_class(self):
        # Determine which form to use based on the 'type' parameter
        user_type = self.request.GET.get('type', 'donor')
        if user_type == 'wisher':
            return WisherRegistrationForm
        return DonorRegistrationForm
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['data'] = self.request.POST or None
        kwargs['files'] = self.request.FILES or None
        return kwargs
    
    def form_valid(self, form):
        try:
            user = form.save(commit=False)
            user.role = 'donor' if isinstance(form, DonorRegistrationForm) else 'wisher'
            user.save()
            login(self.request, user)
            messages.success(self.request, 'Registration successful! Welcome to WishChain.')
            return redirect(self.get_success_url())
        except Exception as e:
            messages.error(self.request, f'An error occurred during registration: {str(e)}')
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        # Add form errors to messages for better user feedback
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field.title()}: {error}")
        return super().form_invalid(form)

class LoginView(FormView):
    form_class = UserLoginForm
    template_name = 'core/auth/login.html'
    success_url = reverse_lazy('core:home')
    
    def form_valid(self, form):
        email = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        remember_me = form.cleaned_data.get('remember_me', False)
        user = authenticate(email=email, password=password)
        
        if user is not None:
            login(self.request, user)
            if not remember_me:
                # Set session to expire when the browser is closed
                self.request.session.set_expiry(0)
            messages.success(self.request, 'You have been logged in successfully.')
            
            # Check if there's a 'next' parameter, otherwise redirect to appropriate dashboard
            next_url = self.request.GET.get('next')
            if next_url:
                return redirect(next_url)
            
            # Redirect to appropriate dashboard based on role
            if user.role == 'wisher':
                return redirect('wishes:dashboard')
            elif user.role == 'donor':
                return redirect('donations:dashboard')
            else:
                return redirect('core:home')
        else:
            messages.error(self.request, 'Invalid email or password.')
            return self.form_invalid(form)

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('core:home')

def profile(request):
    return render(request, 'core/auth/profile.html')

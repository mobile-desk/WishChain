from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login
from django.contrib import messages
# Direct import with the full module path
from core.forms.auth_forms import DonorRegistrationForm, WisherRegistrationForm

class BaseRegisterView(CreateView):
    """Base view for registration."""
    template_name = 'core/auth/register_base.html'
    success_url = reverse_lazy('core:home')
    
    def get_form_class(self):
        """Return the form class based on the role."""
        role = self.request.GET.get('role')
        if role == 'donor':
            return DonorRegistrationForm
        elif role == 'wisher':
            return WisherRegistrationForm
        return super().get_form_class()
    
    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        role = self.request.GET.get('role')
        if role:
            kwargs['role'] = role
        return kwargs
    
    def get_context_data(self, **kwargs):
        """Get the context for this view."""
        context = super().get_context_data(**kwargs)
        role = self.request.GET.get('role')
        if role == 'donor':
            context.update({
                'is_donor': True,
                'registration_title': 'Become a Wish Granter',
                'registration_subtitle': 'Join our community of generous donors making wishes come true',
            })
        elif role == 'wisher':
            context.update({
                'is_wisher': True,
                'registration_title': 'Make a Wish',
                'registration_subtitle': 'Share your needs with our community of generous donors',
            })
        return context
    
    def form_valid(self, form):
        """If the form is valid, save the associated model and log the user in."""
        self.object = form.save(commit=False)
        self.object.role = self.request.GET.get('role', 'donor')
        self.object.save()
        login(self.request, self.object)
        messages.success(self.request, 'Registration successful! Welcome to WishChain.')
        return super().form_valid(form)

class DonorRegisterView(BaseRegisterView):
    """
    View for donor registration.
    URL: /register/donor/
    """
    form_class = DonorRegistrationForm
    template_name = 'core/auth/register_donor.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'is_donor': True,
            'registration_title': 'Become a Wish Granter',
            'registration_subtitle': 'Join our community of generous donors making wishes come true',
        })
        return context
        
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['role'] = 'donor'
        return kwargs
        
    def get(self, request, *args, **kwargs):
        # Ensure role is set to donor for this view
        request.GET = request.GET.copy()
        request.GET['role'] = 'donor'
        return super().get(request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs):
        # Ensure role is set to donor for this view
        request.GET = request.GET.copy()
        request.GET['role'] = 'donor'
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, form):
        """If the form is valid, save the associated model and log the user in."""
        try:
            # Save the user and create DonorProfile (form.save handles this)
            user = form.save(commit=True)
            
            # Set self.object for CreateView compatibility
            self.object = user
            
            # Log the user in
            login(self.request, user)
            messages.success(self.request, 'Registration successful! Welcome to WishChain.')
            
            # Redirect to donor dashboard
            return redirect('donations:dashboard')
            
        except Exception as e:
            import traceback
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Donor registration error: {str(e)}\n{traceback.format_exc()}")
            messages.error(self.request, f'An error occurred during registration: {str(e)}')
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        """If the form is invalid, render the invalid form with error messages."""
        # Log form errors for debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Donor registration form validation failed: {form.errors}")
        logger.error(f"Form data: {form.data}")
        
        # Add detailed error messages
        for field, errors in form.errors.items():
            for error in errors:
                field_name = field.replace('_', ' ').title()
                messages.error(self.request, f"{field_name}: {error}")
        
        # Also add a general error message
        if form.errors:
            messages.error(self.request, "Please correct the errors below and try again.")
        
        return super().form_invalid(form)

class WisherRegisterView(BaseRegisterView):
    """
    View for wisher registration.
    URL: /register/wisher/
    """
    form_class = WisherRegistrationForm
    template_name = 'core/auth/register_wisher.html'
    success_url = reverse_lazy('core:home')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['role'] = 'wisher'
        return kwargs
    
    def get(self, request, *args, **kwargs):
        # Ensure role is set to wisher for this view
        request.GET = request.GET.copy()
        request.GET['role'] = 'wisher'
        return super().get(request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs):
        # Ensure role is set to wisher for this view
        request.GET = request.GET.copy()
        request.GET['role'] = 'wisher'
        return super().post(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'is_wisher': True,
            'registration_title': 'Make a Wish',
            'registration_subtitle': 'Share your needs with our community of generous donors'
        })
        return context
    
    def form_valid(self, form):
        """If the form is valid, save the associated model and log the user in."""
        try:
            # Save the user and create WisherProfile (form.save handles this)
            user = form.save(commit=True)
            
            # Set self.object for CreateView compatibility (required by CreateView)
            self.object = user
            
            # Log the user in
            login(self.request, user)
            messages.success(self.request, 'Registration successful! Welcome to WishChain.')
            
            # Redirect to appropriate dashboard based on role
            if user.role == 'wisher':
                return redirect('wishes:dashboard')
            elif user.role == 'donor':
                return redirect('donations:dashboard')
            else:
                # Fallback to home for other roles
                return redirect('core:home')
            
        except Exception as e:
            import traceback
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Registration error: {str(e)}\n{traceback.format_exc()}")
            messages.error(self.request, f'An error occurred during registration: {str(e)}')
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        """If the form is invalid, render the invalid form with error messages."""
        # Log form errors for debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Wisher registration form validation failed: {form.errors}")
        logger.error(f"Form data: {form.data}")
        
        # Add detailed error messages
        for field, errors in form.errors.items():
            for error in errors:
                field_name = field.replace('_', ' ').title()
                messages.error(self.request, f"{field_name}: {error}")
        
        # Also add a general error message
        if form.errors:
            messages.error(self.request, "Please correct the errors below and try again.")
        
        return super().form_invalid(form)

class RegistrationTypeView(TemplateView):
    """
    View to select registration type (Donor or Wisher).
    URL: /register/
    """
    template_name = 'core/auth/register_choice.html'

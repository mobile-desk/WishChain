from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from ..models import User
from .fields import CountryField

class BaseRegistrationForm(UserCreationForm):
    """Base form with common fields for both wisher and donor registration."""
    email = forms.EmailField(required=True)
    full_name = forms.CharField(max_length=150, required=True)
    country = CountryField(required=True, label=_("Country"))
    city = forms.CharField(
        required=True, 
        label=_("City/Region"),
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your city/region',
            'class': 'w-full px-4 py-3 bg-background/50 border border-border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent text-white placeholder-subtle/70'
        })
    )
    language = forms.ChoiceField(
        choices=[
            ('en', 'English'),
            ('fr', 'Français'),
            ('ar', 'العربية'),
            # Add more languages as needed
        ],
        required=False,
        initial='en'
    )
    terms_accepted = forms.BooleanField(
        required=True,
        label='I agree to the Terms & Privacy Policy'
    )

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        role = kwargs.pop('role', None)
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        
        # Common field classes
        input_class = 'w-full px-4 py-3 bg-background/50 border border-border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent text-white placeholder-subtle/70'
        
        # Update field widgets
        self.fields['full_name'].widget.attrs.update({
            'class': input_class,
            'placeholder': 'Your full name'
        })
        self.fields['email'].widget.attrs.update({
            'class': input_class,
            'placeholder': 'your@email.com'
        })
        self.fields['password1'].widget.attrs.update({
            'class': input_class,
            'placeholder': '••••••••'
        })
        self.fields['password2'].widget.attrs.update({
            'class': input_class,
            'placeholder': '••••••••'
        })
        self.fields['country'].widget.attrs.update({
            'class': f'{input_class} appearance-none',
            'style': 'background-image: url("data:image/svg+xml,%3csvg xmlns=\'http://www.w3.org/2000/svg\' fill=\'none\' viewBox=\'0 0 20 20\'%3e%3cpath stroke=\'%239ca3af\' stroke-linecap=\'round\' stroke-linejoin=\'round\' stroke-width=\'1.5\' d=\'M6 8l4 4 4-4\'/%3e%3c/svg%3e"); background-position: right 0.75rem center; background-repeat: no-repeat; background-size: 1.5em 1.5em; padding-right: 2.5rem;',
            'placeholder': 'Select a country'
        })
        self.fields['city'].widget.attrs.update({
            'class': input_class,
            'placeholder': 'Enter your city/region'
        })
        self.fields['language'].widget.attrs.update({
            'class': f'{input_class} appearance-none',
            'style': 'background-image: url(\'data:image/svg+xml,%3csvg xmlns=\'http://www.w3.org/2000/svg\' fill=\'none\' viewBox=\'0 0 20 20\'%3e%3cpath stroke=\'%239ca3af\' stroke-linecap=\'round\' stroke-linejoin=\'round\' stroke-width=\'1.5\' d=\'M6 8l4 4 4-4\'/%3e%3c/svg%3e\'); background-position: right 0.75rem center; background-repeat: no-repeat; background-size: 1.5em 1.5em; padding-right: 2.5rem;'
        })
        self.fields['terms_accepted'].widget.attrs.update({
            'class': 'h-4 w-4 rounded border-border bg-background text-primary focus:ring-primary/50'
        })
        
        # Reorder fields
        field_order = [
            'full_name', 'email', 'password1', 'password2',
            'country', 'city', 'language', 'terms_accepted'
        ]
        self.order_fields(field_order)

    def save(self, commit=True):
        user = super().save(commit=False)
        # Split full_name into first_name and last_name
        full_name = self.cleaned_data.get('full_name', '').strip()
        if full_name:
            name_parts = full_name.split(maxsplit=1)
            user.first_name = name_parts[0] if len(name_parts) > 0 else ''
            user.last_name = name_parts[1] if len(name_parts) > 1 else ''
        else:
            # Fallback if full_name is somehow empty
            user.first_name = ''
            user.last_name = ''
        
        user.country = self.cleaned_data.get('country', '')
        user.city = self.cleaned_data.get('city', '').strip()
        # Always default to 'en' if language is not provided
        user.language_preference = self.cleaned_data.get('language') or 'en'
        if commit:
            user.save()
        return user

class DonorRegistrationForm(BaseRegistrationForm):
    """Registration form for donors."""
    # List of fields that should be rendered using custom templates
    custom_fields = ['display_name', 'hear_about', 'giving_focus', 'show_display_name', 'is_anonymous']
    
    display_name = forms.CharField(
        max_length=100,
        required=False,
        help_text='What name should be displayed publicly? (Optional)',
        widget=forms.TextInput(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm',
            'placeholder': 'e.g., "Anonymous Angel" or your name'
        })
    )
    
    hear_about = forms.ChoiceField(
        choices=[
            ('', 'How did you hear about WishChain?'),
            ('search', 'Search Engine'),
            ('social', 'Social Media'),
            ('friend', 'Friend or Family'),
            ('other', 'Other')
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 bg-background/50 border border-border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent text-white placeholder-subtle/70',
            'style': 'appearance: none; background-image: url("data:image/svg+xml,%3csvg xmlns=\'http://www.w3.org/2000/svg\' fill=\'none\' viewBox=\'0 0 20 20\'%3e%3cpath stroke=\'%239ca3af\' stroke-linecap=\'round\' stroke-linejoin=\'round\' stroke-width=\'1.5\' d=\'M6 8l4 4 4-4\'/%3e%3c/svg%3e"); background-position: right 0.5rem center; background-repeat: no-repeat; background-size: 1.5em 1.5em; padding-right: 2.5rem;'
        })
    )
    
    giving_focus = forms.MultipleChoiceField(
        choices=[
            ('children', 'Children'),
            ('education', 'Education'),
            ('food', 'Food'),
            ('health', 'Health'),
            ('shelter', 'Shelter')
        ],
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'grid grid-cols-2 gap-4 mt-2'
        }),
        label='Causes I care about (select any)'
    )
    
    show_display_name = forms.BooleanField(
        required=False,
        initial=True,
        label='Show my display name on wishes I grant',
        widget=forms.CheckboxInput(attrs={
            'class': 'h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500'
        })
    )
    
    is_anonymous = forms.BooleanField(
        required=False,
        label='Keep my contributions anonymous',
        widget=forms.CheckboxInput(attrs={
            'class': 'h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **{'role': 'donor', **kwargs})
        
        # Set language field to hidden with default value 'en'
        self.fields['language'].widget = forms.HiddenInput()
        self.fields['language'].initial = 'en'
        
        # Make city optional for donors
        self.fields['city'].required = False
        
        # Common field classes
        input_class = 'w-full px-4 py-3 bg-background/50 border border-border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent text-white placeholder-subtle/70'
        select_class = 'w-full px-4 py-3 bg-background/50 border border-border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent text-white placeholder-subtle/70 appearance-none bg-[url("data:image/svg+xml,%3csvg xmlns=\'http://www.w3.org/2000/svg\' fill=\'none\' viewBox=\'0 0 20 20\'%3e%3cpath stroke=\'%23E5E7EB\' stroke-linecap=\'round\' stroke-linejoin=\'round\' stroke-width=\'1.5\' d=\'M6 8l4 4 4-4\'/%3e%3c/svg%3e")] bg-no-repeat bg-[right_0.75rem_center] bg-[length:1.25em_1.25em] pr-10'
        
        # Update widget classes for base fields
        self.fields['full_name'].widget.attrs.update({
            'class': input_class,
            'placeholder': 'Your full name'
        })
        self.fields['email'].widget.attrs.update({
            'class': input_class,
            'placeholder': 'your@email.com'
        })
        self.fields['password1'].widget.attrs.update({
            'class': input_class,
            'placeholder': '••••••••'
        })
        self.fields['password2'].widget.attrs.update({
            'class': input_class,
            'placeholder': '••••••••'
        })
        self.fields['country'].widget.attrs.update({
            'class': select_class,
            'placeholder': 'Select a country'
        })
        # Make city a text input instead of select for donor registration
        self.fields['city'].widget = forms.TextInput(attrs={
            'class': input_class,
            'placeholder': 'Enter your city/region (optional)'
        })
        self.fields['language'].widget.attrs.update({
            'class': select_class
        })
        self.fields['terms_accepted'].widget.attrs.update({
            'class': 'h-4 w-4 rounded border-border text-primary focus:ring-primary bg-background/50'
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'donor'
        if commit:
            user.save()
            # Create or update donor profile
            from partners.models import DonorProfile
            donor_profile, created = DonorProfile.objects.get_or_create(user=user)
            
            # Update donor profile fields
            donor_profile.display_name = self.cleaned_data.get('display_name', '')
            donor_profile.hear_about = self.cleaned_data.get('hear_about')
            donor_profile.giving_focus = self.cleaned_data.get('giving_focus', [])
            donor_profile.show_display_name = self.cleaned_data.get('show_display_name', False)
            donor_profile.is_anonymous = self.cleaned_data.get('is_anonymous', False)
            donor_profile.save()
            
        return user

class WisherRegistrationForm(BaseRegistrationForm):
    """Registration form for wishers."""
    user_type = forms.ChoiceField(
        choices=[
            ('individual', 'Individual in need'),
            ('parent', 'Parent/Guardian'),
            ('teacher', 'Teacher/School'),
            ('community', 'Community Helper/NGO Worker')
        ],
        required=True,
        label='Who are you?'
    )
    household_size = forms.IntegerField(
        required=False,
        min_value=1,
        initial=1,
        help_text='How many people are you caring for? (Including yourself)',
        widget=forms.NumberInput(attrs={'min': 1})
    )
    help_needed = forms.MultipleChoiceField(
        choices=[
            ('education', 'Education'),
            ('food', 'Food'),
            ('health', 'Health'),
            ('shelter', 'Shelter'),
            ('other', 'Other')
        ],
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='What kind of help do you need? (Select all that apply)'
    )
    contact_preference = forms.ChoiceField(
        choices=[
            ('email', 'Email'),
            ('phone', 'Phone'),
            ('whatsapp', 'WhatsApp')
        ],
        required=False,
        label='Best way to reach you',
        help_text='We may need to contact you for more information'
    )
    phone_number = forms.CharField(
        required=False,
        max_length=20,
        help_text='Optional, but helps us reach you faster'
    )
    has_children = forms.BooleanField(
        required=False,
        initial=False,
        label='Do you have children?',
        widget=forms.CheckboxInput(attrs={
            'class': 'sr-only peer'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **{'role': 'wisher', **kwargs})
        
        # Set language field to hidden with default value 'en'
        self.fields['language'].widget = forms.HiddenInput()
        self.fields['language'].initial = 'en'
        
        # Common field classes
        input_class = 'w-full px-4 py-3 bg-background/50 border border-border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent text-white placeholder-subtle/70'
        
        # Update widget classes
        self.fields['user_type'].widget.attrs.update({
            'class': f'{input_class} appearance-none',
            'style': 'background-image: url("data:image/svg+xml,%3csvg xmlns=\'http://www.w3.org/2000/svg\' fill=\'none\' viewBox=\'0 0 20 20\'%3e%3cpath stroke=\'%239ca3af\' stroke-linecap=\'round\' stroke-linejoin=\'round\' stroke-width=\'1.5\' d=\'M6 8l4 4 4-4\'/%3e%3c/svg%3e"); background-position: right 0.75rem center; background-repeat: no-repeat; background-size: 1.5em 1.5em; padding-right: 2.5rem;'
        })
        
        # Update household size field
        self.fields['household_size'].widget.attrs.update({
            'class': input_class,
            'min': '1',
            'value': '1'
        })
        
        # Update help needed checkboxes
        self.fields['help_needed'].widget.attrs.update({
            'class': 'grid grid-cols-2 gap-4 mt-2'
        })
        
        # Update contact preference radio buttons
        self.fields['contact_preference'].widget.attrs.update({
            'class': 'grid grid-cols-3 gap-4 mt-2'
        })
        
        # Update phone number field
        self.fields['phone_number'].widget.attrs.update({
            'class': input_class,
            'placeholder': 'e.g., +1234567890'
        })
        
        # Update city field
        self.fields['city'].widget.attrs.update({
            'class': input_class,
            'placeholder': 'Enter your city/region',
            'required': 'required'
        })
        
        # Remove any HTMX attributes from the country field
        if 'hx-get' in self.fields['country'].widget.attrs:
            del self.fields['country'].widget.attrs['hx-get']
            del self.fields['country'].widget.attrs['hx-target']
            del self.fields['country'].widget.attrs['hx-trigger']
            
    def clean_language(self):
        """Ensure language defaults to 'en' if not provided."""
        language = self.cleaned_data.get('language', 'en')
        return language if language else 'en'
            
    def clean(self):
        cleaned_data = super().clean()
        country = cleaned_data.get('country')
        city = cleaned_data.get('city', '').strip()
        
        # Ensure language defaults to 'en' if not provided
        if 'language' not in cleaned_data or not cleaned_data.get('language'):
            cleaned_data['language'] = 'en'
        
        # Additional validation can be added here if needed
        
        # If country is selected but city is empty, add an error
        if country and not city:
            self.add_error('city', _('Please enter your city or region'))
            
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'wisher'
        # Save phone number if provided
        user.phone_number = self.cleaned_data.get('phone_number', '')
        
        if commit:
            user.save()
            # Create WisherProfile
            try:
                from wishes.models.wisher_profile import WisherProfile
                wisher_profile, created = WisherProfile.objects.get_or_create(user=user)
                
                # Update wisher profile fields
                household_size = self.cleaned_data.get('household_size')
                if household_size:
                    wisher_profile.household_size = household_size
                    
                    # Determine income bracket based on household size (simple logic)
                    # This can be enhanced later
                    if household_size <= 2:
                        wisher_profile.income_bracket = 'below_average'
                    elif household_size <= 4:
                        wisher_profile.income_bracket = 'average'
                    else:
                        wisher_profile.income_bracket = 'above_average'
                
                wisher_profile.save()
            except Exception as e:
                # Log the error but don't fail registration if profile creation fails
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Error creating WisherProfile: {str(e)}")
                # Continue without profile - it can be created later
            
        return user


class UserLoginForm(AuthenticationForm):
    """
    Custom login form that uses email instead of username.
    """
    username = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(attrs={
            'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50',
            'placeholder': 'your@email.com',
            'autocomplete': 'email',
        })
    )
    password = forms.CharField(
        label=_('Password'),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50',
            'placeholder': '••••••••',
            'autocomplete': 'current-password',
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        label=_('Remember me'),
        widget=forms.CheckboxInput(attrs={
            'class': 'rounded border-gray-300 text-indigo-600 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50',
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = _('Email')
        self.fields['password'].label = _('Password')
        self.fields['username'].widget.attrs.update({'autofocus': True})

    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username.lower()  # Store emails in lowercase for consistency

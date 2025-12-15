from django.db import models
from django.conf import settings

class Partner(models.Model):
    """Model for organizations that can verify wishers"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='partner_profile'
    )
    organization_name = models.CharField(max_length=255)
    organization_description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='partner_logos/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    verification_document = models.FileField(
        upload_to='partner_docs/',
        blank=True,
        null=True,
        help_text='Upload organization verification document'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Partner Organization'
        verbose_name_plural = 'Partner Organizations'

    def __str__(self):
        return self.organization_name

class DonorProfile(models.Model):
    """Extended profile for donors"""
    HEAR_ABOUT_CHOICES = [
        ('search', 'Search Engine (Google, Bing, etc.)'),
        ('social', 'Social Media'),
        ('friend', 'Friend or Family'),
        ('news', 'News Article or Blog'),
        ('other', 'Other')
    ]
    
    GIVING_FOCUS_CHOICES = [
        ('children', 'Children'),
        ('education', 'Education'),
        ('food', 'Food'),
        ('health', 'Health'),
        ('shelter', 'Shelter')
    ]
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='donor_profile'
    )
    display_name = models.CharField(
        max_length=100,
        help_text='What shows publicly (e.g., "Anonymous Angel", "Ada from Lagos")',
        blank=True,
        null=True
    )
    hear_about = models.CharField(
        max_length=20,
        choices=HEAR_ABOUT_CHOICES,
        blank=True,
        null=True,
        help_text='How did you hear about WishChain?'
    )
    giving_focus = models.JSONField(
        default=list,
        help_text='Preferred giving focus areas (e.g., ["education", "health"])'
    )
    show_display_name = models.BooleanField(
        default=False,
        help_text='Show my display name on wishes I grant'
    )
    is_anonymous = models.BooleanField(
        default=False,
        help_text='Keep my contributions anonymous'
    )
    preferred_categories = models.JSONField(
        default=list,
        help_text='List of preferred wish categories (e.g., ["education", "health"])'
    )
    impact_score = models.FloatField(
        default=0.0,
        help_text='Score based on donations and impact'
    )
    visibility = models.BooleanField(
        default=True,
        help_text='Whether the donor wants to be visible to others'
    )
    total_donations = models.PositiveIntegerField(
        default=0,
        help_text='Total number of wishes fulfilled'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Donor Profile'
        verbose_name_plural = 'Donor Profiles'

    def __str__(self):
        return f"{self.user.email}'s Donor Profile"

    def update_impact_score(self):
        """Update the impact score based on donations and other factors"""
        # This can be customized based on your scoring algorithm
        self.impact_score = self.total_donations * 10  # Example calculation
        self.save()

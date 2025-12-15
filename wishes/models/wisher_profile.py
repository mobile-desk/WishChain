from django.db import models
from django.conf import settings
from partners.models import Partner

class WisherProfile(models.Model):
    """Extended profile for users who are making wishes"""
    INCOME_BRACKETS = (
        ('below_average', 'Below Average'),
        ('average', 'Average'),
        ('above_average', 'Above Average'),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wisher_profile'
    )
    verified_by = models.ForeignKey(
        Partner,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_wishers'
    )
    household_size = models.PositiveIntegerField(blank=True, null=True)
    income_bracket = models.CharField(
        max_length=50,
        choices=INCOME_BRACKETS,
        blank=True,
        null=True
    )
    id_document = models.FileField(
        upload_to='id_documents/',
        null=True,
        blank=True,
        help_text='Upload a government-issued ID for verification'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Wisher Profile'
        verbose_name_plural = 'Wisher Profiles'

    def __str__(self):
        return f"{self.user.email}'s Wisher Profile"

    @property
    def is_verified(self):
        """Check if wisher is verified by a partner"""
        return self.verified_by is not None

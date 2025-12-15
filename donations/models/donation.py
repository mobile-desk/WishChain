from django.db import models
from django.conf import settings
from wishes.models.wish import Wish

class Donation(models.Model):
    """Model to track donations/grants of wishes"""
    wish = models.ForeignKey(
        Wish,
        on_delete=models.CASCADE,
        related_name='donations'
    )
    donor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='donations'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(
        blank=True,
        null=True,
        help_text='Optional notes about the donation'
    )
    
    class Meta:
        verbose_name = 'Donation'
        verbose_name_plural = 'Donations'
        ordering = ['-created_at']
        unique_together = ['wish', 'donor']  # Prevent duplicate donations
    
    def __str__(self):
        return f"{self.donor.email} granted '{self.wish.title}'"


from django.db import models
from django.contrib.auth import get_user_model

class Wish(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('fulfilled', 'Fulfilled'),
        ('expired', 'Expired'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='wishes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name_plural = 'Wishes'
        ordering = ['-created_at']

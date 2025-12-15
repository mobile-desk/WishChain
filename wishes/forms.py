from django import forms
from wishes.models.wish import Wish

class WishForm(forms.ModelForm):
    title = forms.CharField(
        label='Wish Title',
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-background-dark/50 border border-white/10 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent text-white placeholder-white/40 transition-all',
            'placeholder': 'e.g., School supplies for my children',
        }),
        help_text='A short title for your wish (e.g., "New Laptop for School")',
    )
    
    description = forms.CharField(
        label='Description',
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-3 bg-background-dark/50 border border-white/10 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent text-white placeholder-white/40 transition-all resize-none',
            'placeholder': 'Tell us more about your wish. What do you need and why is it important to you?',
            'rows': 6,
        }),
        help_text='Tell us more about your wish and why it\'s important to you',
    )
    
    class Meta:
        model = Wish
        fields = ['title', 'description']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add any additional initialization here

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from wishes.models.wish import Wish

class DonateView(LoginRequiredMixin, TemplateView):
    """View for the donation page."""
    template_name = 'donations/donate.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all wishes, prioritizing pending ones
        wishes = Wish.objects.all().order_by('-created_at')
        
        context.update({
            'wishes': wishes,
            'pending_wishes_count': Wish.objects.filter(status='pending').count(),
            'fulfilled_wishes_count': Wish.objects.filter(status='fulfilled').count(),
            'total_wishes_count': Wish.objects.count(),
        })
        return context

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from wishes.models.wish import Wish

class WishDashboardView(LoginRequiredMixin, TemplateView):
    """View for the wisher's dashboard."""
    template_name = 'wishes/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        wishes = Wish.objects.filter(user=user)
        
        context.update({
            'wishes': wishes.order_by('-created_at'),
            'total_wishes': wishes.count(),
            'pending_wishes': wishes.filter(status='pending').count(),
            'fulfilled_wishes': wishes.filter(status='fulfilled').count(),
        })
        return context

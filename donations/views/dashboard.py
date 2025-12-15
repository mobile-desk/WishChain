from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class DonorDashboardView(LoginRequiredMixin, TemplateView):
    """View for the donor's dashboard."""
    template_name = 'donations/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any context data needed for the dashboard
        # context['donations'] = self.request.user.donations.all()
        return context

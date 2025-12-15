import logging
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from ..forms import WishForm

logger = logging.getLogger(__name__)

class CreateWishView(LoginRequiredMixin, CreateView):
    """View for creating a new wish."""
    template_name = 'wishes/simple_wish_form.html'
    form_class = WishForm
    success_url = reverse_lazy('wishes:dashboard')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Your wish has been created successfully!')
        return super().form_valid(form)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Make a Wish'
        # Debug information
        logger.debug(f"Form in context: {context.get('form')}")
        logger.debug(f"Form fields: {[f.name for f in context.get('form').visible_fields()] if context.get('form') else 'No form'}")
        return context

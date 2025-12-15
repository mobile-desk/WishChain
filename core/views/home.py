from django.views.generic import TemplateView
from django.db.models import Count

class HomeView(TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get some stats for the homepage
        context.update({
            'featured_wishes': [],  # Will be populated when we have the Wish model
            'stats': {
                'wishes_granted': 0,  # Will be updated when we have data
                'donors_count': 0,    # Will be updated when we have users
                'countries_count': 0,  # Will be updated with location data
            },
            'how_it_works': [
                {
                    'title': 'Make a Wish',
                    'description': 'Share your need or the need of someone you know',
                    'icon': '🎯',
                },
                {
                    'title': 'Get Verified',
                    'description': 'Our team reviews each wish to ensure legitimacy',
                    'icon': '✅',
                },
                {
                    'title': 'Wish Granted',
                    'description': 'Generous donors from around the world fulfill wishes',
                    'icon': '✨',
                },
            ]
        })
        return context
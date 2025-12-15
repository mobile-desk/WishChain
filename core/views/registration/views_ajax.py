import logging
from django.http import JsonResponse
from django.views import View
from django.utils.translation import gettext_lazy as _
from cities_light.models import City, Country

logger = logging.getLogger(__name__)

class GetCitiesView(View):
    """View to get cities for a given country code or name."""
    def get(self, request, *args, **kwargs):
        country_code = request.GET.get('country_code', '').upper()
        
        if not country_code:
            return JsonResponse({'error': _('Country code is required')}, status=400)
        
        logger.info(f"Looking up cities for country code: {country_code}")
        
        # Try to find the country by different fields
        country = (
            Country.objects.filter(code2=country_code).first() or
            Country.objects.filter(name__iexact=country_code).first() or
            Country.objects.filter(name_ascii__iexact=country_code).first()
        )
        
        if not country:
            logger.warning(f"Country not found for code/name: {country_code}")
            return JsonResponse({'cities': []})
        
        logger.info(f"Found country: {country.name} (code2: {country.code2}, code3: {getattr(country, 'code3', 'N/A')})")
        
        # Get cities for the country
        cities = City.objects.filter(country=country)\
                           .order_by('name')\
                           .values('id', 'name', 'region__name')
        
        logger.info(f"Found {cities.count()} cities for {country.name}")
        
        # Format cities as (id, display_name)
        city_choices = [
            {
                'id': city['id'],
                'name': f"{city['name']}, {city['region__name']}" if city['region__name'] else city['name']
            }
            for city in cities
        ]
        
        return JsonResponse({
            'cities': city_choices,
            'debug': {
                'country': country.name,
                'code2': country.code2,
                'total_cities': len(city_choices)
            }
        })

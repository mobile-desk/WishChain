from django import forms
import pycountry
from cities_light.models import Country, City
from django.utils.translation import gettext_lazy as _

class CountrySelectWidget(forms.Select):
    """Widget for country selection with theme styling."""
    def __init__(self, attrs=None, choices=()):
        default_attrs = {
            'class': 'block w-full px-4 py-3 text-sm bg-background/50 border border-border/50 rounded-lg text-white focus:ring-2 focus:ring-primary/50 focus:border-primary',
            'style': 'appearance: none; background-image: url(\'data:image/svg+xml,%3csvg xmlns=\'http://www.w3.org/2000/svg\' fill=\'none\' viewBox=\'0 0 20 20\'%3e%3cpath stroke=\'%23E5E7EB\' stroke-linecap=\'round\' stroke-linejoin=\'round\' stroke-width=\'1.5\' d=\'M6 8l4 4 4-4\'/%3e%3c/svg%3e\'); background-repeat: no-repeat; background-position: right 0.75rem center; background-size: 1.25em 1.25em;'
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs, choices=choices)

    def create_option(self, name, value, *args, **kwargs):
        option = super().create_option(name, value, *args, **kwargs)
        if value:
            try:
                country = pycountry.countries.get(alpha_2=value)
                option['label'] = country.name
                option['attrs'] = {
                    'class': 'bg-background/50 text-white hover:bg-background/70',
                    'style': 'background-color: #012A34; color: white; padding: 0.5rem 1rem;'
                }
            except (KeyError, AttributeError):
                option['attrs'] = {'class': 'bg-background/50 text-white'}
        return option

class CountryField(forms.ChoiceField):
    """A form field for selecting a country."""
    widget = CountrySelectWidget

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = self._get_country_choices()

    def _get_country_choices(self):
        """Return a list of tuples of (country_code, country_name) sorted by name."""
        countries = [(country.alpha_2, country.name) 
                    for country in pycountry.countries]
        return [("", _("Select a country"))] + sorted(countries, key=lambda x: x[1])

class CityField(forms.ChoiceField):
    """A form field for selecting a city, filtered by country."""
    widget = forms.Select(attrs={
        'class': 'block w-full px-4 py-3 text-sm bg-background/50 border border-border/50 rounded-lg text-white focus:ring-2 focus:ring-primary/50 focus:border-primary',
        'style': 'appearance: none; background-image: url("data:image/svg+xml,%3csvg xmlns=\'http://www.w3.org/2000/svg\' fill=\'none\' viewBox=\'0 0 20 20\'%3e%3cpath stroke=\'%23E5E7EB\' stroke-linecap=\'round\' stroke-linejoin=\'round\' stroke-width=\'1.5\' d=\'M6 8l4 4 4-4\'/%3e%3c/svg%3e"); background-repeat: no-repeat; background-position: right 0.75rem center; background-size: 1.25em 1.25em;',
        'disabled': 'disabled'
    })

    def __init__(self, *args, **kwargs):
        country_code = kwargs.pop('country_code', None)
        super().__init__(*args, **kwargs)
        self.country_code = country_code
        self.choices = self._get_city_choices()

    def _get_city_choices(self):
        """Return a list of tuples of (city_id, city_name) for the selected country."""
        if not self.country_code:
            return [("", _("Select a country first"))]
            
        cities = City.objects.filter(country__code2=self.country_code)\
                           .order_by('name')\
                           .values_list('id', 'name', 'region__name', 'country__name')
        
        # Format as (id, "City, Region, Country")
        return [("", _("Select a city"))] + [
            (city[0], f"{city[1]}, {city[2] or 'N/A'}, {city[3]}")
            for city in cities
        ]

    def set_country(self, country_code):
        """Update the choices based on the selected country."""
        self.country_code = country_code
        self.choices = self._get_city_choices()
        self.widget.attrs['disabled'] = 'disabled' if not country_code else ''

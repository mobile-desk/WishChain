from django.core.management.base import BaseCommand
from django.db import transaction
from cities_light.models import Country, City

class Command(BaseCommand):
    help = 'Import test cities for existing countries'

    def handle(self, *args, **options):
        # Dictionary of country codes to their cities
        country_cities = {
            'US': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
            'CA': ['Toronto', 'Vancouver', 'Montreal', 'Calgary', 'Ottawa'],
            'GB': ['London', 'Manchester', 'Birmingham', 'Glasgow', 'Liverpool'],
            'DE': ['Berlin', 'Munich', 'Hamburg', 'Cologne', 'Frankfurt'],
            'FR': ['Paris', 'Marseille', 'Lyon', 'Toulouse', 'Nice']
        }

        with transaction.atomic():
            for country_code, cities in country_cities.items():
                try:
                    country = Country.objects.get(code2=country_code)
                    for city_name in cities:
                        city, created = City.objects.get_or_create(
                            country=country,
                            name=city_name,
                            defaults={
                                'name_ascii': city_name,
                                'slug': city_name.lower().replace(' ', '-')
                            }
                        )
                        if created:
                            self.stdout.write(self.style.SUCCESS(f'Created city: {city_name}, {country.name}'))
                        else:
                            self.stdout.write(self.style.WARNING(f'City already exists: {city_name}, {country.name}'))
                except Country.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Country not found: {country_code}'))

        self.stdout.write(self.style.SUCCESS(f'Total cities in database: {City.objects.count()}'))

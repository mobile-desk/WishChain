from django.core.management.base import BaseCommand
from django.db import transaction
from cities_light.models import Country

class Command(BaseCommand):
    help = 'Manually import countries data'

    def handle(self, *args, **options):
        # List of countries to import (US and a few others for testing)
        countries = [
            {'name': 'United States', 'code2': 'US', 'code3': 'USA'},
            {'name': 'Canada', 'code2': 'CA', 'code3': 'CAN'},
            {'name': 'United Kingdom', 'code2': 'GB', 'code3': 'GBR'},
            {'name': 'Germany', 'code2': 'DE', 'code3': 'DEU'},
            {'name': 'France', 'code2': 'FR', 'code3': 'FRA'},
        ]

        with transaction.atomic():
            for country_data in countries:
                country, created = Country.objects.get_or_create(
                    code2=country_data['code2'],
                    defaults={
                        'name': country_data['name'],
                        'code3': country_data['code3'],
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created country: {country.name} ({country.code2})'))
                else:
                    self.stdout.write(self.style.WARNING(f'Country already exists: {country.name} ({country.code2})'))

        self.stdout.write(self.style.SUCCESS(f'Total countries in database: {Country.objects.count()}'))

from django.core.management.base import BaseCommand
from django.db import transaction
from cities_light.models import Country, City
from cities_light.management.commands.cities_light import Command as CitiesLightCommand

class Command(BaseCommand):
    help = 'Import cities_light data with progress and error handling'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting cities_light import...'))
        
        # Import data using cities_light's command
        cmd = CitiesLightCommand()
        cmd.handle(**{**options, 'force_import': True, 'progress': True})
        
        # Verify the import
        country_count = Country.objects.count()
        city_count = City.objects.count()
        
        self.stdout.write(self.style.SUCCESS(f'Import complete!'))
        self.stdout.write(self.style.SUCCESS(f'Countries: {country_count}'))
        self.stdout.write(self.style.SUCCESS(f'Cities: {city_count}'))
        
        if country_count == 0:
            self.stdout.write(self.style.ERROR('No countries were imported. There might be an issue with the data source.'))
        if city_count == 0:
            self.stdout.write(self.style.ERROR('No cities were imported. There might be an issue with the data source.'))

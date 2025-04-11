from django.core.management.base import BaseCommand
from voyage.models import Pays, Ville  # Change 'core' en 'voyage'
import requests

class Command(BaseCommand):
    help = 'Populate countries and cities'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Ville.objects.all().delete()
        Pays.objects.all().delete()

        # Get countries from API
        countries_response = requests.get("https://countriesnow.space/api/v0.1/countries")
        countries = countries_response.json()["data"]

        # Insert countries and cities into the database
        for country in countries:
            pays_obj = Pays.objects.create(nom=country["country"])
            for ville in country["cities"]:
                Ville.objects.create(nom=ville, pays=pays_obj)

        self.stdout.write(self.style.SUCCESS("Base de données peuplée avec succès"))

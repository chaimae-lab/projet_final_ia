# voyage/management/commands/peupler_adresses.py

from django.core.management.base import BaseCommand
from voyage.models import Ville, Adresse
import requests
import time

# Fonction katsift city name w trj3 les adresses
def get_addresses_for_city(city_name):
    url = f"https://nominatim.openstreetmap.org/search?city={city_name}&format=json&limit=5"
    headers = {
        "User-Agent": "MyDjangoApp/1.0"
    }
    response = requests.get(url, headers=headers)
    return response.json()

class Command(BaseCommand):
    help = 'Peupler la table Adresse automatiquement depuis les villes'

    def handle(self, *args, **kwargs):
        for ville in Ville.objects.all():
            self.stdout.write(f"Tqddar tji adresses dial : {ville.nom}")
            try:
                results = get_addresses_for_city(ville.nom)
                for result in results:
                    Adresse.objects.create(
                        rue=result.get("display_name", "Adresse inconnue"),
                        code_postal=result.get("postcode", None),
                        ville=ville
                    )
                time.sleep(1)  # khas delay bach ma yblocawch lik l’API
            except Exception as e:
                self.stderr.write(f"Erreur m3a {ville.nom}: {str(e)}")

        self.stdout.write(self.style.SUCCESS("Adresses insérées avec succès"))

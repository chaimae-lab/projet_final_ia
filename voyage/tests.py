from django.test import TestCase   #Elle prépare automatiquement une base de données temporaire isolée pour chaque test,
from django.contrib.auth.models import User
from voyage.models import CritereVoyage, Ville, Pays
from django.urls import reverse
from datetime import date, timedelta
import random
import string

class PlanVoyageTest(TestCase):
    def setUp(self):
        # Création d’un utilisateur fictif
        self.user = User.objects.create_user(username='user_' + self._random_string(5), password='testpass')

        # Création d’un pays et d’une ville avec des noms random
        self.pays = Pays.objects.create(nom='Pays_' + self._random_string(4))
        self.ville = Ville.objects.create(nom='Ville_' + self._random_string(4), pays=self.pays)

        # Dates aléatoires
        today = date.today()
        date_depart = today + timedelta(days=random.randint(1, 30))
        date_retour = date_depart + timedelta(days=random.randint(3, 10))

        # Création d’un CritereVoyage avec données random
        self.critere = CritereVoyage.objects.create(
            utilisateur=self.user,
            adresse="Rue " + self._random_string(6),
            date_depart=date_depart,
            date_retour=date_retour,
            budget_total=random.randint(1000, 5000),
            type_voyage=random.choice(["Détente", "Culture", "Aventure"]),
            voyageurs_enfant=random.randint(0, 3),
            voyageurs_jeune=random.randint(0, 2),
            voyageurs_adulte=random.randint(1, 4),
            voyageurs_senior=random.randint(0, 2),
            api_choisie="deepseek"
        )
        self.critere.ville_destination.add(self.ville)
        self.critere.pays_arrivee.add(self.pays)

    def _random_string(self, length):
        return ''.join(random.choices(string.ascii_letters, k=length))

    def test_generation_plan_voyage(self):
        url = reverse('plan_travel', args=[self.critere.id])
        response = self.client.get(url)  # GET ou POST selon la vue
        self.assertEqual(response.status_code, 200)

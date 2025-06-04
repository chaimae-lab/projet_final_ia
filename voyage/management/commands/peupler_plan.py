from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from voyage.models import CritereVoyage, Ville, Pays
from django.test import Client
from django.urls import reverse
import random
import string
from datetime import date, timedelta


def random_string(length):
    return ''.join(random.choices(string.ascii_letters, k=length))


class Command(BaseCommand):
    print("📍 Commande démarrée")

    help = "Peuple la base et génère un plan de voyage"

    def handle(self, *args, **kwargs):
        user = User.objects.create_user(username='user_' + random_string(5), password='testpass')
        print("👤 Utilisateur créé :", user.username)

        pays = Pays.objects.create(nom='Pays_' + random_string(4))
        print("🌍 Pays créé :", pays.nom)

        ville = Ville.objects.create(nom='Ville_' + random_string(4), pays=pays)
        print("🏙️ Ville créée :", ville.nom)

        today = date.today()
        date_depart = today + timedelta(days=random.randint(1, 30))
        date_retour = date_depart + timedelta(days=random.randint(3, 10))

        critere = CritereVoyage.objects.create(
            utilisateur=user,
            adresse="Rue " + random_string(6),
            date_depart=date_depart,
            date_retour=date_retour,
            budget_total=random.randint(1000, 5000),
            type_voyage=random.choice(["Détente", "Culture", "Aventure"]),
            voyageurs_enfant=random.randint(0, 3),
            voyageurs_jeune=random.randint(0, 2),
            voyageurs_adulte=random.randint(1, 4),
            voyageurs_senior=random.randint(0, 2),
           # api_choisie="deepseek"
            api_choisie=random.choice(["deepseek", "openai"])

        )
        print("📝 Critère créé :", critere.id)

        critere.ville_destination.add(ville)
        critere.pays_arrivee.add(pays)
        print("📍 Ville + pays ajoutés au critère")

        client = Client()
        client.force_login(user)
        print("🔐 Utilisateur connecté via Client test")

        try:
            url = reverse('plan_travel', args=[critere.id])
            print("📡 URL générée :", url)
        except Exception as e:
            print("❌ Erreur dans reverse() :", str(e))
            return

        try:
            response = client.get(url)
            print("📦 Status de la réponse :", response.status_code)
            print("📨 Contenu brut :", response.content.decode())
        except Exception as e:
            print("❌ Erreur lors de la requête GET :", str(e))
            return

        if response.status_code == 200:
            self.stdout.write(self.style.SUCCESS("✅ Plan généré avec succès et critère enregistré."))
        else:
            self.stdout.write(self.style.ERROR(f"❌ Erreur lors de la génération du plan : {response.status_code}"))


# execution python manage.py peupler_plan
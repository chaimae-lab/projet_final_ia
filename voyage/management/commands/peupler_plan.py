from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from voyage.models import CritereVoyage, Ville, Pays
from django.test import Client
from django.urls import reverse
import random
import string
from datetime import date, timedelta, datetime


def random_string(length):
    return ''.join(random.choices(string.ascii_letters, k=length))


class Command(BaseCommand):
    help = "Peuple la base et génère un plan de voyage"

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=1,
            help='Nombre de plans de voyage à générer (par défaut: 1)'
        )

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        success_count = 0

        print(f"[{datetime.now()}] 📍 Commande démarrée - Génération de {count} plan(s) de voyage")

        try:
            for i in range(count):
                print(f"\n[{datetime.now()}] --- Génération numéro {i + 1} ---")

                user = User.objects.create_user(username='user_' + random_string(5), password='testpass')
                print(f"[{datetime.now()}] 👤 Utilisateur créé : {user.username}")

                # 📌 Récupérer les pays qui ont au moins une ville
                pays_possibles = Pays.objects.filter(ville__isnull=False).distinct()

                if not pays_possibles.exists():
                    self.stderr.write(self.style.ERROR("❌ Aucun pays avec des villes disponibles dans la base."))
                    return

                pays = random.choice(list(pays_possibles))
                villes_dans_pays = Ville.objects.filter(pays=pays)

                if not villes_dans_pays.exists():
                    self.stderr.write(self.style.ERROR(f"❌ Aucune ville trouvée pour le pays {pays.nom}."))
                    return

                ville = random.choice(list(villes_dans_pays))

                print(f"[{datetime.now()}] 🌍 Pays choisi : {pays.nom}")
                print(f"[{datetime.now()}] 🏙️ Ville choisie : {ville.nom}")

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
                    api_choisie=random.choice(["deepseek", "openai"])
                )
                print(f"[{datetime.now()}] 📝 Critère créé : {critere.id}")

                critere.ville_destination.add(ville)
                critere.pays_arrivee.add(pays)
                print(f"[{datetime.now()}] 📍 Ville + pays ajoutés au critère")

                client = Client()
                client.force_login(user)
                print(f"[{datetime.now()}] 🔐 Utilisateur connecté via Client test")

                try:
                    url = reverse('plan_travel', args=[critere.id])
                    print(f"[{datetime.now()}] 📡 URL générée : {url}")
                except Exception as e:
                    print(f"[{datetime.now()}] ❌ Erreur dans reverse() : {str(e)}")
                    continue

                try:
                    response = client.get(url)
                    print(f"[{datetime.now()}] 📦 Status de la réponse : {response.status_code}")
                    print(f"[{datetime.now()}] 📨 Contenu brut : {response.content.decode()}")
                except Exception as e:
                    print(f"[{datetime.now()}] ❌ Erreur lors de la requête GET : {str(e)}")
                    continue
                finally:
                    client.logout()

                if response.status_code == 200:
                    self.stdout.write(self.style.SUCCESS(f"✅ Plan généré avec succès et critère enregistré (ID {critere.id})."))
                    success_count += 1
                else:
                    self.stdout.write(self.style.ERROR(f"❌ Erreur lors de la génération du plan : {response.status_code}"))

            print(f"\n[{datetime.now()}] 🎉 Résumé : {success_count} plan(s) généré(s) avec succès sur {count} tentatives.")

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"❌ Erreur inattendue : {e}"))

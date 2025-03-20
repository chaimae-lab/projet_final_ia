
import json
from datetime import datetime
from voyage.models import CritereVoyage, JourVoyage, Activite




#sauvgarder plan dans la base de donnes 
def convertir_date(date_str):
    """ Convertir une date en format YYYY-MM-DD """
    try:
        return datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        return None

def sauvegarder_plan(critere_id, fichier_json):
    """
    Sauvegarde un plan de voyage dans la base de données.
    """
    try:
        # Charger le fichier JSON
        with open(fichier_json, "r", encoding="utf-8") as file:
            plan_data = json.load(file)

        # Vérifier que le critère de voyage existe
        critere = CritereVoyage.objects.get(id=critere_id)

        # Parcourir l'itinéraire et enregistrer les jours et activités
        for jour in plan_data["itineraire"]:
            date_jour = convertir_date(jour["date"])
            if not date_jour:
                print(f"⚠️ Date invalide pour Jour {jour['jour']}, ignoré.")
                continue

            # Enregistrer le jour de voyage
            jour_voyage, created = JourVoyage.objects.get_or_create(
                critere_voyage=critere,
                jour=jour["jour"],
                date=date_jour
            )

            # Enregistrer les activités pour ce jour
            for activite in jour["activites"]:
                if "nom" in activite:  # Vérifier si c'est une activité
                    Activite.objects.create(
                        jour_voyage=jour_voyage,
                        nom=activite["nom"],
                        heure_debut=activite["heure_debut"],
                        heure_fin=activite["heure_fin"],
                        duree=activite["duree"],
                        prix=activite.get("budget", None),  # Récupérer le prix s'il existe
                        description=activite["description"]
                    )
                    print(f"✅ Activité enregistrée : {activite['nom']} - {date_jour}")
                else:
                    print(f"⚠️ Activité ignorée car non valide : {activite}")

        return "✅ Plan de voyage enregistré avec succès !"

    except CritereVoyage.DoesNotExist:
        return f"❌ Erreur : Aucun CritereVoyage trouvé avec ID {critere_id}."

    except Exception as e:
        return f"❌ Erreur lors de l'enregistrement du plan : {str(e)}"

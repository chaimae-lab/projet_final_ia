import json
from datetime import datetime
from voyage.models import CritereVoyage, JourVoyage, Activite

def convertir_date(date_str):
    """ Convertir une date en format YYYY-MM-DD """
    try:
        return datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        return None

def sauvegarder_plan(critere_id, fichier_json):
    """
    Sauvegarde un plan de voyage dans la base de données sans doublons.
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

            # Créer ou récupérer le jour de voyage
            jour_voyage, _ = JourVoyage.objects.get_or_create(
                critere_voyage=critere,
                jour=jour["jour"],
                date=date_jour
            )

            # Enregistrer les activités si elles n'existent pas déjà
            for activite in jour["activites"]:
                if "nom" in activite:
                    existe = Activite.objects.filter(
                        jour_voyage=jour_voyage,
                        nom=activite["nom"],
                        heure_debut=activite["heure_debut"],
                        heure_fin=activite["heure_fin"]
                    ).exists()

                    if not existe:
                        Activite.objects.create(
                            jour_voyage=jour_voyage,
                            nom=activite["nom"],
                            heure_debut=activite["heure_debut"],
                            heure_fin=activite["heure_fin"],
                            duree=activite["duree"],
                            prix=activite.get("budget", None),
                            description=activite["description"]
                        )
                        print(f"✅ Activité enregistrée : {activite['nom']} - {date_jour}")
                    else:
                        print(f"⚠️ Activité déjà existante : {activite['nom']} - {date_jour}")
                else:
                    print(f"⚠️ Activité ignorée (structure invalide) : {activite}")

        return "✅ Plan de voyage enregistré avec succès !"

    except CritereVoyage.DoesNotExist:
        return f"❌ Erreur : Aucun CritereVoyage trouvé avec ID {critere_id}."

    except Exception as e:
        return f"❌ Erreur lors de l'enregistrement du plan : {str(e)}"

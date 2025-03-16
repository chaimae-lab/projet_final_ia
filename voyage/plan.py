import json
from datetime import datetime
from voyage.models import CritereVoyage, Voyage, Itineraire, Activite, Deplacement

def convertir_date(date_str):
    """ Convertir les dates au format YYYY-MM-DD """
    try:
        print(f"🔍 Conversion de la date : {date_str}")  # 🛑 Ajout Debug
        return datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        print(f"❌ Erreur : Format de date invalide -> {date_str}")  # 🛑 Ajout Debug
        return None  

def sauvegarder_plan(critere_id, plan_json):
    """
    Sauvegarde un plan de voyage en base de données en le répartissant sur plusieurs tables.
    """
    try:
        critere = CritereVoyage.objects.get(id=critere_id)
        plan_data = json.loads(plan_json)

        # ✅ Convertir la date de départ et de retour
        date_depart = convertir_date(plan_data["voyage"]["dates"].split(" - ")[0])
        date_retour = convertir_date(plan_data["voyage"]["dates"].split(" - ")[1])

        if not date_depart or not date_retour:
            return "❌ Erreur : Format de date invalide dans les dates de voyage."

        # ✅ Créer l'entrée Voyage
        voyage = Voyage.objects.create(
            critere=critere,
            destination=plan_data["voyage"]["destination"],
            type_voyage=plan_data["voyage"]["type"],
            date_depart=date_depart,
            date_retour=date_retour
        )
        print(f"✅ Voyage créé : {voyage.destination} ({date_depart} - {date_retour})")  # 🛑 Debug

        # ✅ Ajouter chaque jour dans Itinéraire
        for jour in plan_data["itineraire"]:
            print(f"🔄 Enregistrement du Jour {jour['jour']} - {jour['date']}")  # 🛑 Debug

            date_jour = convertir_date(jour["date"])
            if not date_jour:
                print(f"⚠️ Erreur format date pour {jour['jour']}")  # 🛑 Debug
                continue  # ⛔ Passer ce jour et continuer

            itineraire = Itineraire.objects.create(
                voyage=voyage,
                jour=jour["jour"],
                date=date_jour
            )

            # ✅ Ajouter les activités et les déplacements
            for activite in jour["activites"]:
                if "nom" in activite:  # Vérifier si c'est bien une activité
                    print(f"   ✅ Ajout Activité : {activite['nom']}")  # 🛑 Debug
                    Activite.objects.create(
                        itineraire=itineraire,
                        nom=activite["nom"],
                        heure_debut=activite["heure_debut"],
                        heure_fin=activite["heure_fin"],
                        duree=activite["duree"],
                        description=activite["description"]
                    )
                else:
                    print(f"   🚗 Ajout Déplacement : {activite['temps_deplacement']}")  # 🛑 Debug
                    Deplacement.objects.create(
                        itineraire=itineraire,
                        temps_deplacement=activite["temps_deplacement"]
                    )

        return f"✅ PlanVoyage enregistré avec succès pour {voyage.destination}"

    except CritereVoyage.DoesNotExist:
        return "❌ Erreur : Aucun CritereVoyage trouvé avec cet ID."

    except Exception as e:
        return f"❌ Erreur lors de l'enregistrement du plan : {str(e)}"

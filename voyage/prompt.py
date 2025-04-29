import requests
from django.conf import settings

import json
from datetime import date

# Fonction pour générer le prompt
def generer_prompt(critere):
    destinations = ', '.join([ville.nom for ville in critere.ville_destination.all()])
    pays = ', '.join({ville.pays.nom for ville in critere.ville_destination.all()})
    adresse_depart = critere.adresse_depart.rue if critere.adresse_depart else "Non spécifié"

    tranches_age = [
        {
            "tranche": t.get_tranche_age_display(),
            "nombre_voyageurs": t.nombre_voyageurs
        }
        for t in critere.tranches_age_voyageurs.all()
    ]

    prompt = {
        "user_request": "Organiser un voyage personnalisé",
        "details": {
            "destinations": destinations,
            "pays": pays,
            "adresse_depart": adresse_depart,
            "dates_voyage": f"de {critere.date_depart} à {critere.date_retour}",
            "type_voyage": critere.get_type_voyage_display(),
            "nombre_voyageurs": tranches_age if tranches_age else "Non spécifié"
        },
        "instructions": {
            "planification": "Génère un plan détaillé jour par jour.",
            "details_activites": [
                "Nom de l'activité",
                "Heure de début et heure de fin",
                "Durée de chaque activité",
                "Budget de chaque activité"  
            ],
            "contraintes": [
                f"Respecter les préférences liées au type de voyage : {critere.get_type_voyage_display()}",
                "Optimiser le temps de trajet",
                "Fournir des alternatives en cas de mauvaise météo"
            ]
        },
        
        "obligation_format": "Tu dois répondre uniquement au format JSON strict, sans aucune explication, phrase introductive ou commentaire. Le JSON doit respecter exactement la structure donnée ci-dessous.",
        "format_attendu": {
            "jour1": {
                "date": "JJ/MM/AAAA",
                "activites": [
                    {
                        "nom": "Activité 1",
                        "heure_debut": "HH:MM",
                        "heure_fin": "HH:MM",
                        "duree": "X min",
                        "description": "Détails sur l'activité",
                        "budget": "XX.XX EUR"  
                    }
                ]
            },
            "jour2": {
                "date": "JJ/MM/AAAA",
                "activites": [
                    {
                        "nom": "Activité 2",
                        "heure_debut": "HH:MM",
                        "heure_fin": "HH:MM",
                        "duree": "X min",
                        "description": "Détails sur l'activité",
                        "budget": "XX.XX EUR"  
                    }
                ]
            }
        }
    }

    return json.dumps(prompt, indent=2, ensure_ascii=False)





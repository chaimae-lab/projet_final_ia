import requests
from django.conf import settings

import json



from datetime import date

#  Fonction pour calculer l'âge à partir de la date de naissance
def calculer_age(date_naissance):
    if not date_naissance:
        return "Non spécifié"
    
    today = date.today()
    age = today.year - date_naissance.year - ((today.month, today.day) < (date_naissance.month, date_naissance.day))
    return age



#   Générer prompt 


def generer_prompt(critere):
    destinations = ', '.join([ville.nom for ville in critere.ville_destination.all()])
    pays = ', '.join({ville.pays.nom for ville in critere.ville_destination.all()})
    adresse_depart = critere.adresse_depart.rue if critere.adresse_depart else "Non spécifié"
    # ✅ Récupérer l'âge du voyageur depuis `ProfilVoyageur`
    profil_voyageur = getattr(critere.utilisateur, "profilvoyageur", None)
    age_voyageur = calculer_age(profil_voyageur.date_naissance) if profil_voyageur and profil_voyageur.date_naissance else "Non spécifié"
    
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
            "nombre_voyageurs": tranches_age if tranches_age else "Non spécifié",
            "age_voyageur": age_voyageur
            

        },
        "instructions": {
            "planification": "Génère un plan détaillé jour par jour.",
            "details_activites": [
                "Nom de l'activité",
                "Heure de début et heure de fin",
                "Durée de chaque activité",
                "Temps estimé entre chaque activité"
            ],
            "contraintes": [
                f"Respecter les préférences liées au type de voyage : {critere.get_type_voyage_display()}",
                "Optimiser le temps de trajet",
                "Fournir des alternatives en cas de mauvaise météo"
            ]
        },
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
                        "temps_deplacement": "X min"
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
                        "temps_deplacement": "X min"
                    }
                ]
            }
        }
    }

    return json.dumps(prompt, indent=2, ensure_ascii=False)




#    Envoyer le prompt à l'API DeepSeek

# ✅ Envoyer le prompt à l'API DeepSeek avec une meilleure gestion des erreurs
def envoyer_prompt_ia(prompt):
    """
    Envoie un prompt à DeepSeek et récupère la réponse sous forme JSON.
    """
    headers = {
        "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",  # Vérifie que ta clé API est bien définie
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1000
    }

    try:
        response = requests.post(settings.DEEPSEEK_API_URL, json=payload, headers=headers)
        response.raise_for_status()  # Lève une exception en cas d'erreur HTTP

        data = response.json()

        # ✅ Vérifier que DeepSeek renvoie bien un JSON valide avec une réponse correcte
        if "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0]["message"]["content"]
        else:
            print("Erreur : Réponse API mal formatée ou vide.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Erreur API DeepSeek : {e}")
        return None  # En cas d'erreur, retourne None
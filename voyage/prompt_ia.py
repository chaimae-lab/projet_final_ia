import json
import requests
from django.conf import settings

def generat_prompt(critere):
    # Vérifier si adresse_depart est définie et non None
    adresse_depart = critere.adresse_depart.rue if critere.adresse_depart and critere.adresse_depart.rue else "Adresse départ non définie"
    
    # Vérifier si adresse_arrivee est définie et non None
    adresse_arrivee = critere.adresse if critere.adresse else "Adresse arrivée non définie"
    
    # Vérifier si ville_destination est défini et non vide
    destinations = ', '.join([ville.nom for ville in critere.ville_destination.all()]) if critere.ville_destination else "Destinations non définies"
    
    # Vérifier si pays est défini
    pays = ', '.join({ville.pays.nom for ville in critere.ville_destination.all()}) if critere.ville_destination else "Pays non définis"
    
    prompt = {
        "user_request": "Organiser un voyage personnalisé",
        "details": {
            "destinations": destinations,
            "pays": pays,
            "adresse_depart": adresse_depart,
            "adresse_arrivee": adresse_arrivee,
            "dates_voyage": f"de {critere.date_depart} à {critere.date_retour}" if critere.date_depart and critere.date_retour else "Dates non définies",
            "type_voyage": critere.type_voyage if critere.type_voyage else "Type de voyage non défini",
            "nombre_voyageurs": [
                {"tranche": "Enfant", "nombre_voyageurs": critere.voyageurs_enfant if critere.voyageurs_enfant is not None else 0},
                {"tranche": "Jeune", "nombre_voyageurs": critere.voyageurs_jeune if critere.voyageurs_jeune is not None else 0},
                {"tranche": "Adulte", "nombre_voyageurs": critere.voyageurs_adulte if critere.voyageurs_adulte is not None else 0},
                {"tranche": "Senior", "nombre_voyageurs": critere.voyageurs_senior if critere.voyageurs_senior is not None else 0}
            ]
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
                f"Respecter les préférences liées au type de voyage : {critere.type_voyage}" if critere.type_voyage else "Type de voyage non spécifié",
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
    




#envoi le prompt a deppseek mock 


def obtenir_reponse_deepseek(prompt):
    """
    Gère l'appel à l'IA DeepSeek :
    - En mode développement (DEBUG=True), utilise une réponse simulée via prompt_ia().
    - Pas d'appel réel à l'API DeepSeek.
    
    Retourne la réponse sous forme de texte (str).
    """

    if settings.DEBUG:
        print("🔧 Mode développement activé : utilisation de la réponse mock.")
        return prompt_ia(prompt)  # Utilisation de la fonction mock pour tester localement
    else:
        # On ne fait pas d'appel réel à l'API
        print("🚀 Appel réel à l'API DeepSeek désactivé.")
        return None


    # de test 

def prompt_ia(prompt):
    """
    🧪 Version MOCK : Simule une réponse de DeepSeek pour les tests locaux.
    Remplace cette version par la vraie quand tu utiliseras l'API réelle.
    """
    print("📡 Simulation de l'appel à DeepSeek...")
    fake_response = {
        "jour1": {
            "date": "01/06/2025",
            "activites": [
                {
                    "nom": "Visite Tour Eiffel",
                    "heure_debut": "10:00",
                    "heure_fin": "12:00",
                    "duree": "2h",
                    "budget": "25 EUR"
                }
            ]
        },
        "jour2": {
            "date": "02/06/2025",
            "activites": [
                {
                    "nom": "Musée du Louvre",
                    "heure_debut": "11:00",
                    "heure_fin": "14:00",
                    "duree": "3h",
                    "budget": "30 EUR"
                }
            ]
        }
    }

    # On retourne la réponse sous forme de texte JSON
    # On retourne la réponse sous forme de texte JSON
    import json
    return json.dumps(fake_response, indent=2)







#  

import requests
from django.conf import settings



#   Générer prompt 

def generer_prompt(critere):
    """
    Génère un prompt détaillé et structuré pour l'IA afin de produire un plan de voyage réaliste et optimisé.
    """
    prompt = f"""
    🛫 **Plan de voyage personnalisé** 🛬

    Un utilisateur souhaite organiser un voyage selon les critères suivants :

   
    🔹 **Destination :** {critere.ville_destination.nom} ({critere.pays_arrivee.nom})
    🔹 **Adresse de départ :** {critere.adresse_depart.rue if critere.adresse_depart else "Non spécifiée"}
    
    📅 **Dates du voyage :**  
    - Date de départ : {critere.date_depart}
    - Date de retour : {critere.date_retour}
    
    💰 **Budget total :** {critere.budget_total} €  
   
  
    🎯 **Type de voyage :** {critere.type_voyage.nom if critere.type_voyage else "Non spécifié"}  

   
    **📝 Instructions pour générer le plan de voyage :**  
    🔸 Planifie chaque jour avec un itinéraire optimisé.  
    🔸 Intègre des horaires précis pour chaque activité.  
    🔸 Inclut des recommandations de restaurants et des spécialités locales à essayer.  
    🔸 Estime le coût des activités, repas et déplacements quotidiens.  
    🔸 Fournis des conseils sur les coutumes locales et les meilleures périodes pour visiter.  
    🔸 Suggère des alternatives en cas de météo défavorable.  

    **🗓️ Exemple attendu :**  
    ✦ Jour 1 : Arrivée + Exploration du centre-ville  
    ✦ Jour 2 : Visite des sites historiques + Dîner traditionnel  
    ✦ Jour 3 : Excursion en nature + Activités aquatiques  
    ✦ Jour 4 : Shopping et détente + Départ  

    💡 L'objectif est de créer un plan optimisé, équilibré entre découverte, détente et plaisir.
    """
    
    return prompt



#   envoyer_prompt_ia
def envoyer_prompt_ia(prompt):
    """
    Envoie un prompt à DeepSeek et récupère la réponse.
    """
    headers = {
        "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",  # Utilise ta clé API DeepSeek
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",  # Vérifie si DeepSeek propose d'autres modèles gratuits
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1000
    }

    response = requests.post(settings.DEEPSEEK_API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        print("Erreur API DeepSeek :", response.text)  # Affiche l'erreur pour debug
        return None  # En cas d'erreur, retourne `None`

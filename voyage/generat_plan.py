# Fichier : views.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import CritereVoyage
from .prompt_ia  import generat_prompt, envoyer_prompt_ia  
import json

def generer_plan_de_voyage(request, critere_id):
    critere = get_object_or_404(CritereVoyage, pk=critere_id)
    prompt = generat_prompt(critere)
    reponse = envoyer_prompt_ia(prompt)

    if reponse:
        try:
            plan_json = json.loads(reponse)
            critere.plan_generé = plan_json
            critere.save()
            return JsonResponse({"message": "Plan généré avec succès", "plan": plan_json})
        except json.JSONDecodeError:
            return JsonResponse({"erreur": "Le contenu reçu n’est pas un JSON valide."}, status=400)
    else:
        return JsonResponse({"erreur": "Erreur de génération via l'IA."}, status=500)

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import CritereVoyage ,PlanVoyage ,Activite ,JourVoyage
from .prompt_ia import generat_prompt, obtenir_reponse_deepseek, envoyer_prompt_ia
import json
from django.core.exceptions import ObjectDoesNotExist
from django.utils.dateparse import parse_time

from datetime import datetime





#generer plan de voyage ,stocker dans la base 

def plan_voyage(request, critere_id):
    try:
        critere = CritereVoyage.objects.get(id=critere_id)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Critère de voyage non trouvé'}, status=404)

    # Générer le prompt de voyage
    prompt = generat_prompt(critere)

    # Envoyer le prompt à l'API IA et récupérer la réponse
    plan_voyage = envoyer_prompt_ia(prompt)

    # Vérifier si la réponse a bien été générée
    if plan_voyage is None:
        return JsonResponse({'error': 'Erreur dans la génération du plan de voyage'}, status=500)

 # Sauvegarder le plan généré dans la base de données
    try:
        PlanVoyage.objects.create(
            critere_voyage=critere,  # Référence au critère de voyage
            contenu_plan=plan_voyage  # Contenu du plan généré par l'IA
        )
    except Exception as e:
        return JsonResponse({'error': f'Erreur lors de la sauvegarde du plan de voyage: {str(e)}'}, status=500)

    # Renvoi du plan de voyage en format JSON
    return JsonResponse(plan_voyage, safe=False)







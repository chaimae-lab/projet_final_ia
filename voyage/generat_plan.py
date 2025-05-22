from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import CritereVoyage ,PlanVoyage ,Activite ,JourVoyage
from .prompt_ia import generat_prompt, obtenir_reponse_deepseek, envoyer_prompt_ia, envoyer_prompt_selon_api
import json
from django.core.exceptions import ObjectDoesNotExist
from django.utils.dateparse import parse_time

from datetime import datetime





#generer plan de voyage ,stocker dans la base  api deepseek payante (fonction get)

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








#generer plan de voyage ,stocker dans la base  api deepseek et openIa payante (fonction get)
def plan_travel(request, critere_id):
    try:
        critere = CritereVoyage.objects.get(id=critere_id)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Critère de voyage non trouvé'}, status=404)

    # Générer le prompt de voyage
    prompt = generat_prompt(critere)

    # API choisie par l'utilisateur (défaut = deepseek si non précisé)
    api_choisie = critere.api_choisie if critere.api_choisie else "deepseek"

    # Envoyer le prompt à l'API choisie
    plan_contenu = envoyer_prompt_selon_api(api_choisie, prompt)

    if plan_contenu is None:
        return JsonResponse({'error': f'Erreur dans la génération du plan avec {api_choisie}'}, status=500)

    try:
        # Sauvegarder le plan généré
        PlanVoyage.objects.create(
            critere_voyage=critere,
            contenu_plan=plan_contenu
        )
    except Exception as e:
        return JsonResponse({'error': f'Erreur lors de la sauvegarde du plan de voyage: {str(e)}'}, status=500)

    return JsonResponse(plan_contenu, safe=False)




#get plan selon id 
def generer_plan_de_voyage(request, critere_id):
    critere = get_object_or_404(CritereVoyage, pk=critere_id)
    prompt = generat_prompt(critere)
    reponse = obtenir_reponse_deepseek(prompt)

    if reponse:
        try:
            # Essayer de parser la réponse en JSON
            plan_json = json.loads(reponse)

            # Vérification de la structure du plan JSON
            if "jour1" not in plan_json or "jour2" not in plan_json:
                return JsonResponse({"erreur": "La réponse JSON ne contient pas le plan de voyage attendu."}, status=400)

            critere.plan_generé = plan_json
            critere.save()
            return JsonResponse({"message": "Plan généré avec succès", "plan": plan_json})
        except json.JSONDecodeError:
            return JsonResponse({"erreur": "Le contenu reçu n’est pas un JSON valide."}, status=400)
        except Exception as e:
            return JsonResponse({"erreur": f"Erreur interne: {str(e)}"}, status=500)
    else:
        return JsonResponse({"erreur": "Erreur de génération via l'IA."}, status=500)

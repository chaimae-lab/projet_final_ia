from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import CritereVoyage
from .serializers_voyage  import CritereVoyageSerializer

from voyage.models import Voyage, Itineraire, Activite, Deplacement


#   Récupérer les critères d’un voyage via son ID.
@api_view(['GET'])
def recuperer_criteres(request, critere_id):
   
    critere = get_object_or_404(CritereVoyage, id=critere_id)
    serializer = CritereVoyageSerializer(critere)
    return Response(serializer.data)


# Récupérer plan 
@api_view(['GET'])
def recuperer_plan_voyage(request, voyage_id):
    """
    API pour récupérer un plan de voyage enregistré en base.
    """
    try:
        voyage = Voyage.objects.get(id=voyage_id)
        itineraire_data = []

        for itineraire in voyage.itineraire.all():
            activites = [
                {
                    "nom": activite.nom,
                    "heure_debut": activite.heure_debut.strftime("%H:%M"),
                    "heure_fin": activite.heure_fin.strftime("%H:%M"),
                    "duree": activite.duree,
                    "description": activite.description
                }
                for activite in itineraire.activites.all()
            ]

            deplacements = [
                {
                    "temps_deplacement": deplacement.temps_deplacement
                }
                for deplacement in itineraire.deplacements.all()
            ]

            itineraire_data.append({
                "jour": itineraire.jour,
                "date": itineraire.date.strftime("%Y-%m-%d"),
                "activites": activites + deplacements
            })

        return Response({
            "destination": voyage.destination,
            "date_depart": voyage.date_depart.strftime("%Y-%m-%d"),
            "date_retour": voyage.date_retour.strftime("%Y-%m-%d"),
            "type_voyage": voyage.type_voyage,
            "itineraire": itineraire_data
        }, status=200)

    except Voyage.DoesNotExist:
        return Response({"error": "Voyage non trouvé"}, status=404)


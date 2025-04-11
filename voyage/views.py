from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import CritereVoyage
from .serializers_voyage  import CritereVoyageSerializer

from voyage.models import  JourVoyage ,Activite 

from .models import Pays, Ville
from .serializers_voyage  import PaysSerializer, VilleSerializer



#   Récupérer un  critères  via son ID.
@api_view(['GET'])
def recuperer_criteres(request, critere_id):
   
    critere = get_object_or_404(CritereVoyage, id=critere_id)
    serializer = CritereVoyageSerializer(critere)
    return Response(serializer.data)


#  consommer api 

class PaysList(APIView):
    def get(self, request):
        pays = Pays.objects.all()
        serializer = PaysSerializer(pays, many=True)
        return Response(serializer.data)

class VilleList(APIView):
    def get(self, request, pays_nom):
        villes = Ville.objects.filter(pays__nom=pays_nom)
        serializer = VilleSerializer(villes, many=True)
        return Response(serializer.data)
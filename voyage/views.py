from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView


from .models import CritereVoyage
from .serializers_voyage  import CritereVoyageSerializer

from voyage.models import  JourVoyage ,Activite 

from .models import Pays, Ville ,Adresse

from .serializers_voyage  import PaysSerializer, VilleSerializer ,AdresseSerializer
from rest_framework import viewsets

from rest_framework import generics


from django.http import HttpResponse
#pour le lien de auth
def home(request):
    return HttpResponse("Bienvenue sur la page d'accueil !")


#   Récupérer un  critères  via son ID.
@api_view(['GET'])
def recuperer_criteres(request, critere_id):
   
    critere = get_object_or_404(CritereVoyage, id=critere_id)
    serializer = CritereVoyageSerializer(critere)
    return Response(serializer.data)





#  get api 

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
    

#get ALL adresse 
class AllAdresses(APIView):
    def get(self, request):
        adresses = Adresse.objects.all()
        serializer = AdresseSerializer(adresses, many=True)
        return Response(serializer.data)

    
#get adresse by ville 
class AdresseList(APIView):
    def get(self, request, ville_nom):
        # Récupérer toutes les adresses associées à la ville spécifiée
        adresses = Adresse.objects.filter(ville__nom=ville_nom)
        
        # Sérialiser les données des adresses
        serializer = AdresseSerializer(adresses, many=True)
        
        # Retourner la réponse avec les adresses sérialisées
        return Response(serializer.data)
    


 #post criteres

class CritereVoyageCreateView(generics.CreateAPIView):
    serializer_class = CritereVoyageSerializer

    def perform_create(self, serializer):
        serializer.save()  
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework import viewsets



from .models import CritereVoyage
from .serializers_voyage  import CritereVoyageSerializer

from voyage.models import  JourVoyage ,Activite 

from .models import Pays, Ville ,Adresse  ,Voyageur

from .serializers_voyage  import PaysSerializer, VilleSerializer ,AdresseSerializer , VoyageurSerializer
from rest_framework import viewsets

from rest_framework import generics


from django.http import HttpResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
################login facebook 
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
            #a supp 
from rest_framework.authentication import BasicAuthentication

from rest_framework.permissions import AllowAny
@method_decorator(csrf_exempt, name="dispatch")
class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter

            # asupp
    authentication_classes = []  # <-- désactive toutes les authentifications
    permission_classes = [AllowAny]  # autorise tout le monde

    def dispatch(self, request, *args, **kwargs):
        print("✅ FacebookLogin called")  # vérifie que cette vue est bien utilisée
        return super().dispatch(request, *args, **kwargs)

#pour le lien de auth
def home(request):
    return HttpResponse("Bienvenue sur la page d'accueil !")





########google auth 
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class GoogleLoginAPIView(APIView):
    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token manquant'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), "633703049993-h0qc5leo71oqdgl0opejgn1nprhg9u0l.apps.googleusercontent.com")

            email = idinfo.get('email')
            name = idinfo.get('name', '')
            if not email:
                return Response({'error': 'Email non trouvé dans le token'}, status=status.HTTP_400_BAD_REQUEST)

            user, created = User.objects.get_or_create(email=email, defaults={
                'username': email,
                'first_name': name,
            })

            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'email': user.email,
                    'username': user.username,
                }
            })
        except ValueError:
            return Response({'error': 'Token Google invalide'}, status=status.HTTP_400_BAD_REQUEST)




#supprimer les donnes pour app dev


def delete_data_view(request):
    return render(request, 'delete_data.html')

#pour supprimer les donnes 
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    user = request.user
    user.delete()
    return Response({"message": "Votre compte a été supprimé avec succès."}, status=200)



#gesion voyageur 

from rest_framework import viewsets

class VoyageurViewSet(viewsets.ModelViewSet):
    queryset = Voyageur.objects.all()
    serializer_class = VoyageurSerializer
    

# affichage de voyageur selon user connecte 
from rest_framework import generics, permissions

class VoyageurListAPIView(generics.ListAPIView):
    serializer_class = VoyageurSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Voyageur.objects.filter(utilisateur=user)





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
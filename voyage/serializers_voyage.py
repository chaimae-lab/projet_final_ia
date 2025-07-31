from rest_framework import serializers
from .models import CritereVoyage
from .models import Pays, Ville , Adresse,Voyageur
from django.contrib.auth.models import User






# Serializer pour le modèle User (lié via OneToOneField)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']  #les champs q'ont veux afficher




class VoyageurSerializer(serializers.ModelSerializer):
    utilisateur = UserSerializer(read_only=True)  # lecture (affichage)
    utilisateur_id = serializers.PrimaryKeyRelatedField(  # écriture
        queryset=User.objects.all(),
        source='utilisateur',
        write_only=True
    )

    class Meta:
        model = Voyageur
        fields = ['id', 'utilisateur', 'utilisateur_id', 'telephone', 'date_naissance']



class CritereVoyageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CritereVoyage
        fields = '__all__'



class VilleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ville
        fields = ['id', 'nom']

class PaysSerializer(serializers.ModelSerializer):
    villes = VilleSerializer(many=True, read_only=True)

    class Meta:
        model = Pays
        fields = ['id', 'nom', 'villes']


class AdresseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adresse
        fields = ['id', 'rue', 'code_postal', 'ville']
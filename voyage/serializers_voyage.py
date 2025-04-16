from rest_framework import serializers
from .models import CritereVoyage
from .models import Pays, Ville , Adresse

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
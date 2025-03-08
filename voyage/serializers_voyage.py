from rest_framework import serializers
from .models import CritereVoyage

class CritereVoyageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CritereVoyage
        fields = '__all__'
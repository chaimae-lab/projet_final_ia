

from django.contrib import admin
from .models import Pays, Ville, Adresse, ProfilVoyageur,  CritereVoyage, TrancheAgeVoyageur ,PlanVoyage

# Enregistrer les modèles de base
admin.site.register(Pays)
admin.site.register(Ville)
admin.site.register(Adresse)
admin.site.register(TrancheAgeVoyageur) 

# Enregistrer ProfilVoyageur avec une configuration avancée
@admin.register(ProfilVoyageur)
class ProfilVoyageurAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'telephone', 'date_naissance')
    search_fields = ('utilisateur__username', 'telephone')

# Enregistrer CritereVoyage avec plus d'informations affichées
@admin.register(CritereVoyage)
class CritereVoyageAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'date_depart', 'date_retour', 'budget_total', 'date_creation')
    search_fields = ('utilisateur__username', 'ville_depart__nom', 'ville_destination__nom')
    list_filter = ('date_depart', 'date_retour', 'type_voyage')

# Enregistrer PlanVoyage pour voir le contenu JSON
@admin.register(PlanVoyage)
class PlanVoyageAdmin(admin.ModelAdmin):
    list_display = ('critere_voyage', 'date_creation')
    search_fields = ('critere_voyage__utilisateur__username',)


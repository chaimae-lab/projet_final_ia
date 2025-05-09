from django.urls import path
from .views import recuperer_criteres
from .views import PaysList, VilleList ,AdresseList

from .views import  AllAdresses 
from .views import CritereVoyageCreateView
from .generat_plan import generer_plan_de_voyage
from .generat_plan import plan_voyage



urlpatterns = [
    path('criteres/<int:critere_id>/', recuperer_criteres, name='recuperer_criteres'),
    path('pays/', PaysList.as_view()),
    path('villes/<str:pays_nom>/', VilleList.as_view()),
    path('adresses/<str:ville_nom>/', AdresseList.as_view(), name='adresse-list'),
    path('adresses/', AllAdresses.as_view(), name='adresse-list-all'),
    path('criteres/', CritereVoyageCreateView.as_view(), name='create-critere'),
    path('generer-plan/<int:critere_id>/', generer_plan_de_voyage, name='generer_plan'),
    path('plan_voyage/<int:critere_id>/', plan_voyage, name='plan_voyage'),


    


    

]

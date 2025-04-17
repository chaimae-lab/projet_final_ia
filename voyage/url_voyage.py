from django.urls import path
from .views import recuperer_criteres
from .views import PaysList, VilleList ,AdresseList

from .views import  AllAdresses 

urlpatterns = [
    path('criteres/<int:critere_id>/', recuperer_criteres, name='recuperer_criteres'),
    path('pays/', PaysList.as_view()),
    path('villes/<str:pays_nom>/', VilleList.as_view()),
    path('adresses/<str:ville_nom>/', AdresseList.as_view(), name='adresse-list'),
    path('adresses/', AllAdresses.as_view(), name='adresse-list-all')

]

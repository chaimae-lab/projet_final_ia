from django.urls import path
from .views import recuperer_criteres
from .views import PaysList, VilleList

urlpatterns = [
    path('criteres/<int:critere_id>/', recuperer_criteres, name='recuperer_criteres'),
    path('pays/', PaysList.as_view()),
    path('villes/<str:pays_nom>/', VilleList.as_view()),
]

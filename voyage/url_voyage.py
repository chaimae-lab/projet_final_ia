from django.urls import path
from .views import recuperer_criteres

urlpatterns = [
    path('criteres/<int:critere_id>/', recuperer_criteres, name='recuperer_criteres'),
]

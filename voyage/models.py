from django.db import models
from django.contrib.auth.models import User


class Pays(models.Model):
    nom = models.CharField(max_length=100)



class Ville(models.Model):
    nom = models.CharField(max_length=100)
    pays = models.ForeignKey(Pays, on_delete=models.CASCADE) # Chaque ville est associée à un seul pays.


class Adresse(models.Model):
    rue = models.CharField(max_length=200)
    code_postal = models.CharField(max_length=20, null=True, blank=True)
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE)


    
    
class ProfilVoyageur(models.Model):
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    date_naissance = models.DateField(blank=True, null=True)
    pays_favoris = models.ManyToManyField(Pays, blank=True)   # ManyToMany ,Chaque profil voyageur peut avoir plusieurs pays favoris(nouveau table generer automatique ).


class Transport(models.Model):
    type_transport = models.CharField(max_length=50)
    compagnie = models.CharField(max_length=100, blank=True, null=True)
    confort = models.CharField(max_length=50, blank=True, null=True)


class Hebergement(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=200, null=True, blank=True)
    type_hebergement = models.CharField(max_length=50, blank=True, null=True)
    etoiles = models.PositiveIntegerField(null=True, blank=True)


class Activite(models.Model):
    nom = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)


class TypeVoyage(models.Model):
    nom = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)



class CritereVoyage(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    pays_depart = models.ForeignKey(Pays, related_name='pays_depart_voyages', on_delete=models.CASCADE)
    pays_arrivee = models.ForeignKey(Pays, related_name='pays_arrivee_voyages', on_delete=models.CASCADE)
    ville_depart = models.ForeignKey(Ville, related_name='depart_voyages', on_delete=models.CASCADE)
    ville_destination = models.ForeignKey(Ville, related_name='destination_voyages', on_delete=models.CASCADE)
    adresse_depart = models.ForeignKey(Adresse, related_name='adresse_depart_voyages', on_delete=models.SET_NULL, null=True, blank=True)
    adresse_arrivee = models.ForeignKey(Adresse, related_name='adresse_arrivee_voyages', on_delete=models.SET_NULL, null=True, blank=True)
    date_depart = models.DateField()
    date_retour = models.DateField()
    budget_total = models.DecimalField(max_digits=10, decimal_places=2)
    nombre_voyageurs = models.PositiveIntegerField()
    type_voyage = models.ForeignKey(TypeVoyage, null=True, on_delete=models.SET_NULL)
    moyen_transport_prefere = models.ForeignKey(Transport, null=True, on_delete=models.SET_NULL)
    hebergement_prefere = models.ForeignKey(Hebergement, null=True, on_delete=models.SET_NULL)
    activites_souhaitees = models.ManyToManyField(Activite)  # ManyToMany  nouveau table
    date_creation = models.DateTimeField(auto_now_add=True)



class PlanVoyage(models.Model):
    critere_voyage = models.ForeignKey(CritereVoyage, on_delete=models.CASCADE)
    contenu_plan = models.JSONField()  # Stocke le plan sous format JSON
    date_creation = models.DateTimeField(auto_now_add=True)

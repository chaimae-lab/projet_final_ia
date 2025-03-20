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


   # Modèle Voyageur (ancien ProfilVoyageur)
    
class Voyageur(models.Model): # Pas de conflit avec User de Django   on peux pas le rennomer user 
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    date_naissance = models.DateField(blank=True, null=True)
    










class CritereVoyage(models.Model):
    class TypeVoyage(models.TextChoices):
        LOISIR = 'loisir', 'Loisir'
        AFFAIRES = 'affaires', 'Affaires'
        FAMILIAL = 'familial', 'Familial'
        CULTUREL = 'culturel', 'Culturel'
        AVENTURE = 'aventure', 'Aventure'
        ROMANTIQUE = 'romantique', 'Romantique'
        RELIGIEUX = 'religieux', 'Religieux'
        

    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    pays_arrivee = models.ManyToManyField(Pays, related_name='pays_arrivee_voyages')
    ville_destination = models.ManyToManyField(Ville, related_name='destination_voyages') 
    adresse_depart = models.ForeignKey(Adresse, related_name='adresse_depart_voyages', on_delete=models.SET_NULL, null=True, blank=True)  
    date_depart = models.DateField()
    date_retour = models.DateField()
    budget_total = models.DecimalField(max_digits=10, decimal_places=2)
    type_voyage = models.CharField(max_length=20,choices=TypeVoyage.choices)# liste 
    date_creation = models.DateTimeField(auto_now_add=True)
    #tranche d'age appel 
    @property   
    def tranches_age(self):
        return self.tranches_age_voyageurs.all()





#   model tranche d'age 

class TrancheAgeVoyageur(models.Model):
         #enum
    class NomTranche(models.TextChoices):
        ENFANT = 'enfant', 'Enfant (0-12 ans)'
        JEUNE = 'jeune', 'Jeune (13-25 ans)'
        ADULTE = 'adulte', 'Adulte (26-60 ans)'
        SENIOR = 'senior', 'Senior (+60 ans)'


    critere_voyage = models.ForeignKey(CritereVoyage,related_name='tranches_age_voyageurs',on_delete=models.CASCADE ) # un CritereVoyage peut être lié à plusieurs objets de ce modèle
    tranche_age = models.CharField( max_length=20, choices=NomTranche.choices )
    nombre_voyageurs = models.PositiveIntegerField(default=1)

    

class PlanVoyage(models.Model):
    critere_voyage = models.ForeignKey(CritereVoyage, on_delete=models.CASCADE)
    contenu_plan = models.JSONField()  # Stocke le plan sous format JSON
    date_creation = models.DateTimeField(auto_now_add=True)



#  les tables pour deviser le plan 




 
class JourVoyage(models.Model):
    critere_voyage = models.ForeignKey(CritereVoyage, on_delete=models.CASCADE, related_name="jour")
    jour = models.IntegerField()
    date = models.DateField()

class Activite(models.Model):
    jour_voyage = models.ForeignKey(JourVoyage, on_delete=models.CASCADE, related_name="activites", null=True, blank=True)
    nom = models.CharField(max_length=255)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    duree = models.CharField(max_length=50)
    prix = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  
    description = models.TextField()


    
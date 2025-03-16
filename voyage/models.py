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
        ETUDES = 'etudes', 'Études'
        AUTRE = 'autre', 'Autre'

    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    pays_arrivee = models.ManyToManyField(Pays, related_name='pays_arrivee_voyages') #liste  ,9atlk plusier pas f7ala pys visite (ANBDL LA RELATION)
    ville_destination = models.ManyToManyField(Ville, related_name='destination_voyages') #liste   plusieur pas visite  (ANBDL LA RELATION )
    adresse_depart = models.ForeignKey(Adresse, related_name='adresse_depart_voyages', on_delete=models.SET_NULL, null=True, blank=True)  
    date_depart = models.DateField()
    date_retour = models.DateField()
    budget_total = models.DecimalField(max_digits=10, decimal_places=2)
    type_voyage = models.CharField(max_length=20,choices=TypeVoyage.choices,default=TypeVoyage.AUTRE )# liste 
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


    critere_voyage = models.ForeignKey(CritereVoyage,related_name='tranches_age_voyageurs',on_delete=models.CASCADE ) # Chaque voyage (CritereVoyage) peut avoir plusieurs lignes différentes (une par tranche d’âge)
    tranche_age = models.CharField( max_length=20, choices=NomTranche.choices )
    nombre_voyageurs = models.PositiveIntegerField(default=1)

    

class PlanVoyage(models.Model):
    critere_voyage = models.ForeignKey(CritereVoyage, on_delete=models.CASCADE)
    contenu_plan = models.JSONField()  # Stocke le plan sous format JSON
    date_creation = models.DateTimeField(auto_now_add=True)



#  les tables pour deviser le plan 


#  Modèle Voyage (lié à CritereVoyage)
class Voyage(models.Model):
    critere = models.ForeignKey("CritereVoyage", on_delete=models.CASCADE, related_name="voyages")
    destination = models.CharField(max_length=255)
    type_voyage = models.CharField(max_length=50)
    date_depart = models.DateField()
    date_retour = models.DateField()


#  Modèle Itinéraire (lié à Voyage)
class Itineraire(models.Model):
    voyage = models.ForeignKey(Voyage, on_delete=models.CASCADE, related_name="itineraire")
    jour = models.IntegerField()
    date = models.DateField()


# Modèle Activité (lié à Itinéraire)
class Activite(models.Model):
    itineraire = models.ForeignKey(Itineraire, on_delete=models.CASCADE, related_name="activites")
    nom = models.CharField(max_length=255)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    duree = models.CharField(max_length=50)
    description = models.TextField()


#  Modèle Déplacement (lié à Itinéraire)
class Deplacement(models.Model):
    itineraire = models.ForeignKey(Itineraire, on_delete=models.CASCADE, related_name="deplacements")
    temps_deplacement = models.CharField(max_length=50)

    
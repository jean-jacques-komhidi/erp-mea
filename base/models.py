from django.db import models
from django.contrib.auth.models import User

class Entreprise(models.Model):
    """Modèle pour l'entreprise"""
    nom = models.CharField(max_length=200, verbose_name="Nom de l'entreprise")
    adresse = models.TextField(verbose_name="Adresse")
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")
    email = models.EmailField(verbose_name="Email")
    numero_fiscal = models.CharField(max_length=50, verbose_name="Numéro fiscal (NINEA)")
    logo = models.ImageField(upload_to='entreprise/', null=True, blank=True, verbose_name="Logo")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    
    class Meta:
        verbose_name = "Entreprise"
        verbose_name_plural = "Entreprises"
    
    def __str__(self):
        return self.nom

class Client(models.Model):
    """Modèle pour les clients"""
    code = models.CharField(max_length=20, unique=True, verbose_name="Code client")
    nom = models.CharField(max_length=200, verbose_name="Nom du client")
    email = models.EmailField(verbose_name="Email")
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")
    adresse = models.TextField(verbose_name="Adresse")
    ville = models.CharField(max_length=100, verbose_name="Ville")
    pays = models.CharField(max_length=100, verbose_name="Pays")
    numero_fiscal = models.CharField(max_length=50, blank=True, verbose_name="Numéro fiscal")
    limite_credit = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Limite de crédit")
    est_actif = models.BooleanField(default=True, verbose_name="Est actif")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    
    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
    
    def __str__(self):
        return f"{self.code} - {self.nom}"

class Fournisseur(models.Model):
    """Modèle pour les fournisseurs"""
    code = models.CharField(max_length=20, unique=True, verbose_name="Code fournisseur")
    nom = models.CharField(max_length=200, verbose_name="Nom du fournisseur")
    email = models.EmailField(verbose_name="Email")
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")
    adresse = models.TextField(verbose_name="Adresse")
    ville = models.CharField(max_length=100, verbose_name="Ville")
    pays = models.CharField(max_length=100, verbose_name="Pays")
    numero_fiscal = models.CharField(max_length=50, blank=True, verbose_name="Numéro fiscal")
    delai_paiement = models.IntegerField(default=30, verbose_name="Délai de paiement (jours)")
    est_actif = models.BooleanField(default=True, verbose_name="Est actif")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    
    class Meta:
        verbose_name = "Fournisseur"
        verbose_name_plural = "Fournisseurs"
    
    def __str__(self):
        return f"{self.code} - {self.nom}"

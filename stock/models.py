from django.db import models
from django.contrib.auth.models import  User
from base.models import Client, Fournisseur

class Categorie(models.Model):
    """Modèle pour les catégories de produits"""
    nom = models.CharField(max_length=100, verbose_name="Nom de la catégorie")
    description = models.TextField(blank=True, verbose_name="Description")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Catégorie parente")
    
    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
    
    def __str__(self):
        return self.nom

class Produit(models.Model):
    """Modèle pour les produits"""
    code = models.CharField(max_length=50, unique=True, verbose_name="Code produit")
    nom = models.CharField(max_length=200, verbose_name="Nom du produit")
    description = models.TextField(blank=True, verbose_name="Description")
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, verbose_name="Catégorie")
    unite = models.CharField(max_length=20, default='PCE', verbose_name="Unité de mesure")
    prix_achat = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Prix d'achat")
    prix_vente = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Prix de vente")
    taux_tva = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Taux de TVA (%)")
    stock_min = models.IntegerField(default=0, verbose_name="Stock minimum")
    stock_max = models.IntegerField(default=0, verbose_name="Stock maximum")
    seuil_reapprovisionnement = models.IntegerField(default=0, verbose_name="Seuil de réapprovisionnement")
    est_actif = models.BooleanField(default=True, verbose_name="Est actif")
    image = models.ImageField(upload_to='produits/', null=True, blank=True, verbose_name="Image")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    
    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
    
    def __str__(self):
        return f"{self.code} - {self.nom}"
    
    @property
    def stock_actuel(self):
        """Calcule le stock actuel du produit"""
        total = self.mouvementstock_set.aggregate(
            total=models.Sum('quantite')
        )['total']
        return total or 0

class Entrepot(models.Model):
    """Modèle pour les entrepôts"""
    code = models.CharField(max_length=20, unique=True, verbose_name="Code entrepôt")
    nom = models.CharField(max_length=100, verbose_name="Nom de l'entrepôt")
    adresse = models.TextField(verbose_name="Adresse")
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Responsable")
    est_actif = models.BooleanField(default=True, verbose_name="Est actif")
    
    class Meta:
        verbose_name = "Entrepôt"
        verbose_name_plural = "Entrepôts"
    
    def __str__(self):
        return f"{self.code} - {self.nom}"

class MouvementStock(models.Model):
    """Modèle pour les mouvements de stock"""
    TYPES_MOUVEMENT = [
        ('ENTREE', 'Entrée'),
        ('SORTIE', 'Sortie'),
        ('AJUSTEMENT', 'Ajustement'),
        ('TRANSFERT', 'Transfert'),
    ]
    
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, verbose_name="Produit")
    entrepot = models.ForeignKey(Entrepot, on_delete=models.CASCADE, verbose_name="Entrepôt")
    type_mouvement = models.CharField(max_length=20, choices=TYPES_MOUVEMENT, verbose_name="Type de mouvement")
    quantite = models.IntegerField(verbose_name="Quantité")
    reference = models.CharField(max_length=50, verbose_name="Référence")
    notes = models.TextField(blank=True, verbose_name="Notes")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date")
    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Utilisateur")
    
    class Meta:
        verbose_name = "Mouvement de stock"
        verbose_name_plural = "Mouvements de stock"
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.type_mouvement} - {self.produit.code} - {self.quantite}"
    
class Stock(models.Model):
    """Modèle pour gérer le stock par entrepôt"""
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, verbose_name="Produit")
    entrepot = models.ForeignKey(Entrepot, on_delete=models.CASCADE, verbose_name="Entrepôt")
    quantite = models.IntegerField(default=0, verbose_name="Quantité en stock")
    date_derniere_maj = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")
    
    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"
        unique_together = ['produit', 'entrepot']
    
    def __str__(self):
        return f"{self.produit.code} - {self.entrepot.code}: {self.quantite}"
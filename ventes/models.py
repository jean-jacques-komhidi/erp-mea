from django.db import models
from django.contrib.auth.models import User
from base.models import Client
from stock.models import Produit, Entrepot

class CommandeVente(models.Model):
    """Modèle pour les commandes de vente"""
    STATUTS = [
        ('BROUILLON', 'Brouillon'),
        ('CONFIRME', 'Confirmé'),
        ('EXPEDIE', 'Expédié'),
        ('FACTURE', 'Facturé'),
        ('ANNULE', 'Annulé'),
    ]
    
    numero_commande = models.CharField(max_length=50, unique=True, verbose_name="Numéro de commande")
    client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name="Client")
    date_commande = models.DateField(auto_now_add=True, verbose_name="Date de commande")
    date_livraison = models.DateField(verbose_name="Date de livraison prévue")
    statut = models.CharField(max_length=20, choices=STATUTS, default='BROUILLON', verbose_name="Statut")
    entrepot = models.ForeignKey(Entrepot, on_delete=models.PROTECT, verbose_name="Entrepôt")
    sous_total = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Sous-total")
    montant_tva = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Montant TVA")
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Total")
    notes = models.TextField(blank=True, verbose_name="Notes")
    cree_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Créé par")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    
    class Meta:
        verbose_name = "Commande de vente"
        verbose_name_plural = "Commandes de vente"
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"{self.numero_commande} - {self.client.nom}"
    
    def calculer_totaux(self):
        """Calcule les totaux de la commande"""
        lignes = self.lignecommandevente_set.all()
        self.sous_total = sum(ligne.sous_total for ligne in lignes)
        self.montant_tva = sum(ligne.montant_tva for ligne in lignes)
        self.total = self.sous_total + self.montant_tva
        self.save()

class LigneCommandeVente(models.Model):
    """Modèle pour les lignes de commande de vente"""
    commande = models.ForeignKey(CommandeVente, on_delete=models.CASCADE, verbose_name="Commande")
    produit = models.ForeignKey(Produit, on_delete=models.PROTECT, verbose_name="Produit")
    quantite = models.IntegerField(verbose_name="Quantité")
    prix_unitaire = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Prix unitaire")
    remise = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Remise (%)")
    taux_tva = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Taux TVA (%)")
    
    class Meta:
        verbose_name = "Ligne de commande de vente"
        verbose_name_plural = "Lignes de commande de vente"
    
    @property
    def sous_total(self):
        """Calcule le sous-total de la ligne"""
        montant = self.quantite * self.prix_unitaire
        montant_apres_remise = montant * (1 - self.remise / 100)
        return montant_apres_remise
    
    @property
    def montant_tva(self):
        """Calcule le montant de TVA de la ligne"""
        return self.sous_total * self.taux_tva / 100
    
    @property
    def total(self):
        """Calcule le total de la ligne"""
        return self.sous_total + self.montant_tva

class Facture(models.Model):
    """Modèle pour les factures"""
    STATUTS = [
        ('BROUILLON', 'Brouillon'),
        ('ENVOYEE', 'Envoyée'),
        ('PAYEE', 'Payée'),
        ('EN_RETARD', 'En retard'),
        ('ANNULEE', 'Annulée'),
    ]
    
    numero_facture = models.CharField(max_length=50, unique=True, verbose_name="Numéro de facture")
    commande_vente = models.ForeignKey(CommandeVente, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Commande de vente")
    client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name="Client")
    date_facture = models.DateField(auto_now_add=True, verbose_name="Date de facture")
    date_echeance = models.DateField(verbose_name="Date d'échéance")
    statut = models.CharField(max_length=20, choices=STATUTS, default='BROUILLON', verbose_name="Statut")
    sous_total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Sous-total")
    montant_tva = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Montant TVA")
    total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Total")
    montant_paye = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Montant payé")
    notes = models.TextField(blank=True, verbose_name="Notes")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    
    class Meta:
        verbose_name = "Facture"
        verbose_name_plural = "Factures"
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"{self.numero_facture} - {self.client.nom}"
    
    @property
    def solde(self):
        """Calcule le solde restant de la facture"""
        return self.total - self.montant_paye
    
class LigneFacture(models.Model):
    """Modèle pour les lignes de facture"""
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, related_name='lignes', verbose_name="Facture")
    produit = models.ForeignKey(Produit, on_delete=models.PROTECT, verbose_name="Produit")
    quantite = models.IntegerField(verbose_name="Quantité")
    prix_unitaire = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Prix unitaire")
    remise = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Remise (%)")
    taux_tva = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Taux TVA (%)")
    
    class Meta:
        verbose_name = "Ligne de facture"
        verbose_name_plural = "Lignes de facture"
    
    def __str__(self):
        return f"{self.facture.numero_facture} - {self.produit.nom}"
    
    @property
    def sous_total(self):
        """Calcule le sous-total de la ligne"""
        montant = self.quantite * self.prix_unitaire
        montant_apres_remise = montant * (1 - self.remise / 100)
        return montant_apres_remise
    
    @property
    def montant_tva(self):
        """Calcule le montant de TVA de la ligne"""
        return self.sous_total * self.taux_tva / 100
    
    @property
    def total(self):
        """Calcule le total de la ligne"""
        return self.sous_total + self.montant_tva

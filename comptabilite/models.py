# ============================================
# comptabilite/models.py - Modèles de comptabilité
# ============================================

from django.db import models
from django.contrib.auth.models import User
from base.models import Client, Fournisseur
from decimal import Decimal

class PlanComptable(models.Model):
    """Plan comptable - Liste des comptes"""
    TYPES_COMPTE = [
        ('ACTIF', 'Actif'),
        ('PASSIF', 'Passif'),
        ('CHARGE', 'Charge'),
        ('PRODUIT', 'Produit'),
    ]
    
    numero_compte = models.CharField(max_length=20, unique=True, verbose_name="Numéro de compte")
    libelle = models.CharField(max_length=200, verbose_name="Libellé")
    type_compte = models.CharField(max_length=20, choices=TYPES_COMPTE, verbose_name="Type de compte")
    compte_parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Compte parent")
    est_actif = models.BooleanField(default=True, verbose_name="Est actif")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    
    class Meta:
        verbose_name = "Plan comptable"
        verbose_name_plural = "Plan comptable"
        ordering = ['numero_compte']
    
    def __str__(self):
        return f"{self.numero_compte} - {self.libelle}"
    
    @property
    def solde(self):
        """Calcule le solde du compte"""
        debits = self.ecritures_debit.aggregate(total=models.Sum('montant'))['total'] or Decimal('0')
        credits = self.ecritures_credit.aggregate(total=models.Sum('montant'))['total'] or Decimal('0')
        
        if self.type_compte in ['ACTIF', 'CHARGE']:
            return debits - credits
        else:  # PASSIF, PRODUIT
            return credits - debits


class Exercice(models.Model):
    """Exercice comptable"""
    nom = models.CharField(max_length=100, verbose_name="Nom de l'exercice")
    date_debut = models.DateField(verbose_name="Date de début")
    date_fin = models.DateField(verbose_name="Date de fin")
    est_cloture = models.BooleanField(default=False, verbose_name="Est clôturé")
    date_cloture = models.DateField(null=True, blank=True, verbose_name="Date de clôture")
    
    class Meta:
        verbose_name = "Exercice comptable"
        verbose_name_plural = "Exercices comptables"
        ordering = ['-date_debut']
    
    def __str__(self):
        return self.nom


class Journal(models.Model):
    """Journal comptable"""
    TYPES_JOURNAL = [
        ('VENTE', 'Ventes'),
        ('ACHAT', 'Achats'),
        ('BANQUE', 'Banque'),
        ('CAISSE', 'Caisse'),
        ('OD', 'Opérations diverses'),
    ]
    
    code = models.CharField(max_length=10, unique=True, verbose_name="Code du journal")
    libelle = models.CharField(max_length=100, verbose_name="Libellé")
    type_journal = models.CharField(max_length=20, choices=TYPES_JOURNAL, verbose_name="Type de journal")
    est_actif = models.BooleanField(default=True, verbose_name="Est actif")
    
    class Meta:
        verbose_name = "Journal"
        verbose_name_plural = "Journaux"
    
    def __str__(self):
        return f"{self.code} - {self.libelle}"


class Piece(models.Model):
    """Pièce comptable (regroupement d'écritures)"""
    numero_piece = models.CharField(max_length=50, unique=True, verbose_name="Numéro de pièce")
    journal = models.ForeignKey(Journal, on_delete=models.PROTECT, verbose_name="Journal")
    exercice = models.ForeignKey(Exercice, on_delete=models.PROTECT, verbose_name="Exercice")
    date_piece = models.DateField(verbose_name="Date de la pièce")
    libelle = models.CharField(max_length=200, verbose_name="Libellé")
    reference = models.CharField(max_length=100, blank=True, verbose_name="Référence")
    est_validee = models.BooleanField(default=False, verbose_name="Est validée")
    date_validation = models.DateTimeField(null=True, blank=True, verbose_name="Date de validation")
    validee_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='pieces_validees', verbose_name="Validée par")
    cree_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='pieces_creees', verbose_name="Créée par")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    
    class Meta:
        verbose_name = "Pièce comptable"
        verbose_name_plural = "Pièces comptables"
        ordering = ['-date_piece']
    
    def __str__(self):
        return f"{self.numero_piece} - {self.libelle}"
    
    @property
    def total_debit(self):
        """Total des débits de la pièce"""
        return self.ecritures.aggregate(total=models.Sum('debit'))['total'] or Decimal('0')
    
    @property
    def total_credit(self):
        """Total des crédits de la pièce"""
        return self.ecritures.aggregate(total=models.Sum('credit'))['total'] or Decimal('0')
    
    @property
    def est_equilibree(self):
        """Vérifie si la pièce est équilibrée (Débit = Crédit)"""
        return self.total_debit == self.total_credit
    
    def valider(self, utilisateur):
        """Valider la pièce comptable"""
        from django.utils import timezone
        if self.est_equilibree:
            self.est_validee = True
            self.date_validation = timezone.now()
            self.validee_par = utilisateur
            self.save()
            return True
        return False


class Ecriture(models.Model):
    """Écriture comptable"""
    piece = models.ForeignKey(Piece, on_delete=models.CASCADE, related_name='ecritures', verbose_name="Pièce")
    compte = models.ForeignKey(PlanComptable, on_delete=models.PROTECT, verbose_name="Compte")
    libelle = models.CharField(max_length=200, verbose_name="Libellé")
    debit = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Débit")
    credit = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Crédit")
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Client")
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Fournisseur")
    
    class Meta:
        verbose_name = "Écriture comptable"
        verbose_name_plural = "Écritures comptables"
    
    def __str__(self):
        return f"{self.compte.numero_compte} - {self.libelle}"
    
    @property
    def montant(self):
        """Retourne le montant (débit ou crédit)"""
        return self.debit if self.debit > 0 else self.credit


class Banque(models.Model):
    """Compte bancaire"""
    nom = models.CharField(max_length=100, verbose_name="Nom de la banque")
    numero_compte = models.CharField(max_length=50, verbose_name="Numéro de compte")
    iban = models.CharField(max_length=34, blank=True, verbose_name="IBAN")
    swift = models.CharField(max_length=11, blank=True, verbose_name="Code SWIFT/BIC")
    devise = models.CharField(max_length=3, default='XOF', verbose_name="Devise")
    solde_initial = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Solde initial")
    compte_comptable = models.ForeignKey(PlanComptable, on_delete=models.PROTECT, verbose_name="Compte comptable associé")
    est_actif = models.BooleanField(default=True, verbose_name="Est actif")
    
    class Meta:
        verbose_name = "Banque"
        verbose_name_plural = "Banques"
    
    def __str__(self):
        return f"{self.nom} - {self.numero_compte}"
    
    @property
    def solde_actuel(self):
        """Calcule le solde actuel du compte bancaire"""
        mouvements_debit = MouvementBancaire.objects.filter(
            banque=self,
            type_mouvement='DEBIT'
        ).aggregate(total=models.Sum('montant'))['total'] or Decimal('0')
        
        mouvements_credit = MouvementBancaire.objects.filter(
            banque=self,
            type_mouvement='CREDIT'
        ).aggregate(total=models.Sum('montant'))['total'] or Decimal('0')
        
        return self.solde_initial + mouvements_credit - mouvements_debit


class MouvementBancaire(models.Model):
    """Mouvement bancaire"""
    TYPES_MOUVEMENT = [
        ('CREDIT', 'Crédit (Entrée)'),
        ('DEBIT', 'Débit (Sortie)'),
    ]
    
    banque = models.ForeignKey(Banque, on_delete=models.CASCADE, verbose_name="Banque")
    date_mouvement = models.DateField(verbose_name="Date du mouvement")
    type_mouvement = models.CharField(max_length=10, choices=TYPES_MOUVEMENT, verbose_name="Type de mouvement")
    montant = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Montant")
    libelle = models.CharField(max_length=200, verbose_name="Libellé")
    reference = models.CharField(max_length=100, blank=True, verbose_name="Référence")
    piece = models.ForeignKey(Piece, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Pièce comptable")
    est_rapproche = models.BooleanField(default=False, verbose_name="Est rapproché")
    date_rapprochement = models.DateField(null=True, blank=True, verbose_name="Date de rapprochement")
    cree_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Créé par")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    
    class Meta:
        verbose_name = "Mouvement bancaire"
        verbose_name_plural = "Mouvements bancaires"
        ordering = ['-date_mouvement']
    
    def __str__(self):
        return f"{self.banque.nom} - {self.libelle} - {self.montant}"


class Budget(models.Model):
    """Budget prévisionnel"""
    exercice = models.ForeignKey(Exercice, on_delete=models.CASCADE, verbose_name="Exercice")
    compte = models.ForeignKey(PlanComptable, on_delete=models.CASCADE, verbose_name="Compte")
    montant_prevu = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Montant prévu")
    mois = models.IntegerField(verbose_name="Mois (1-12)")
    notes = models.TextField(blank=True, verbose_name="Notes")
    
    class Meta:
        verbose_name = "Budget"
        verbose_name_plural = "Budgets"
        unique_together = ['exercice', 'compte', 'mois']
    
    def __str__(self):
        return f"{self.exercice.nom} - {self.compte.numero_compte} - Mois {self.mois}"
    
    @property
    def montant_realise(self):
        """Calcule le montant réalisé pour ce budget"""
        from datetime import date
        debut_mois = date(self.exercice.date_debut.year, self.mois, 1)
        
        if self.mois == 12:
            fin_mois = date(self.exercice.date_debut.year, 12, 31)
        else:
            fin_mois = date(self.exercice.date_debut.year, self.mois + 1, 1)
        
        ecritures = Ecriture.objects.filter(
            compte=self.compte,
            piece__date_piece__gte=debut_mois,
            piece__date_piece__lt=fin_mois,
            piece__est_validee=True
        )
        
        if self.compte.type_compte in ['CHARGE', 'ACTIF']:
            realise = ecritures.aggregate(total=models.Sum('debit'))['total'] or Decimal('0')
        else:
            realise = ecritures.aggregate(total=models.Sum('credit'))['total'] or Decimal('0')
        
        return realise
    
    @property
    def ecart(self):
        """Calcule l'écart entre prévu et réalisé"""
        return self.montant_prevu - self.montant_realise
    
    @property
    def taux_realisation(self):
        """Calcule le taux de réalisation en %"""
        if self.montant_prevu == 0:
            return 0
        return (self.montant_realise / self.montant_prevu) * 100
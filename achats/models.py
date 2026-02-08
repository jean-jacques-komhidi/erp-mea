# achats/models.py - Modèles du module achats (AMÉLIORÉ)

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import Decimal
from base.models import Fournisseur
from stock.models import Produit, Entrepot


class CommandeAchat(models.Model):
    """Modèle pour les commandes d'achat"""
    
    STATUTS = [
        ('BROUILLON', 'Brouillon'),
        ('CONFIRMEE', 'Confirmée'),
        ('ENVOYEE', 'Envoyée'),
        ('RECUE', 'Reçue'),
        ('FACTUREE', 'Facturée'),
        ('ANNULEE', 'Annulée'),
    ]
    
    # Informations principales
    numero_commande = models.CharField(
        max_length=50, 
        unique=True, 
        blank=True,
        verbose_name="Numéro de commande"
    )
    
    fournisseur = models.ForeignKey(
        Fournisseur,
        on_delete=models.PROTECT,
        related_name='commandes_achat',
        verbose_name="Fournisseur"
    )
    
    entrepot = models.ForeignKey(
        Entrepot,
        on_delete=models.PROTECT,
        related_name='commandes_achat',
        verbose_name="Entrepôt de destination"
    )
    
    statut = models.CharField(
        max_length=20,
        choices=STATUTS,
        default='BROUILLON',
        verbose_name="Statut"
    )
    
    # Dates
    date_commande = models.DateField(
        auto_now_add=True,
        verbose_name="Date de commande"
    )
    
    date_livraison_prevue = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date de livraison prévue"
    )
    
    date_reception = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date de réception"
    )
    
    # Montants
    sous_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Sous-total HT"
    )
    
    montant_tva = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Montant TVA"
    )
    
    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Total TTC"
    )
    
    # Informations complémentaires
    notes = models.TextField(
        blank=True,
        verbose_name="Notes"
    )
    
    raison_annulation = models.TextField(
        blank=True,
        verbose_name="Raison de l'annulation"
    )
    
    # Lien avec la comptabilité
    piece_comptable = models.ForeignKey(
        'comptabilite.Piece',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='commandes_achat',
        verbose_name="Pièce comptable"
    )
    
    # Traçabilité
    cree_par = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='commandes_achat_creees',
        verbose_name="Créé par"
    )
    
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    
    date_modification = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de modification"
    )
    
    class Meta:
        verbose_name = "Commande d'achat"
        verbose_name_plural = "Commandes d'achat"
        ordering = ['-date_creation']
        indexes = [
            models.Index(fields=['numero_commande']),
            models.Index(fields=['statut']),
            models.Index(fields=['date_commande']),
            models.Index(fields=['fournisseur']),
        ]
        permissions = [
            ("can_validate_commande_achat", "Peut valider les commandes d'achat"),
            ("can_cancel_commande_achat", "Peut annuler les commandes d'achat"),
        ]
    
    def __str__(self):
        return f"{self.numero_commande} - {self.fournisseur.nom}"
    
    def save(self, *args, **kwargs):
        """Génère automatiquement le numéro de commande si nécessaire"""
        if not self.numero_commande:
            self.numero_commande = self._generer_numero_commande()
        super().save(*args, **kwargs)
    
    def _generer_numero_commande(self):
        """Génère un numéro de commande unique"""
        date = timezone.now().date()
        prefixe = "CMD"
        annee_mois = date.strftime('%y%m')
        
        # Trouver la dernière commande du mois
        dernier_numero = CommandeAchat.objects.filter(
            numero_commande__startswith=f"{prefixe}{annee_mois}"
        ).order_by('-numero_commande').first()
        
        if dernier_numero:
            try:
                dernier_seq = int(dernier_numero.numero_commande[-4:])
                nouveau_seq = dernier_seq + 1
            except (ValueError, IndexError):
                nouveau_seq = 1
        else:
            nouveau_seq = 1
        
        return f"{prefixe}{annee_mois}{nouveau_seq:04d}"
    
    def calculer_totaux(self):
        """Calcule les totaux de la commande"""
        lignes = self.lignecommandeachat_set.all()
        self.sous_total = sum(ligne.sous_total for ligne in lignes)
        self.montant_tva = sum(ligne.montant_tva for ligne in lignes)
        self.total = self.sous_total + self.montant_tva
        self.save(update_fields=['sous_total', 'montant_tva', 'total'])
    
    def peut_etre_confirmee(self):
        """Vérifie si la commande peut être confirmée"""
        return (
            self.statut == 'BROUILLON' and 
            self.lignecommandeachat_set.exists() and
            self.total > 0
        )
    
    def peut_etre_envoyee(self):
        """Vérifie si la commande peut être envoyée au fournisseur"""
        return self.statut == 'CONFIRMEE'
    
    def peut_etre_recue(self):
        """Vérifie si la commande peut être reçue"""
        return self.statut in ['CONFIRMEE', 'ENVOYEE']
    
    def peut_etre_annulee(self):
        """Vérifie si la commande peut être annulée"""
        return self.statut in ['BROUILLON', 'CONFIRMEE', 'ENVOYEE']
    
    def peut_etre_modifiee(self):
        """Vérifie si la commande peut être modifiée"""
        return self.statut in ['BROUILLON', 'CONFIRMEE']
    
    def est_completement_recue(self):
        """Vérifie si toutes les lignes ont été complètement reçues"""
        lignes = self.lignecommandeachat_set.all()
        if not lignes.exists():
            return False
        return all(ligne.est_completement_recue() for ligne in lignes)
    
    def taux_reception(self):
        """Calcule le taux de réception en pourcentage"""
        lignes = self.lignecommandeachat_set.all()
        if not lignes.exists():
            return 0
        
        total_commande = sum(ligne.quantite for ligne in lignes)
        total_recu = sum(ligne.quantite_recue for ligne in lignes)
        
        if total_commande == 0:
            return 0
        
        return (total_recu / total_commande) * 100
    
    def generer_ecriture_comptable(self, journal, exercice):
        """
        Génère l'écriture comptable lors de la réception
        Débit: Compte Achat (60X) et TVA déductible (4456)
        Crédit: Compte Fournisseur (401X)
        """
        if self.piece_comptable:
            # Écriture déjà générée
            return self.piece_comptable
        
        # Import ici pour éviter les imports circulaires
        from comptabilite.models import Piece, Ecriture, PlanComptable
        
        # Récupérer les comptes comptables
        try:
            compte_achat = PlanComptable.objects.get(numero_compte__startswith='60')
            compte_tva = PlanComptable.objects.get(numero_compte__startswith='4456')
            compte_fournisseur = PlanComptable.objects.get(numero_compte__startswith='401')
        except PlanComptable.DoesNotExist:
            raise ValueError("Les comptes comptables nécessaires n'existent pas dans le plan comptable")
        
        # Créer la pièce comptable
        piece = Piece.objects.create(
            journal=journal,
            exercice=exercice,
            date_piece=self.date_reception or timezone.now().date(),
            libelle=f"Achat - {self.numero_commande} - {self.fournisseur.nom}",
            reference=self.numero_commande,
            cree_par=self.cree_par
        )
        
        # Écriture 1 : Débit compte Achat
        Ecriture.objects.create(
            piece=piece,
            compte=compte_achat,
            libelle=f"Achat {self.numero_commande}",
            debit=self.sous_total,
            credit=Decimal('0.00'),
            fournisseur=self.fournisseur
        )
        
        # Écriture 2 : Débit TVA déductible (si TVA > 0)
        if self.montant_tva > 0:
            Ecriture.objects.create(
                piece=piece,
                compte=compte_tva,
                libelle=f"TVA déductible {self.numero_commande}",
                debit=self.montant_tva,
                credit=Decimal('0.00'),
                fournisseur=self.fournisseur
            )
        
        # Écriture 3 : Crédit compte Fournisseur
        Ecriture.objects.create(
            piece=piece,
            compte=compte_fournisseur,
            libelle=f"Fournisseur {self.fournisseur.nom} - {self.numero_commande}",
            debit=Decimal('0.00'),
            credit=self.total,
            fournisseur=self.fournisseur
        )
        
        # Lier la pièce à la commande
        self.piece_comptable = piece
        self.save(update_fields=['piece_comptable'])
        
        return piece


class LigneCommandeAchat(models.Model):
    """Modèle pour les lignes de commande d'achat"""
    
    commande = models.ForeignKey(
        CommandeAchat,
        on_delete=models.CASCADE,
        verbose_name="Commande"
    )
    
    produit = models.ForeignKey(
        Produit,
        on_delete=models.PROTECT,
        verbose_name="Produit"
    )
    
    quantite = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Quantité commandée"
    )
    
    quantite_recue = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Quantité reçue"
    )
    
    prix_unitaire = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Prix unitaire HT"
    )
    
    taux_tva = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Taux TVA (%)"
    )
    
    notes = models.TextField(
        blank=True,
        verbose_name="Notes"
    )
    
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    
    class Meta:
        verbose_name = "Ligne de commande d'achat"
        verbose_name_plural = "Lignes de commande d'achat"
        ordering = ['id']
        unique_together = ['commande', 'produit']
    
    def __str__(self):
        return f"{self.commande.numero_commande} - {self.produit.nom}"
    
    @property
    def sous_total(self):
        """Calcule le sous-total HT de la ligne"""
        return Decimal(self.quantite) * self.prix_unitaire
    
    @property
    def montant_tva(self):
        """Calcule le montant de TVA de la ligne"""
        return self.sous_total * (self.taux_tva / Decimal('100.00'))
    
    @property
    def total(self):
        """Calcule le total TTC de la ligne"""
        return self.sous_total + self.montant_tva
    
    def quantite_restante(self):
        """Retourne la quantité restant à recevoir"""
        return self.quantite - self.quantite_recue
    
    def est_completement_recue(self):
        """Vérifie si la ligne est complètement reçue"""
        return self.quantite_recue >= self.quantite
    
    def taux_reception(self):
        """Calcule le taux de réception en pourcentage"""
        if self.quantite == 0:
            return 0
        return (self.quantite_recue / self.quantite) * 100
    
    def save(self, *args, **kwargs):
        """Recalcule les totaux de la commande après sauvegarde"""
        super().save(*args, **kwargs)
        # Recalculer les totaux de la commande parent
        self.commande.calculer_totaux()
    
    def delete(self, *args, **kwargs):
        """Recalcule les totaux de la commande après suppression"""
        commande = self.commande
        super().delete(*args, **kwargs)
        commande.calculer_totaux()


class PaiementFournisseur(models.Model):
    """Modèle pour les paiements aux fournisseurs"""
    
    MODES_PAIEMENT = [
        ('ESPECES', 'Espèces'),
        ('CHEQUE', 'Chèque'),
        ('VIREMENT', 'Virement bancaire'),
        ('CARTE', 'Carte bancaire'),
        ('MOBILE', 'Paiement mobile'),
    ]
    
    numero_paiement = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        verbose_name="Numéro de paiement"
    )
    
    commande = models.ForeignKey(
        CommandeAchat,
        on_delete=models.PROTECT,
        related_name='paiements',
        verbose_name="Commande d'achat"
    )
    
    fournisseur = models.ForeignKey(
        Fournisseur,
        on_delete=models.PROTECT,
        related_name='paiements_recus',
        verbose_name="Fournisseur"
    )
    
    montant = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Montant payé"
    )
    
    date_paiement = models.DateField(
        verbose_name="Date de paiement"
    )
    
    mode_paiement = models.CharField(
        max_length=20,
        choices=MODES_PAIEMENT,
        default='VIREMENT',
        verbose_name="Mode de paiement"
    )
    
    reference = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Référence (n° chèque, virement, etc.)"
    )
    
    notes = models.TextField(
        blank=True,
        verbose_name="Notes"
    )
    
    # Lien avec la comptabilité
    piece_comptable = models.ForeignKey(
        'comptabilite.Piece',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='paiements_fournisseur',
        verbose_name="Pièce comptable"
    )
    
    # Traçabilité
    utilisateur = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Enregistré par"
    )
    
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    
    class Meta:
        verbose_name = "Paiement fournisseur"
        verbose_name_plural = "Paiements fournisseurs"
        ordering = ['-date_paiement']
    
    def __str__(self):
        return f"{self.numero_paiement} - {self.fournisseur.nom} - {self.montant} FCFA"
    
    def save(self, *args, **kwargs):
        """Génère automatiquement le numéro de paiement"""
        if not self.numero_paiement:
            self.numero_paiement = self._generer_numero_paiement()
        super().save(*args, **kwargs)
    
    def _generer_numero_paiement(self):
        """Génère un numéro de paiement unique"""
        date = timezone.now().date()
        prefixe = "PAY"
        annee_mois = date.strftime('%y%m')
        
        dernier = PaiementFournisseur.objects.filter(
            numero_paiement__startswith=f"{prefixe}{annee_mois}"
        ).order_by('-numero_paiement').first()
        
        if dernier:
            try:
                dernier_seq = int(dernier.numero_paiement[-4:])
                nouveau_seq = dernier_seq + 1
            except (ValueError, IndexError):
                nouveau_seq = 1
        else:
            nouveau_seq = 1
        
        return f"{prefixe}{annee_mois}{nouveau_seq:04d}"
    
    def generer_ecriture_comptable(self, journal, exercice, banque):
        """
        Génère l'écriture comptable du paiement
        Débit: Compte Fournisseur (401X)
        Crédit: Compte Banque (512X)
        """
        if self.piece_comptable:
            return self.piece_comptable
        
        from comptabilite.models import Piece, Ecriture, PlanComptable
        
        try:
            compte_fournisseur = PlanComptable.objects.get(numero_compte__startswith='401')
            compte_banque = banque.compte_comptable
        except PlanComptable.DoesNotExist:
            raise ValueError("Les comptes comptables nécessaires n'existent pas")
        
        # Créer la pièce
        piece = Piece.objects.create(
            journal=journal,
            exercice=exercice,
            date_piece=self.date_paiement,
            libelle=f"Paiement fournisseur {self.fournisseur.nom} - {self.numero_paiement}",
            reference=self.numero_paiement,
            cree_par=self.utilisateur
        )
        
        # Débit Fournisseur
        Ecriture.objects.create(
            piece=piece,
            compte=compte_fournisseur,
            libelle=f"Paiement {self.fournisseur.nom}",
            debit=self.montant,
            credit=Decimal('0.00'),
            fournisseur=self.fournisseur
        )
        
        # Crédit Banque
        Ecriture.objects.create(
            piece=piece,
            compte=compte_banque,
            libelle=f"Paiement {self.fournisseur.nom} - {self.mode_paiement}",
            debit=Decimal('0.00'),
            credit=self.montant,
            fournisseur=self.fournisseur
        )
        
        self.piece_comptable = piece
        self.save(update_fields=['piece_comptable'])
        
        return piece
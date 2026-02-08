# achats/forms.py - Formulaires du module achats

from django import forms
from django.forms import inlineformset_factory
from django.utils import timezone
from decimal import Decimal
from .models import CommandeAchat, LigneCommandeAchat, PaiementFournisseur
from stock.models import Produit, Entrepot
from base.models import Fournisseur


class CommandeAchatForm(forms.ModelForm):
    """Formulaire pour créer/modifier une commande d'achat"""
    
    class Meta:
        model = CommandeAchat
        fields = [
            'fournisseur',
            'entrepot',
            'date_livraison_prevue',
            'notes',
        ]
        widgets = {
            'fournisseur': forms.Select(attrs={
                'class': 'form-select select2',
                'required': True,
                'data-placeholder': 'Sélectionnez un fournisseur'
            }),
            'entrepot': forms.Select(attrs={
                'class': 'form-select select2',
                'required': True,
                'data-placeholder': 'Sélectionnez un entrepôt'
            }),
            'date_livraison_prevue': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'min': timezone.now().date().isoformat()
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Notes additionnelles (optionnel)...'
            }),
        }
        labels = {
            'fournisseur': 'Fournisseur *',
            'entrepot': 'Entrepôt de destination *',
            'date_livraison_prevue': 'Date de livraison prévue',
            'notes': 'Notes',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filtrer uniquement les fournisseurs actifs
        self.fields['fournisseur'].queryset = Fournisseur.objects.filter(
            est_actif=True
        ).order_by('nom')
        
        # Filtrer uniquement les entrepôts actifs
        self.fields['entrepot'].queryset = Entrepot.objects.filter(
            est_actif=True
        ).order_by('nom')
        
        # Valider que le queryset n'est pas vide
        if not self.fields['fournisseur'].queryset.exists():
            self.fields['fournisseur'].widget.attrs['disabled'] = True
            self.fields['fournisseur'].help_text = 'Aucun fournisseur actif disponible'
        
        if not self.fields['entrepot'].queryset.exists():
            self.fields['entrepot'].widget.attrs['disabled'] = True
            self.fields['entrepot'].help_text = 'Aucun entrepôt actif disponible'
    
    def clean_date_livraison_prevue(self):
        """Valide que la date de livraison n'est pas dans le passé"""
        date_livraison = self.cleaned_data.get('date_livraison_prevue')
        
        if date_livraison and date_livraison < timezone.now().date():
            raise forms.ValidationError(
                "La date de livraison prévue ne peut pas être dans le passé."
            )
        
        return date_livraison


class LigneCommandeAchatForm(forms.ModelForm):
    """Formulaire pour une ligne de commande d'achat"""
    
    produit = forms.ModelChoiceField(
        queryset=Produit.objects.filter(est_actif=True).order_by('nom'),
        widget=forms.Select(attrs={
            'class': 'form-select select2 produit-select',
            'data-placeholder': 'Sélectionnez un produit',
            'required': True,
        }),
        label='Produit *'
    )
    
    class Meta:
        model = LigneCommandeAchat
        fields = ['produit', 'quantite', 'prix_unitaire', 'taux_tva', 'notes']
        widgets = {
            'quantite': forms.NumberInput(attrs={
                'class': 'form-control quantite',
                'min': 1,
                'step': 1,
                'required': True,
                'placeholder': '0'
            }),
            'prix_unitaire': forms.NumberInput(attrs={
                'class': 'form-control prix-unitaire',
                'min': 0,
                'step': 0.01,
                'required': True,
                'placeholder': '0.00'
            }),
            'taux_tva': forms.NumberInput(attrs={
                'class': 'form-control taux-tva',
                'min': 0,
                'max': 100,
                'step': 0.01,
                'placeholder': '18.00'
            }),
            'notes': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Notes (optionnel)...'
            }),
        }
        labels = {
            'produit': 'Produit *',
            'quantite': 'Quantité *',
            'prix_unitaire': 'Prix unitaire HT *',
            'taux_tva': 'Taux TVA (%)',
            'notes': 'Notes',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Si nouvelle ligne, initialiser avec les valeurs du produit
        if not self.instance.pk and 'initial' in kwargs:
            initial = kwargs.get('initial', {})
            if 'produit' in initial:
                try:
                    produit = Produit.objects.get(pk=initial['produit'])
                    self.fields['prix_unitaire'].initial = produit.prix_achat or Decimal('0.00')
                    self.fields['taux_tva'].initial = produit.taux_tva or Decimal('0.00')
                except Produit.DoesNotExist:
                    pass
    
    def clean_quantite(self):
        """Valide que la quantité est positive"""
        quantite = self.cleaned_data.get('quantite')
        
        if quantite is not None and quantite < 1:
            raise forms.ValidationError("La quantité doit être au moins 1.")
        
        return quantite
    
    def clean_prix_unitaire(self):
        """Valide que le prix unitaire est positif"""
        prix = self.cleaned_data.get('prix_unitaire')
        
        if prix is not None and prix < 0:
            raise forms.ValidationError("Le prix unitaire ne peut pas être négatif.")
        
        return prix
    
    def clean_taux_tva(self):
        """Valide que le taux de TVA est entre 0 et 100"""
        taux = self.cleaned_data.get('taux_tva')
        
        if taux is not None:
            if taux < 0 or taux > 100:
                raise forms.ValidationError("Le taux de TVA doit être entre 0 et 100%.")
        
        return taux


# Formset pour gérer plusieurs lignes de commande
LigneCommandeAchatFormSet = inlineformset_factory(
    CommandeAchat,
    LigneCommandeAchat,
    form=LigneCommandeAchatForm,
    extra=1,  # Nombre de formulaires vides à afficher
    can_delete=True,
    min_num=1,  # Minimum une ligne requise
    validate_min=True,
    max_num=50,  # Maximum 50 lignes par commande
)


class RecevoirCommandeForm(forms.Form):
    """Formulaire pour la réception d'une commande (quantités à recevoir)"""
    
    def __init__(self, *args, **kwargs):
        commande = kwargs.pop('commande', None)
        super().__init__(*args, **kwargs)
        
        if commande:
            for ligne in commande.lignecommandeachat_set.select_related('produit').all():
                quantite_restante = ligne.quantite_restante()
                
                if quantite_restante > 0:
                    field_name = f'quantite_{ligne.pk}'
                    self.fields[field_name] = forms.IntegerField(
                        label=f'{ligne.produit.nom} ({ligne.produit.code})',
                        min_value=0,
                        max_value=quantite_restante,
                        initial=quantite_restante,
                        required=False,
                        widget=forms.NumberInput(attrs={
                            'class': 'form-control quantite-recue',
                            'data-ligne-id': ligne.pk,
                            'data-max': quantite_restante,
                            'data-produit': ligne.produit.nom,
                            'min': 0,
                            'max': quantite_restante,
                        }),
                        help_text=f'Commandé: {ligne.quantite} | Déjà reçu: {ligne.quantite_recue} | Reste: {quantite_restante}'
                    )


class AnnulerCommandeForm(forms.Form):
    """Formulaire pour annuler une commande avec raison"""
    
    raison = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Veuillez indiquer la raison de l\'annulation de cette commande...',
            'required': True,
        }),
        label="Raison de l'annulation *",
        help_text="Cette information sera enregistrée dans l'historique de la commande."
    )
    
    def clean_raison(self):
        """Valide que la raison n'est pas vide"""
        raison = self.cleaned_data.get('raison', '').strip()
        
        if not raison:
            raise forms.ValidationError("La raison de l'annulation est obligatoire.")
        
        if len(raison) < 10:
            raise forms.ValidationError("La raison doit contenir au moins 10 caractères.")
        
        return raison


class PaiementFournisseurForm(forms.ModelForm):
    """Formulaire pour enregistrer un paiement fournisseur"""
    
    class Meta:
        model = PaiementFournisseur
        fields = [
            'montant',
            'date_paiement',
            'mode_paiement',
            'reference',
            'notes',
        ]
        widgets = {
            'montant': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0.01,
                'step': 0.01,
                'required': True,
                'placeholder': '0.00'
            }),
            'date_paiement': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'required': True,
                'max': timezone.now().date().isoformat()
            }),
            'mode_paiement': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
            }),
            'reference': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'N° chèque, virement, etc. (optionnel)'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Notes additionnelles (optionnel)...'
            }),
        }
        labels = {
            'montant': 'Montant payé *',
            'date_paiement': 'Date de paiement *',
            'mode_paiement': 'Mode de paiement *',
            'reference': 'Référence',
            'notes': 'Notes',
        }
    
    def __init__(self, *args, **kwargs):
        self.commande = kwargs.pop('commande', None)
        super().__init__(*args, **kwargs)
        
        # Définir la date par défaut à aujourd'hui
        if not self.instance.pk:
            self.fields['date_paiement'].initial = timezone.now().date()
        
        # Ajouter le solde restant dans le help_text si une commande est fournie
        if self.commande:
            total_paye = self.commande.paiements.aggregate(
                total=forms.models.Sum('montant')
            )['total'] or Decimal('0.00')
            solde = self.commande.total - total_paye
            
            self.fields['montant'].help_text = f'Solde restant à payer : {solde:,.2f} FCFA'
            self.fields['montant'].widget.attrs['max'] = float(solde)
    
    def clean_montant(self):
        """Valide que le montant est positif et ne dépasse pas le solde"""
        montant = self.cleaned_data.get('montant')
        
        if montant is not None:
            if montant <= 0:
                raise forms.ValidationError("Le montant doit être supérieur à 0.")
            
            # Vérifier que le montant ne dépasse pas le solde si une commande est fournie
            if self.commande:
                total_paye = self.commande.paiements.aggregate(
                    total=forms.models.Sum('montant')
                )['total'] or Decimal('0.00')
                solde = self.commande.total - total_paye
                
                if montant > solde:
                    raise forms.ValidationError(
                        f"Le montant ne peut pas dépasser le solde restant ({solde:,.2f} FCFA)."
                    )
        
        return montant
    
    def clean_date_paiement(self):
        """Valide que la date de paiement n'est pas dans le futur"""
        date_paiement = self.cleaned_data.get('date_paiement')
        
        if date_paiement and date_paiement > timezone.now().date():
            raise forms.ValidationError(
                "La date de paiement ne peut pas être dans le futur."
            )
        
        return date_paiement


class FiltreCommandeAchatForm(forms.Form):
    """Formulaire pour filtrer les commandes d'achat"""
    
    STATUTS_CHOICES = [('', 'Tous les statuts')] + list(CommandeAchat.STATUTS)
    
    statut = forms.ChoiceField(
        choices=STATUTS_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        label='Statut'
    )
    
    recherche = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rechercher par numéro, fournisseur...',
        }),
        label='Recherche'
    )
    
    date_debut = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
        }),
        label='Date début'
    )
    
    date_fin = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
        }),
        label='Date fin'
    )
    
    fournisseur = forms.ModelChoiceField(
        queryset=Fournisseur.objects.filter(est_actif=True).order_by('nom'),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select select2',
            'data-placeholder': 'Tous les fournisseurs',
        }),
        label='Fournisseur',
        empty_label='Tous les fournisseurs'
    )
    
    def clean(self):
        """Valide que la période de dates est cohérente"""
        cleaned_data = super().clean()
        date_debut = cleaned_data.get('date_debut')
        date_fin = cleaned_data.get('date_fin')
        
        if date_debut and date_fin:
            if date_fin < date_debut:
                raise forms.ValidationError(
                    "La date de fin doit être postérieure ou égale à la date de début."
                )
        
        return cleaned_data


class ImporterCommandeForm(forms.Form):
    """Formulaire pour importer des commandes depuis un fichier (CSV, Excel)"""
    
    TYPE_FICHIER_CHOICES = [
        ('csv', 'CSV'),
        ('excel', 'Excel (XLSX)'),
    ]
    
    fichier = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.csv,.xlsx,.xls',
        }),
        label='Fichier à importer *',
        help_text='Formats acceptés : CSV, Excel (XLSX, XLS)'
    )
    
    type_fichier = forms.ChoiceField(
        choices=TYPE_FICHIER_CHOICES,
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        label='Type de fichier *',
        initial='excel'
    )
    
    fournisseur = forms.ModelChoiceField(
        queryset=Fournisseur.objects.filter(est_actif=True).order_by('nom'),
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select select2',
        }),
        label='Fournisseur *',
        help_text='Toutes les lignes importées seront associées à ce fournisseur'
    )
    
    entrepot = forms.ModelChoiceField(
        queryset=Entrepot.objects.filter(est_actif=True).order_by('nom'),
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-select select2',
        }),
        label='Entrepôt *',
        help_text='Entrepôt de destination pour tous les produits'
    )
    
    def clean_fichier(self):
        """Valide le fichier uploadé"""
        fichier = self.cleaned_data.get('fichier')
        
        if fichier:
            # Vérifier la taille (max 5MB)
            if fichier.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Le fichier ne doit pas dépasser 5 MB.")
            
            # Vérifier l'extension
            nom_fichier = fichier.name.lower()
            extensions_valides = ['.csv', '.xlsx', '.xls']
            
            if not any(nom_fichier.endswith(ext) for ext in extensions_valides):
                raise forms.ValidationError(
                    "Format de fichier non supporté. Utilisez CSV ou Excel."
                )
        
        return fichier
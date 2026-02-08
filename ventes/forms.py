from django import forms
from .models import CommandeVente, LigneCommandeVente, Facture
from django.forms import inlineformset_factory

class FormulaireCommandeVente(forms.ModelForm):
    """Formulaire pour créer/modifier une commande de vente"""
    class Meta:
        model = CommandeVente
        fields = ['client', 'date_livraison', 'entrepot', 'statut', 'notes']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-control'}),
            'date_livraison': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'entrepot': forms.Select(attrs={'class': 'form-control'}),
            'statut': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class FormulaireLigneCommandeVente(forms.ModelForm):
    """Formulaire pour les lignes de commande de vente"""
    class Meta:
        model = LigneCommandeVente
        fields = ['produit', 'quantite', 'prix_unitaire', 'remise', 'taux_tva']
        widgets = {
            'produit': forms.Select(attrs={'class': 'form-control'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control'}),
            'prix_unitaire': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'remise': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '0'}),
            'taux_tva': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '18'}),
        }

# Formset pour gérer plusieurs lignes de commande
FormulaireEnsembleLignesVente = inlineformset_factory(
    CommandeVente, 
    LigneCommandeVente,
    form=FormulaireLigneCommandeVente,
    extra=1,
    can_delete=True
)

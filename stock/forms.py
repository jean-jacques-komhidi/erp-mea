# stock/forms.py - Formulaires corrigés

from django import forms
from .models import Produit, Categorie, Entrepot, MouvementStock

class FormulaireProduit(forms.ModelForm):
    """Formulaire pour créer/modifier un produit"""
    class Meta:
        model = Produit
        fields = ['code', 'nom', 'description', 'categorie', 'unite', 
                  'prix_achat', 'prix_vente', 'taux_tva', 
                  'stock_min', 'stock_max', 'seuil_reapprovisionnement', 'est_actif', 'image']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PROD001'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'categorie': forms.Select(attrs={'class': 'form-control'}),
            'unite': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PCE'}),
            'prix_achat': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'prix_vente': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'taux_tva': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '18'}),
            'stock_min': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock_max': forms.NumberInput(attrs={'class': 'form-control'}),
            'seuil_reapprovisionnement': forms.NumberInput(attrs={'class': 'form-control'}),
            'est_actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class FormulaireCategorie(forms.ModelForm):
    """Formulaire pour créer/modifier une catégorie"""
    class Meta:
        model = Categorie
        fields = ['nom', 'description', 'parent']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'parent': forms.Select(attrs={'class': 'form-control'}),
        }

class FormulaireEntrepot(forms.ModelForm):
    """Formulaire pour créer/modifier un entrepôt"""
    class Meta:
        model = Entrepot
        fields = ['code', 'nom', 'adresse', 'responsable', 'est_actif']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ENT001'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'responsable': forms.Select(attrs={'class': 'form-control'}),
            'est_actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class FormulaireMouvementStock(forms.ModelForm):
    """Formulaire pour enregistrer un mouvement de stock"""
    class Meta:
        model = MouvementStock
        fields = ['produit', 'entrepot', 'type_mouvement', 'quantite', 'reference', 'notes']
        widgets = {
            'produit': forms.Select(attrs={'class': 'form-control'}),
            'entrepot': forms.Select(attrs={'class': 'form-control'}),
            'type_mouvement': forms.Select(attrs={'class': 'form-control'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control'}),
            'reference': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
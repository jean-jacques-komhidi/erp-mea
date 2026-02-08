from django import forms
from .models import Client, Fournisseur, Entreprise

class FormulaireClient(forms.ModelForm):
    """Formulaire pour créer/modifier un client"""
    class Meta:
        model = Client
        fields = ['code', 'nom', 'email', 'telephone', 'adresse', 'ville', 
                  'pays', 'numero_fiscal', 'limite_credit', 'est_actif']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CLI001'}),
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du client'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@exemple.com'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+221 XX XXX XX XX'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ville': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dakar'}),
            'pays': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sénégal'}),
            'numero_fiscal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'NINEA'}),
            'limite_credit': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'est_actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class FormulaireFournisseur(forms.ModelForm):
    """Formulaire pour créer/modifier un fournisseur"""
    class Meta:
        model = Fournisseur
        fields = ['code', 'nom', 'email', 'telephone', 'adresse', 'ville', 
                  'pays', 'numero_fiscal', 'delai_paiement', 'est_actif']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'FOUR001'}),
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du fournisseur'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ville': forms.TextInput(attrs={'class': 'form-control'}),
            'pays': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_fiscal': forms.TextInput(attrs={'class': 'form-control'}),
            'delai_paiement': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '30'}),
            'est_actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

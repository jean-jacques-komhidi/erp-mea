# ============================================
# comptabilite/forms.py - Formulaires de comptabilité
# ============================================

from django import forms
from .models import (
    PlanComptable, Exercice, Journal, Piece, Ecriture,
    Banque, MouvementBancaire, Budget
)

class FormulairePlanComptable(forms.ModelForm):
    """Formulaire pour le plan comptable"""
    class Meta:
        model = PlanComptable
        fields = ['numero_compte', 'libelle', 'type_compte', 'compte_parent', 'est_actif']
        widgets = {
            'numero_compte': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '411000'}),
            'libelle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Clients'}),
            'type_compte': forms.Select(attrs={'class': 'form-control'}),
            'compte_parent': forms.Select(attrs={'class': 'form-control'}),
            'est_actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class FormulaireExercice(forms.ModelForm):
    """Formulaire pour les exercices comptables"""
    class Meta:
        model = Exercice
        fields = ['nom', 'date_debut', 'date_fin']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Exercice 2024'}),
            'date_debut': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class FormulaireJournal(forms.ModelForm):
    """Formulaire pour les journaux"""
    class Meta:
        model = Journal
        fields = ['code', 'libelle', 'type_journal', 'est_actif']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'VE'}),
            'libelle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Journal des ventes'}),
            'type_journal': forms.Select(attrs={'class': 'form-control'}),
            'est_actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class FormulairePiece(forms.ModelForm):
    """Formulaire pour les pièces comptables"""
    class Meta:
        model = Piece
        fields = ['journal', 'exercice', 'date_piece', 'libelle', 'reference']
        widgets = {
            'journal': forms.Select(attrs={'class': 'form-control'}),
            'exercice': forms.Select(attrs={'class': 'form-control'}),
            'date_piece': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'libelle': forms.TextInput(attrs={'class': 'form-control'}),
            'reference': forms.TextInput(attrs={'class': 'form-control'}),
        }


class FormulaireEcriture(forms.ModelForm):
    """Formulaire pour les écritures comptables"""
    class Meta:
        model = Ecriture
        fields = ['compte', 'libelle', 'debit', 'credit', 'client', 'fournisseur']
        widgets = {
            'compte': forms.Select(attrs={'class': 'form-control'}),
            'libelle': forms.TextInput(attrs={'class': 'form-control'}),
            'debit': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '0'}),
            'credit': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '0'}),
            'client': forms.Select(attrs={'class': 'form-control'}),
            'fournisseur': forms.Select(attrs={'class': 'form-control'}),
        }


class FormulaireBanque(forms.ModelForm):
    """Formulaire pour les comptes bancaires"""
    class Meta:
        model = Banque
        fields = ['nom', 'numero_compte', 'iban', 'swift', 'devise', 'solde_initial', 'compte_comptable', 'est_actif']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CBAO'}),
            'numero_compte': forms.TextInput(attrs={'class': 'form-control'}),
            'iban': forms.TextInput(attrs={'class': 'form-control'}),
            'swift': forms.TextInput(attrs={'class': 'form-control'}),
            'devise': forms.TextInput(attrs={'class': 'form-control', 'value': 'XOF'}),
            'solde_initial': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'compte_comptable': forms.Select(attrs={'class': 'form-control'}),
            'est_actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class FormulaireMouvementBancaire(forms.ModelForm):
    """Formulaire pour les mouvements bancaires"""
    class Meta:
        model = MouvementBancaire
        fields = ['banque', 'date_mouvement', 'type_mouvement', 'montant', 'libelle', 'reference']
        widgets = {
            'banque': forms.Select(attrs={'class': 'form-control'}),
            'date_mouvement': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'type_mouvement': forms.Select(attrs={'class': 'form-control'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'libelle': forms.TextInput(attrs={'class': 'form-control'}),
            'reference': forms.TextInput(attrs={'class': 'form-control'}),
        }


class FormulaireBudget(forms.ModelForm):
    """Formulaire pour les budgets"""
    class Meta:
        model = Budget
        fields = ['exercice', 'compte', 'mois', 'montant_prevu', 'notes']
        widgets = {
            'exercice': forms.Select(attrs={'class': 'form-control'}),
            'compte': forms.Select(attrs={'class': 'form-control'}),
            'mois': forms.Select(attrs={'class': 'form-control'}, choices=[(i, f'Mois {i}') for i in range(1, 13)]),
            'montant_prevu': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class FormulaireRapprochementBancaire(forms.Form):
    """Formulaire pour le rapprochement bancaire"""
    banque = forms.ModelChoiceField(
        queryset=Banque.objects.filter(est_actif=True),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Banque"
    )
    date_debut = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label="Date de début"
    )
    date_fin = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label="Date de fin"
    )
    solde_releve = forms.DecimalField(
        max_digits=15,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        label="Solde du relevé bancaire"
    )
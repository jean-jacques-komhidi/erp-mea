# achats/signals.py - Signaux pour l'automatisation du module achats

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from decimal import Decimal
from .models import CommandeAchat, LigneCommandeAchat, PaiementFournisseur


@receiver(post_save, sender=LigneCommandeAchat)
def recalculer_totaux_commande(sender, instance, created, **kwargs):
    """
    Signal pour recalculer automatiquement les totaux de la commande
    après chaque modification de ligne
    """
    if instance.commande:
        instance.commande.calculer_totaux()


@receiver(pre_save, sender=CommandeAchat)
def verifier_statut_commande(sender, instance, **kwargs):
    """
    Signal pour vérifier et ajuster le statut de la commande
    avant la sauvegarde
    """
    # Si la commande existe déjà (modification)
    if instance.pk:
        try:
            ancienne_commande = CommandeAchat.objects.get(pk=instance.pk)
            
            # Si le statut passe à RECUE, vérifier que toutes les lignes sont reçues
            if instance.statut == 'RECUE' and ancienne_commande.statut != 'RECUE':
                if not instance.est_completement_recue():
                    # Ne pas permettre de passer à RECUE si pas complètement reçu
                    instance.statut = ancienne_commande.statut
            
        except CommandeAchat.DoesNotExist:
            pass


@receiver(post_save, sender=CommandeAchat)
def generer_ecriture_automatique(sender, instance, created, **kwargs):
    """
    Signal pour générer automatiquement l'écriture comptable
    lorsqu'une commande passe au statut RECUE
    
    NOTE: Cette fonction est optionnelle et peut être désactivée
    si vous préférez générer les écritures manuellement depuis les vues
    """
    # Désactivé par défaut - décommentez pour activer l'automatisation complète
    """
    if instance.statut == 'RECUE' and not instance.piece_comptable:
        try:
            from comptabilite.models import Journal, Exercice
            from django.utils import timezone
            
            # Trouver le journal d'achats
            journal_achat = Journal.objects.filter(
                type_journal='ACHAT', 
                est_actif=True
            ).first()
            
            # Trouver l'exercice en cours
            aujourdhui = timezone.now().date()
            exercice = Exercice.objects.filter(
                est_cloture=False,
                date_debut__lte=aujourdhui,
                date_fin__gte=aujourdhui
            ).first()
            
            if journal_achat and exercice:
                instance.generer_ecriture_comptable(journal_achat, exercice)
                
        except Exception as e:
            # Logger l'erreur sans bloquer l'enregistrement
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Erreur génération écriture comptable: {str(e)}")
    """
    pass


@receiver(post_save, sender=PaiementFournisseur)
def generer_ecriture_paiement(sender, instance, created, **kwargs):
    """
    Signal pour générer automatiquement l'écriture comptable
    lors d'un nouveau paiement fournisseur
    
    NOTE: Cette fonction est optionnelle et peut être désactivée
    si vous préférez générer les écritures manuellement
    """
    # Désactivé par défaut - décommentez pour activer
    """
    if created and not instance.piece_comptable:
        try:
            from comptabilite.models import Journal, Exercice, Banque
            from django.utils import timezone
            
            # Trouver le journal de banque
            journal_banque = Journal.objects.filter(
                type_journal='BANQUE',
                est_actif=True
            ).first()
            
            # Trouver l'exercice en cours
            aujourdhui = timezone.now().date()
            exercice = Exercice.objects.filter(
                est_cloture=False,
                date_debut__lte=aujourdhui,
                date_fin__gte=aujourdhui
            ).first()
            
            # Trouver la banque par défaut
            banque = Banque.objects.filter(est_actif=True).first()
            
            if journal_banque and exercice and banque:
                instance.generer_ecriture_comptable(journal_banque, exercice, banque)
                
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Erreur génération écriture paiement: {str(e)}")
    """
    pass


# Signal pour logger les changements de statut (optionnel)
@receiver(pre_save, sender=CommandeAchat)
def logger_changement_statut(sender, instance, **kwargs):
    """
    Signal pour logger les changements de statut dans les logs
    """
    if instance.pk:
        try:
            ancienne_commande = CommandeAchat.objects.get(pk=instance.pk)
            
            if ancienne_commande.statut != instance.statut:
                import logging
                logger = logging.getLogger(__name__)
                logger.info(
                    f"Commande {instance.numero_commande}: "
                    f"Statut changé de {ancienne_commande.get_statut_display()} "
                    f"à {instance.get_statut_display()}"
                )
        except CommandeAchat.DoesNotExist:
            pass


# Signal pour notifier les utilisateurs (optionnel - à implémenter selon vos besoins)
@receiver(post_save, sender=CommandeAchat)
def notifier_changement_commande(sender, instance, created, **kwargs):
    """
    Signal pour envoyer des notifications lors de changements importants
    
    Exemples d'utilisation:
    - Envoyer un email au fournisseur quand la commande passe à ENVOYEE
    - Notifier l'équipe logistique quand une commande est RECUE
    - Alerter la comptabilité quand une commande est FACTUREE
    
    NOTE: À implémenter selon vos besoins de notification
    """
    # TODO: Implémenter la logique de notification
    # Exemples:
    # - Email
    # - SMS
    # - Notification push
    # - Webhook
    pass
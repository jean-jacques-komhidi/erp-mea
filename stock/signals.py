from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MouvementStock, Stock

@receiver(post_save, sender=MouvementStock)
def mettre_a_jour_stock(sender, instance, created, **kwargs):
    """Mettre à jour le stock après un mouvement"""
    if created:
        # Récupérer ou créer le stock
        stock, _ = Stock.objects.get_or_create(
            produit=instance.produit,
            entrepot=instance.entrepot,
            defaults={'quantite': 0}
        )
        
        # Mettre à jour la quantité selon le type de mouvement
        if instance.type_mouvement in ['ENTREE', 'AJUSTEMENT']:
            stock.quantite += instance.quantite
        elif instance.type_mouvement == 'SORTIE':
            stock.quantite -= instance.quantite
        
        stock.save()
from django.apps import AppConfig

class StockConfig(AppConfig):
    list_display = ['produit', 'entrepot', 'quantite', 'date_derniere_maj']
    list_filter = ['entrepot', 'produit__categorie']
    search_fields = ['produit__nom', 'produit__code', 'entrepot__nom']
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stock'
    
    def ready(self):
        import stock.signals  # Importer les signaux
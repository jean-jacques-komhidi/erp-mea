# achats/apps.py - Configuration de l'application achats

from django.apps import AppConfig


class AchatsConfig(AppConfig):
    """Configuration de l'application de gestion des achats"""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'achats'
    verbose_name = 'Gestion des Achats'
    
    def ready(self):
        """
        Méthode appelée lorsque l'application est prête.
        Utilisée pour charger les signaux et autres configurations.
        """
        # Importer les signaux si le fichier signals.py existe
        try:
            import achats.signals
        except ImportError:
            pass
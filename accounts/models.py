# ============================================
# NOUVEAU FICHIER : accounts/models.py
# Modèles pour l'authentification et la gestion des utilisateurs
# ============================================

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Profil(models.Model):
    """
    Profil étendu pour l'utilisateur
    """
    ROLES = [
        ('ADMIN', 'Administrateur'),
        ('MANAGER', 'Gestionnaire'),
        ('COMPTABLE', 'Comptable'),
        ('COMMERCIAL', 'Commercial'),
        ('MAGASINIER', 'Magasinier'),
        ('USER', 'Utilisateur'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')
    role = models.CharField(max_length=20, choices=ROLES, default='USER', verbose_name="Rôle")
    
    # Informations personnelles
    telephone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    adresse = models.TextField(blank=True, verbose_name="Adresse")
    ville = models.CharField(max_length=100, blank=True, verbose_name="Ville")
    code_postal = models.CharField(max_length=10, blank=True, verbose_name="Code postal")
    photo = models.ImageField(upload_to='profils/', blank=True, null=True, verbose_name="Photo de profil")
    
    # Paramètres de sécurité
    two_factor_enabled = models.BooleanField(default=False, verbose_name="2FA activé")
    two_factor_secret = models.CharField(max_length=32, blank=True, verbose_name="Secret 2FA")
    email_verified = models.BooleanField(default=False, verbose_name="Email vérifié")
    email_verification_token = models.CharField(max_length=100, blank=True, verbose_name="Token de vérification")
    
    # Métadonnées
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    dernier_login = models.DateTimeField(null=True, blank=True, verbose_name="Dernier login")
    
    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profils"
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_role_display()})"
    
    def get_initiales(self):
        """Retourne les initiales de l'utilisateur"""
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name[0]}{self.user.last_name[0]}".upper()
        return self.user.username[:2].upper()
    
    def has_permission(self, permission):
        """Vérifie si l'utilisateur a une permission spécifique"""
        return Permission.objects.filter(
            role_permissions__role=self.role,
            role_permissions__est_actif=True,
            code=permission
        ).exists()
    
    def get_permissions(self):
        """Retourne toutes les permissions de l'utilisateur"""
        return Permission.objects.filter(
            role_permissions__role=self.role,
            role_permissions__est_actif=True
        )


# Signal pour créer automatiquement un profil lors de la création d'un utilisateur
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profil.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profil.save()


class Permission(models.Model):
    """
    Permissions du système
    """
    MODULES = [
        ('CLIENTS', 'Clients'),
        ('FOURNISSEURS', 'Fournisseurs'),
        ('STOCK', 'Stock'),
        ('VENTES', 'Ventes'),
        ('ACHATS', 'Achats'),
        ('COMPTABILITE', 'Comptabilité'),
        ('RAPPORTS', 'Rapports'),
        ('ADMINISTRATION', 'Administration'),
    ]
    
    code = models.CharField(max_length=100, unique=True, verbose_name="Code")
    nom = models.CharField(max_length=200, verbose_name="Nom")
    description = models.TextField(blank=True, verbose_name="Description")
    module = models.CharField(max_length=50, choices=MODULES, verbose_name="Module")
    
    class Meta:
        verbose_name = "Permission"
        verbose_name_plural = "Permissions"
        ordering = ['module', 'nom']
    
    def __str__(self):
        return f"{self.nom} ({self.module})"


class RolePermission(models.Model):
    """
    Association Rôle-Permission
    """
    role = models.CharField(max_length=20, choices=Profil.ROLES, verbose_name="Rôle")
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name='role_permissions')
    est_actif = models.BooleanField(default=True, verbose_name="Est actif")
    
    class Meta:
        verbose_name = "Rôle-Permission"
        verbose_name_plural = "Rôles-Permissions"
        unique_together = ['role', 'permission']
    
    def __str__(self):
        return f"{self.get_role_display()} - {self.permission.nom}"


class LogConnexion(models.Model):
    """
    Journal des connexions
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logs_connexion')
    date_connexion = models.DateTimeField(auto_now_add=True, verbose_name="Date de connexion")
    ip_address = models.GenericIPAddressField(verbose_name="Adresse IP")
    user_agent = models.TextField(verbose_name="User Agent")
    succes = models.BooleanField(default=True, verbose_name="Succès")
    message = models.TextField(blank=True, verbose_name="Message")
    
    class Meta:
        verbose_name = "Log de connexion"
        verbose_name_plural = "Logs de connexion"
        ordering = ['-date_connexion']
    
    def __str__(self):
        return f"{self.user.username} - {self.date_connexion.strftime('%d/%m/%Y %H:%M')}"


class PasswordResetToken(models.Model):
    """
    Tokens pour la réinitialisation de mot de passe
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_tokens')
    token = models.CharField(max_length=100, unique=True, verbose_name="Token")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_expiration = models.DateTimeField(verbose_name="Date d'expiration")
    utilise = models.BooleanField(default=False, verbose_name="Utilisé")
    
    class Meta:
        verbose_name = "Token de réinitialisation"
        verbose_name_plural = "Tokens de réinitialisation"
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"{self.user.username} - {self.token[:10]}..."
    
    def is_valid(self):
        """Vérifie si le token est encore valide"""
        return not self.utilise and timezone.now() < self.date_expiration
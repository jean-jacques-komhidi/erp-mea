# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profil, Permission, RolePermission, LogConnexion, PasswordResetToken


class ProfilInline(admin.StackedInline):
    """
    Afficher le profil directement dans la page d'édition de l'utilisateur
    """
    model = Profil
    can_delete = False
    verbose_name_plural = 'Profil'
    fk_name = 'user'
    fields = ('role', 'telephone', 'adresse', 'ville', 'code_postal', 'photo', 
              'email_verified', 'two_factor_enabled')


class UserAdmin(BaseUserAdmin):
    """
    Admin personnalisé pour User avec le Profil intégré
    """
    inlines = (ProfilInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'profil__role', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    
    def get_role(self, obj):
        return obj.profil.get_role_display()
    get_role.short_description = 'Rôle'
    get_role.admin_order_field = 'profil__role'


# Désenregistrer l'admin User par défaut et enregistrer le nôtre
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    """
    Admin pour gérer directement les profils
    """
    list_display = ('user', 'get_full_name', 'role', 'telephone', 'email_verified', 'two_factor_enabled', 'date_creation')
    list_filter = ('role', 'email_verified', 'two_factor_enabled', 'date_creation')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email', 'telephone')
    readonly_fields = ('date_creation', 'date_modification', 'dernier_login')
    
    fieldsets = (
        ('Utilisateur', {
            'fields': ('user', 'role')
        }),
        ('Informations personnelles', {
            'fields': ('telephone', 'adresse', 'ville', 'code_postal', 'photo')
        }),
        ('Sécurité', {
            'fields': ('email_verified', 'email_verification_token', 'two_factor_enabled', 'two_factor_secret')
        }),
        ('Métadonnées', {
            'fields': ('date_creation', 'date_modification', 'dernier_login'),
            'classes': ('collapse',)
        }),
    )
    
    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_full_name.short_description = 'Nom complet'


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    """
    Admin pour gérer les permissions
    """
    list_display = ('code', 'nom', 'module', 'description')
    list_filter = ('module',)
    search_fields = ('code', 'nom', 'description')


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    """
    Admin pour gérer les rôles-permissions
    """
    list_display = ('role', 'permission', 'est_actif')
    list_filter = ('role', 'est_actif', 'permission__module')
    search_fields = ('permission__nom', 'permission__code')


@admin.register(LogConnexion)
class LogConnexionAdmin(admin.ModelAdmin):
    """
    Admin pour voir les logs de connexion
    """
    list_display = ('user', 'date_connexion', 'ip_address', 'succes', 'message')
    list_filter = ('succes', 'date_connexion')
    search_fields = ('user__username', 'ip_address', 'message')
    readonly_fields = ('user', 'date_connexion', 'ip_address', 'user_agent', 'succes', 'message')
    date_hierarchy = 'date_connexion'
    
    def has_add_permission(self, request):
        return False  # Empêcher l'ajout manuel
    
    def has_change_permission(self, request, obj=None):
        return False  # Empêcher la modification


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    """
    Admin pour gérer les tokens de réinitialisation
    """
    list_display = ('user', 'token_preview', 'date_creation', 'date_expiration', 'utilise', 'is_valid')
    list_filter = ('utilise', 'date_creation', 'date_expiration')
    search_fields = ('user__username', 'user__email', 'token')
    readonly_fields = ('user', 'token', 'date_creation', 'date_expiration', 'utilise')
    date_hierarchy = 'date_creation'
    
    def token_preview(self, obj):
        return f"{obj.token[:20]}..."
    token_preview.short_description = 'Token'
    
    def is_valid(self, obj):
        return obj.is_valid()
    is_valid.boolean = True
    is_valid.short_description = 'Valide'
    
    def has_add_permission(self, request):
        return False
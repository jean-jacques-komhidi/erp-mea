# ============================================
# NOUVEAU FICHIER : accounts/decorators.py
# Décorateurs personnalisés pour les permissions
# ============================================

from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def require_role(*allowed_roles):
    """
    Décorateur pour restreindre l'accès selon le rôle de l'utilisateur
    
    Usage:
        @require_role('ADMIN')
        def ma_vue(request):
            ...
        
        @require_role('ADMIN', 'MANAGER')
        def ma_vue(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Vérifier si l'utilisateur est authentifié
            if not request.user.is_authenticated:
                messages.error(request, 'Vous devez être connecté pour accéder à cette page.')
                return redirect('accounts:login')
            
            # Vérifier le rôle
            user_role = request.user.profil.role
            
            if user_role not in allowed_roles:
                messages.error(request, f'Accès refusé. Cette page est réservée aux : {", ".join(allowed_roles)}.')
                return redirect('/')
            
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator


def require_permission(permission_code):
    """
    Décorateur pour vérifier une permission spécifique
    
    Usage:
        @require_permission('STOCK_VIEW')
        def liste_stock(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Vérifier si l'utilisateur est authentifié
            if not request.user.is_authenticated:
                messages.error(request, 'Vous devez être connecté pour accéder à cette page.')
                return redirect('accounts:login')
            
            # Vérifier la permission
            if not request.user.profil.has_permission(permission_code):
                messages.error(request, 'Vous n\'avez pas la permission d\'accéder à cette page.')
                return redirect('/')
            
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator


def admin_required(view_func):
    """
    Décorateur pour restreindre l'accès aux administrateurs uniquement
    
    Usage:
        @admin_required
        def gestion_utilisateurs(request):
            ...
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Vous devez être connecté pour accéder à cette page.')
            return redirect('accounts:login')
        
        if request.user.profil.role != 'ADMIN':
            messages.error(request, 'Accès refusé. Page réservée aux administrateurs.')
            return redirect('/')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper
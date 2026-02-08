# ============================================
# NOUVEAU FICHIER : accounts/views.py
# Vues pour l'authentification et la gestion des utilisateurs
# ============================================

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from datetime import timedelta
import secrets
import string

from .models import Profil, LogConnexion, PasswordResetToken


def get_client_ip(request):
    """Récupère l'adresse IP du client"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def log_connexion(user, request, succes=True, message=''):
    """Enregistre une tentative de connexion"""
    LogConnexion.objects.create(
        user=user,
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
        succes=succes,
        message=message
    )


# ========== LOGIN ==========

def login_view(request):
    """Vue de connexion"""
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                
                # Gérer "Se souvenir de moi"
                if not remember_me:
                    request.session.set_expiry(0)  # Session expire à la fermeture du navigateur
                else:
                    request.session.set_expiry(1209600)  # 2 semaines
                
                # Mettre à jour le dernier login
                user.profil.dernier_login = timezone.now()
                user.profil.save()
                
                # Logger la connexion
                log_connexion(user, request, succes=True, message='Connexion réussie')
                
                messages.success(request, f'Bienvenue {user.get_full_name() or user.username} !')
                
                # Rediriger vers la page demandée ou le tableau de bord
                next_url = request.GET.get('next', '/')
                return redirect(next_url)
            else:
                messages.error(request, 'Votre compte est désactivé.')
        else:
            # Logger la tentative échouée si l'utilisateur existe
            try:
                failed_user = User.objects.get(username=username)
                log_connexion(failed_user, request, succes=False, message='Mot de passe incorrect')
            except User.DoesNotExist:
                pass
            
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    
    return render(request, 'accounts/login.jinja')


# ========== REGISTER ==========

def register_view(request):
    """Vue d'inscription"""
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Validation
        errors = []
        
        if not username or len(username) < 3:
            errors.append('Le nom d\'utilisateur doit contenir au moins 3 caractères.')
        
        if User.objects.filter(username=username).exists():
            errors.append('Ce nom d\'utilisateur est déjà utilisé.')
        
        if not email:
            errors.append('L\'email est obligatoire.')
        
        if User.objects.filter(email=email).exists():
            errors.append('Cet email est déjà utilisé.')
        
        if not password1 or len(password1) < 8:
            errors.append('Le mot de passe doit contenir au moins 8 caractères.')
        
        if password1 != password2:
            errors.append('Les mots de passe ne correspondent pas.')
        
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            # Créer l'utilisateur
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name
            )
            
            # Générer un token de vérification email
            verification_token = secrets.token_urlsafe(32)
            user.profil.email_verification_token = verification_token
            user.profil.save()
            
            # TODO: Envoyer l'email de vérification
            # send_verification_email(user, verification_token)
            
            messages.success(request, 'Votre compte a été créé avec succès ! Vous pouvez maintenant vous connecter.')
            return redirect('accounts:login')
    
    return render(request, 'accounts/register.jinja')


# ========== LOGOUT ==========

@login_required
def logout_view(request):
    """Vue de déconnexion"""
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès.')
    return redirect('accounts:login')


# ========== PROFIL ==========

@login_required
def profil_view(request):
    """Vue du profil utilisateur"""
    profil = request.user.profil
    
    # Récupérer les dernières connexions
    derniers_logs = LogConnexion.objects.filter(user=request.user).order_by('-date_connexion')[:10]
    
    context = {
        'profil': profil,
        'derniers_logs': derniers_logs,
    }
    
    return render(request, 'accounts/profil.jinja', context)


@login_required
def modifier_profil(request):
    """Vue de modification du profil"""
    profil = request.user.profil
    
    if request.method == 'POST':
        # Mettre à jour les informations de l'utilisateur
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        
        # Mettre à jour le profil
        profil.telephone = request.POST.get('telephone', '')
        profil.adresse = request.POST.get('adresse', '')
        profil.ville = request.POST.get('ville', '')
        profil.code_postal = request.POST.get('code_postal', '')
        
        # Gérer l'upload de photo
        if 'photo' in request.FILES:
            profil.photo = request.FILES['photo']
        
        profil.save()
        
        messages.success(request, 'Votre profil a été mis à jour avec succès !')
        return redirect('accounts:profil')
    
    return render(request, 'accounts/modifier_profil.jinja', {'profil': profil})


@login_required
def changer_mot_de_passe(request):
    """Vue de changement de mot de passe"""
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        
        # Vérifier l'ancien mot de passe
        if not request.user.check_password(old_password):
            messages.error(request, 'L\'ancien mot de passe est incorrect.')
        elif new_password1 != new_password2:
            messages.error(request, 'Les nouveaux mots de passe ne correspondent pas.')
        elif len(new_password1) < 8:
            messages.error(request, 'Le nouveau mot de passe doit contenir au moins 8 caractères.')
        else:
            request.user.set_password(new_password1)
            request.user.save()
            
            # Maintenir la session active
            update_session_auth_hash(request, request.user)
            
            messages.success(request, 'Votre mot de passe a été changé avec succès !')
            return redirect('accounts:profil')
    
    return render(request, 'accounts/changer_mot_de_passe.jinja')


# ========== MOT DE PASSE OUBLIÉ ==========

def mot_de_passe_oublie(request):
    """Vue mot de passe oublié"""
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = User.objects.get(email=email)
            
            # Générer un token
            token = secrets.token_urlsafe(32)
            
            # Créer le token de réinitialisation
            reset_token = PasswordResetToken.objects.create(
                user=user,
                token=token,
                date_expiration=timezone.now() + timedelta(hours=24)
            )
            
            # Construire le lien de réinitialisation
            reset_link = request.build_absolute_uri(f'/accounts/reinitialiser-mot-de-passe/{token}/')
            
            # Date d'expiration formatée
            expiration_date = reset_token.date_expiration.strftime('%d/%m/%Y à %H:%M')
            
            # Message simple en texte
            message = f"""
Bonjour {user.get_full_name() or user.username},

Vous avez demandé la réinitialisation de votre mot de passe pour votre compte ERP MEA.

Cliquez sur ce lien pour réinitialiser votre mot de passe :
{reset_link}

⏰ Ce lien est valide jusqu'au {expiration_date}.

Si vous n'avez pas demandé cette réinitialisation, ignorez cet email.

Cordialement,
L'équipe ERP MEA
"""
            
            # Envoyer l'email
            try:
                send_mail(
                    subject='Réinitialisation de votre mot de passe - ERP MEA',
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                
                messages.success(request, f'Un email de réinitialisation a été envoyé à {email}. Veuillez vérifier votre boîte de réception.')
            except Exception as e:
                messages.error(request, f'Erreur lors de l\'envoi de l\'email. Veuillez réessayer plus tard.')
                print(f"Erreur d'envoi d'email : {e}")
            
            return redirect('accounts:login')
        
        except User.DoesNotExist:
            # Ne pas révéler si l'email existe ou non (sécurité)
            messages.success(request, 'Si cet email existe dans notre système, un lien de réinitialisation a été envoyé.')
            return redirect('accounts:login')
    
    return render(request, 'accounts/mot_de_passe_oublie.jinja')


def reinitialiser_mot_de_passe(request, token):
    """Vue de réinitialisation du mot de passe"""
    try:
        reset_token = PasswordResetToken.objects.get(token=token)
        
        if not reset_token.is_valid():
            messages.error(request, 'Ce lien de réinitialisation a expiré ou a déjà été utilisé.')
            return redirect('accounts:login')
        
        if request.method == 'POST':
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')
            
            if new_password1 != new_password2:
                messages.error(request, 'Les mots de passe ne correspondent pas.')
            elif len(new_password1) < 8:
                messages.error(request, 'Le mot de passe doit contenir au moins 8 caractères.')
            else:
                # Changer le mot de passe
                reset_token.user.set_password(new_password1)
                reset_token.user.save()
                
                # Marquer le token comme utilisé
                reset_token.utilise = True
                reset_token.save()
                
                messages.success(request, 'Votre mot de passe a été réinitialisé avec succès ! Vous pouvez maintenant vous connecter.')
                return redirect('accounts:login')
        
        return render(request, 'accounts/reinitialiser_mot_de_passe.jinja', {'token': token})
    
    except PasswordResetToken.DoesNotExist:
        messages.error(request, 'Lien de réinitialisation invalide.')
        return redirect('accounts:login')


# ========== VÉRIFICATION EMAIL ==========

def verifier_email(request, token):
    """Vue de vérification d'email"""
    try:
        profil = Profil.objects.get(email_verification_token=token)
        
        if not profil.email_verified:
            profil.email_verified = True
            profil.save()
            
            messages.success(request, 'Votre email a été vérifié avec succès !')
        else:
            messages.info(request, 'Votre email est déjà vérifié.')
        
        return redirect('accounts:login')
    
    except Profil.DoesNotExist:
        messages.error(request, 'Lien de vérification invalide.')
        return redirect('accounts:login')


# ========== GESTION DES UTILISATEURS (Admin) ==========

@login_required
def liste_utilisateurs(request):
    """Liste des utilisateurs (Admin uniquement)"""
    if request.user.profil.role != 'ADMIN':
        messages.error(request, 'Vous n\'avez pas la permission d\'accéder à cette page.')
        return redirect('/')
    
    utilisateurs = User.objects.select_related('profil').all().order_by('-date_joined')
    
    context = {
        'utilisateurs': utilisateurs,
    }
    
    return render(request, 'accounts/liste_utilisateurs.jinja', context)


@login_required
def modifier_utilisateur(request, user_id):
    """Modifier un utilisateur (Admin uniquement)"""
    if request.user.profil.role != 'ADMIN':
        messages.error(request, 'Vous n\'avez pas la permission d\'accéder à cette page.')
        return redirect('/')
    
    user = get_object_or_404(User, pk=user_id)
    
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.is_active = request.POST.get('is_active') == 'on'
        user.save()
        
        # Mettre à jour le rôle
        user.profil.role = request.POST.get('role', 'USER')
        user.profil.save()
        
        messages.success(request, f'L\'utilisateur {user.username} a été mis à jour avec succès !')
        return redirect('accounts:liste_utilisateurs')
    
    context = {
        'user_to_edit': user,
        'roles': Profil.ROLES,
    }
    
    return render(request, 'accounts/modifier_utilisateur.jinja', context)
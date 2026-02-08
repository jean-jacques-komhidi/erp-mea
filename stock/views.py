from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q, F

from .models import MouvementStock, Stock
from .models import Produit, Categorie, MouvementStock, Entrepot
from .forms import FormulaireProduit, FormulaireMouvementStock, FormulaireCategorie, FormulaireEntrepot


# ========== GESTION DES PRODUITS ==========

@login_required
def liste_produits(request):
    """Vue pour afficher la liste des produits"""
    recherche = request.GET.get('recherche', '')
    categorie_id = request.GET.get('categorie', '')
    
    produits = Produit.objects.filter(est_actif=True).select_related('categorie')
    
    if recherche:
        produits = produits.filter(
            Q(code__icontains=recherche) |
            Q(nom__icontains=recherche) |
            Q(description__icontains=recherche)
        )
    
    if categorie_id:
        produits = produits.filter(categorie_id=categorie_id)
    
    # Ajouter le stock actuel pour chaque produit
    produits = produits.annotate(
        stock_actuel_qte=Sum('mouvementstock__quantite')
    )
    
    categories = Categorie.objects.all().order_by('nom')
    
    contexte = {
        'produits': produits.order_by('nom'),
        'categories': categories,
        'recherche': recherche,
        'categorie_selectionnee': categorie_id,
    }
    
    return render(request, 'stock/liste_produits.jinja', contexte)


@login_required
def creer_produit(request):
    """Vue pour créer un nouveau produit"""
    if request.method == 'POST':
        formulaire = FormulaireProduit(request.POST, request.FILES)
        if formulaire.is_valid():
            formulaire.save()
            messages.success(request, 'Produit créé avec succès!')
            return redirect('stock:liste_produits')
    else:
        formulaire = FormulaireProduit()
    
    contexte = {
        'formulaire': formulaire,
        'action': 'Créer'
    }
    
    return render(request, 'stock/formulaire_produit.jinja', contexte)




@login_required
def details_produit(request, pk):
    """Vue pour afficher les détails d'un produit"""
    produit = get_object_or_404(Produit, pk=pk)
    mouvements = MouvementStock.objects.filter(
        produit=produit
    ).select_related('entrepot', 'utilisateur').order_by('-date')[:20]
    
    stock_par_entrepot = MouvementStock.objects.filter(
        produit=produit
    ).values('entrepot__nom').annotate(stock=Sum('quantite'))
    
    contexte = {
        'produit': produit,
        'mouvements': mouvements,
        'stock_par_entrepot': stock_par_entrepot,
        'stock_actuel': produit.stock_actuel,
    }
    
    return render(request, 'stock/details_produit.jinja', contexte)


@login_required
def modifier_produit(request, pk):
    """Vue pour modifier un produit existant"""
    produit = get_object_or_404(Produit, pk=pk)
    
    if request.method == 'POST':
        formulaire = FormulaireProduit(request.POST, request.FILES, instance=produit)
        if formulaire.is_valid():
            formulaire.save()
            messages.success(request, 'Produit modifié avec succès!')
            return redirect('stock:liste_produits')
    else:
        formulaire = FormulaireProduit(instance=produit)
    
    contexte = {
        'formulaire': formulaire,
        'action': 'Modifier',
        'produit': produit
    }
    
    return render(request, 'stock/formulaire_produit.jinja', contexte)

@login_required
def supprimer_produit(request, pk):
    """Vue pour désactiver un produit"""
    produit = get_object_or_404(Produit, pk=pk)
    
    if request.method == 'POST':
        produit.est_actif = False
        produit.save()
        messages.success(request, 'Produit désactivé avec succès!')
        return redirect('stock:liste_produits')
    
    contexte = {'produit': produit}
    return render(request, 'stock/confirmer_suppression_produit.jinja', contexte)


# ========== GESTION DES CATÉGORIES ==========

@login_required
def liste_categories(request):
    """Vue pour afficher la liste des catégories"""
    categories = Categorie.objects.all().order_by('nom')
    recherche = request.GET.get('recherche', '')
    
    # Compter le nombre de produits par catégorie
    for categorie in categories:
        categorie.nombre_produits = Produit.objects.filter(
            categorie=categorie, 
            est_actif=True
        ).count()

        
    
    contexte = {'categories': categories}
    return render(request, 'stock/liste_categories.jinja', contexte)


@login_required
def creer_categorie(request):
    """Vue pour créer une nouvelle catégorie"""
    if request.method == 'POST':
        formulaire = FormulaireCategorie(request.POST)
        if formulaire.is_valid():
            formulaire.save()
            messages.success(request, 'Catégorie créée avec succès!')
            return redirect('stock:liste_categories')
    else:
        formulaire = FormulaireCategorie()
    
    contexte = {
        'formulaire': formulaire,
        'action': 'Créer'
    }
    return render(request, 'stock/formulaire_categorie.jinja', contexte)


@login_required
def modifier_categorie(request, pk):
    """Vue pour modifier une catégorie existante"""
    try:
        categorie = get_object_or_404(Categorie, pk=pk)
        
        if request.method == 'POST':
            formulaire = FormulaireCategorie(request.POST, instance=categorie)
            if formulaire.is_valid():
                formulaire.save()
                messages.success(request, 'Catégorie modifiée avec succès!')
                return redirect('stock:liste_categories')
        else:
            formulaire = FormulaireCategorie(instance=categorie)
        
        # Compter les produits associés
        nombre_produits = Produit.objects.filter(categorie=categorie, est_actif=True).count()
        
        contexte = {
            'formulaire': formulaire,
            'action': 'Modifier',
            'categorie': categorie,
            'nombre_produits': nombre_produits
        }
        return render(request, 'stock/formulaire_categorie.jinja', contexte)
        
    except Exception as e:
        messages.error(request, f'Erreur lors de la modification : {str(e)}')
        return redirect('stock:liste_categories')


@login_required
def details_categorie(request, pk):
    """Vue pour afficher les détails d'une catégorie"""
    try:
        categorie = get_object_or_404(Categorie, pk=pk)
        
        # Récupérer les produits de cette catégorie
        produits = Produit.objects.filter(categorie=categorie, est_actif=True).order_by('nom')
        
        # Statistiques
        nombre_produits = produits.count()
        valeur_stock = sum(produit.stock_actuel_qte * produit.prix_vente for produit in produits if produit.stock_actuel_qte)
        
        # Produits par statut
        produits_stock_bas = produits.filter(stock_actuel_qte__lte=F('stock_min')).count()
        produits_rupture = produits.filter(stock_actuel_qte__lte=F('seuil_reapprovisionnement')).count()
        produits_en_stock = produits.filter(stock_actuel_qte__gt=0).count()
        
        contexte = {
            'categorie': categorie,
            'produits': produits,
            'nombre_produits': nombre_produits,
            'valeur_stock': valeur_stock,
            'produits_stock_bas': produits_stock_bas,
            'produits_rupture': produits_rupture,
            'produits_en_stock': produits_en_stock,
        }
        return render(request, 'stock/details_categorie.jinja', contexte)
        
    except Exception as e:
        messages.error(request, f'Erreur lors de l\'affichage des détails : {str(e)}')
        return redirect('stock:liste_categories')


@login_required
def supprimer_categorie(request, pk):
    """Vue pour supprimer (désactiver) une catégorie"""
    try:
        categorie = get_object_or_404(Categorie, pk=pk)
        
        if request.method == 'POST':
            # Vérifier si la catégorie a des produits actifs
            produits_associes = Produit.objects.filter(categorie=categorie, est_actif=True).count()
            
            # Vérifier si la catégorie a des sous-catégories
            sous_categories = Categorie.objects.filter(parent=categorie).count()
            
            if produits_associes > 0:
                messages.warning(request, f'Impossible de supprimer cette catégorie. {produits_associes} produit(s) y sont associés.')
                return redirect('stock:details_categorie', pk=pk)
            elif sous_categories > 0:
                messages.warning(request, f'Impossible de supprimer cette catégorie. {sous_categories} sous-catégorie(s) y sont associées.')
                return redirect('stock:details_categorie', pk=pk)
            else:
                # Si aucun produit ni sous-catégorie, on peut supprimer
                nom_categorie = categorie.nom
                categorie.delete()
                messages.success(request, f'Catégorie "{nom_categorie}" supprimée avec succès!')
                return redirect('stock:liste_categories')
        
        # Récupérer les informations pour la confirmation
        produits_associes_queryset = Produit.objects.filter(categorie=categorie, est_actif=True)
        sous_categories_queryset = Categorie.objects.filter(parent=categorie)
        
        contexte = {
            'categorie': categorie,
            'produits_associes': produits_associes_queryset.count(),
            'produits_liste': produits_associes_queryset[:10],  # Limiter à 10 pour l'affichage
            'sous_categories': sous_categories_queryset,
        }
        return render(request, 'stock/confirmer_suppression_categorie.jinja', contexte)
        
    except Exception as e:
        messages.error(request, f'Erreur lors de la suppression : {str(e)}')
        return redirect('stock:liste_categories')
    

# ========== GESTION DES MOUVEMENTS DE STOCK ==========

@login_required
def liste_mouvements(request):
    """Vue pour afficher la liste des mouvements de stock"""
    type_mouvement = request.GET.get('type', '')
    produit_id = request.GET.get('produit', '')
    entrepot_id = request.GET.get('entrepot', '')
    
    mouvements = MouvementStock.objects.select_related(
        'produit', 'entrepot', 'utilisateur'
    ).order_by('-date')
    
    if type_mouvement:
        mouvements = mouvements.filter(type_mouvement=type_mouvement)
    
    if produit_id:
        mouvements = mouvements.filter(produit_id=produit_id)
    
    if entrepot_id:
        mouvements = mouvements.filter(entrepot_id=entrepot_id)
    
    # Limiter aux 100 derniers mouvements pour la performance
    mouvements = mouvements[:100]
    
    # Données pour les filtres
    produits = Produit.objects.filter(est_actif=True).order_by('nom')
    entrepots = Entrepot.objects.filter(est_actif=True).order_by('nom')
    
    contexte = {
        'mouvements': mouvements,
        'produits': produits,
        'entrepots': entrepots,
        'types_mouvement': MouvementStock.TYPES_MOUVEMENT,
        'type_selectionne': type_mouvement,
        'produit_selectionne': produit_id,
        'entrepot_selectionne': entrepot_id,
    }
    
    return render(request, 'stock/liste_mouvements.jinja', contexte)


@login_required
def creer_mouvement_stock(request):
    """Vue pour créer un mouvement de stock"""
    if request.method == 'POST':
        formulaire = FormulaireMouvementStock(request.POST)
        if formulaire.is_valid():
            mouvement = formulaire.save(commit=False)
            mouvement.utilisateur = request.user
            mouvement.save()
            messages.success(request, 'Mouvement de stock enregistré avec succès!')
            return redirect('stock:liste_mouvements')
    else:
        formulaire = FormulaireMouvementStock()
    
    contexte = {
        'formulaire': formulaire,
        'action': 'Créer'
        }
    return render(request, 'stock/formulaire_mouvement.jinja', contexte)

@login_required
def details_mouvement(request, pk):
    """Vue pour afficher les détails d'un mouvement de stock"""
    mouvement = get_object_or_404(
        MouvementStock.objects.select_related('produit', 'entrepot', 'utilisateur'),
        pk=pk
    )
    
    # Récupérer le stock actuel du produit dans l'entrepôt
    try:
        stock_obj = Stock.objects.get(
            produit=mouvement.produit,
            entrepot=mouvement.entrepot
        )
        stock_actuel = stock_obj.quantite
    except Stock.DoesNotExist:
        stock_actuel = 0
    
    # Récupérer les 5 derniers mouvements du même produit (sauf celui-ci)
    mouvements_connexes = MouvementStock.objects.filter(
        produit=mouvement.produit
    ).exclude(
        pk=mouvement.pk
    ).select_related(
        'entrepot', 'utilisateur'
    ).order_by('-date')[:5]
    
    contexte = {
        'mouvement': mouvement,
        'stock_actuel': stock_actuel,
        'mouvements_connexes': mouvements_connexes,
    }
    
    return render(request, 'stock/details_mouvement.jinja', contexte)


@login_required
def details_mouvement(request, pk):
    """Vue pour afficher les détails d'un mouvement de stock"""
    mouvement = get_object_or_404(
        MouvementStock.objects.select_related('produit', 'entrepot', 'utilisateur'),
        pk=pk
    )
    
    # Récupérer le stock actuel du produit dans l'entrepôt
    try:
        stock_obj = Stock.objects.get(  # ✅ Stock avec majuscule
            produit=mouvement.produit,
            entrepot=mouvement.entrepot
        )
        stock_actuel = stock_obj.quantite
    except Stock.DoesNotExist:  # ✅ Stock avec majuscule
        stock_actuel = 0
    
    # Récupérer les 5 derniers mouvements du même produit (sauf celui-ci)
    mouvements_connexes = MouvementStock.objects.filter(
        produit=mouvement.produit
    ).exclude(
        pk=mouvement.pk
    ).select_related(
        'entrepot', 'utilisateur'
    ).order_by('-date')[:5]
    
    contexte = {
        'mouvement': mouvement,
        'stock_actuel': stock_actuel,
        'mouvements_connexes': mouvements_connexes,
    }
    
    return render(request, 'stock/details_mouvement.jinja', contexte)


@login_required
def modifier_mouvement(request, pk):
    """Vue pour modifier un mouvement de stock"""
    mouvement = get_object_or_404(MouvementStock, pk=pk)
    
    if request.method == 'POST':
        formulaire = FormulaireMouvementStock(request.POST, instance=mouvement)
        if formulaire.is_valid():
            formulaire.save()
            messages.success(request, 'Mouvement de stock modifié avec succès!')
            return redirect('stock:details_mouvement', pk=mouvement.pk)
    else:
        formulaire = FormulaireMouvementStock(instance=mouvement)
    
    contexte = {
        'formulaire': formulaire,
        'mouvement': mouvement,
        'action': 'Modifier'
    }
    
    return render(request, 'stock/formulaire_mouvement.jinja', contexte)


@login_required
def supprimer_mouvement(request, pk):
    """Vue pour supprimer un mouvement de stock"""
    mouvement = get_object_or_404(
        MouvementStock.objects.select_related('produit', 'entrepot'),
        pk=pk
    )
    
    if request.method == 'POST':
        mouvement.delete()
        messages.success(request, 'Mouvement de stock supprimé avec succès!')
        return redirect('stock:liste_mouvements')
    
    contexte = {
        'mouvement': mouvement,
    }
    
    return render(request, 'stock/confirmer_supprimer_mouvement.jinja', contexte)


# ========== GESTION DES ENTREPÔTS ==========

@login_required
def liste_entrepots(request):
    """Vue pour afficher la liste des entrepôts"""
    entrepots = Entrepot.objects.filter(est_actif=True).order_by('nom')
    
    # Ajouter des statistiques pour chaque entrepôt
    for entrepot in entrepots:
        # Nombre de produits différents dans l'entrepôt
        entrepot.nombre_produits = MouvementStock.objects.filter(
            entrepot=entrepot
        ).values('produit').distinct().count()
        
        # Valeur totale du stock (si besoin)
        # Total des mouvements
        entrepot.total_mouvements = MouvementStock.objects.filter(
            entrepot=entrepot
        ).count()
    
    contexte = {'entrepots': entrepots}
    return render(request, 'stock/liste_entrepots.jinja', contexte)


@login_required
def creer_entrepot(request):
    """Vue pour créer un nouveau entrepôt"""
    if request.method == 'POST':
        formulaire = FormulaireEntrepot(request.POST)
        if formulaire.is_valid():
            formulaire.save()
            messages.success(request, 'Entrepôt créé avec succès!')
            return redirect('stock:liste_entrepots')
    else:
        formulaire = FormulaireEntrepot()
    
    contexte = {
        'formulaire': formulaire,
        'action': 'Créer'
    }
    return render(request, 'stock/formulaire_entrepot.jinja', contexte)

@login_required
def modifier_entrepot(request, pk):
    """Vue pour modifier un entrepôt existant"""
    entrepot = get_object_or_404(Entrepot, pk=pk)
    
    if request.method == 'POST':
        formulaire = FormulaireEntrepot(request.POST, instance=entrepot)
        if formulaire.is_valid():
            formulaire.save()
            messages.success(request, 'Entrepôt modifié avec succès!')
            return redirect('stock:liste_entrepots')
    else:
        formulaire = FormulaireEntrepot(instance=entrepot)
    
    contexte = {
        'formulaire': formulaire,
        'action': 'Modifier',
        'entrepot': entrepot
    }
    
    return render(request, 'stock/formulaire_entrepot.jinja', contexte)

@login_required
def details_entrepot(request, pk):
    """Vue pour afficher les détails d'un entrepôt"""
    entrepot = get_object_or_404(Entrepot, pk=pk)
    
    # Mouvements récents de cet entrepôt
    mouvements = MouvementStock.objects.filter(
        entrepot=entrepot
    ).select_related('produit', 'utilisateur').order_by('-date')[:50]
    
    # Stock par produit dans cet entrepôt
    stock_produits = MouvementStock.objects.filter(
        entrepot=entrepot
    ).values(
        'produit__code',
        'produit__nom'
    ).annotate(
        quantite_totale=Sum('quantite')
    ).filter(
        quantite_totale__gt=0  # Seulement les produits en stock
    ).order_by('-quantite_totale')
    
    contexte = {
        'entrepot': entrepot,
        'mouvements': mouvements,
        'stock_produits': stock_produits,
    }
    
    return render(request, 'stock/details_entrepot.jinja', contexte)

@login_required
def supprimer_entrepot(request, pk):
    """Vue pour supprimer (désactiver) un entrepôt"""
    try:
        entrepot = get_object_or_404(Entrepot, pk=pk)
        
        if request.method == 'POST':
            # Vérifier si l'entrepôt a du stock
            stock_present = MouvementStock.objects.filter(
                entrepot=entrepot
            ).aggregate(
                total=Sum('quantite')
            )['total'] or 0
            
            # Vérifier s'il y a des mouvements récents (moins de 30 jours)
            from datetime import datetime, timedelta
            date_limite = datetime.now() - timedelta(days=30)
            mouvements_recents = MouvementStock.objects.filter(
                entrepot=entrepot,
                date__gte=date_limite
            ).count()
            
            if stock_present > 0:
                messages.warning(request, f'Impossible de supprimer cet entrepôt. Il contient encore du stock ({stock_present} unités au total).')
                return redirect('stock:details_entrepot', pk=pk)
            elif mouvements_recents > 0:
                messages.warning(request, f'Cet entrepôt a {mouvements_recents} mouvement(s) récent(s). Êtes-vous sûr de vouloir le désactiver ?')
                # On continue quand même la désactivation
            
            # Désactiver l'entrepôt plutôt que de le supprimer
            nom_entrepot = entrepot.nom
            entrepot.est_actif = False
            entrepot.save()
            messages.success(request, f'Entrepôt "{nom_entrepot}" désactivé avec succès!')
            return redirect('stock:liste_entrepots')
        
        # Récupérer les informations pour la confirmation
        # Stock par produit dans cet entrepôt
        stock_produits = MouvementStock.objects.filter(
            entrepot=entrepot
        ).values(
            'produit__code',
            'produit__nom',
            'produit__pk'
        ).annotate(
            quantite_totale=Sum('quantite')
        ).filter(
            quantite_totale__gt=0
        ).order_by('-quantite_totale')[:10]
        
        # Total du stock
        stock_total = MouvementStock.objects.filter(
            entrepot=entrepot
        ).aggregate(
            total=Sum('quantite')
        )['total'] or 0
        
        # Nombre de produits différents
        nombre_produits = MouvementStock.objects.filter(
            entrepot=entrepot
        ).values('produit').distinct().count()
        
        # Nombre total de mouvements
        total_mouvements = MouvementStock.objects.filter(
            entrepot=entrepot
        ).count()
        
        # Mouvements récents (30 derniers jours)
        from datetime import datetime, timedelta
        date_limite = datetime.now() - timedelta(days=30)
        mouvements_recents = MouvementStock.objects.filter(
            entrepot=entrepot,
            date__gte=date_limite
        ).count()
        
        contexte = {
            'entrepot': entrepot,
            'stock_produits': stock_produits,
            'stock_total': stock_total,
            'nombre_produits': nombre_produits,
            'total_mouvements': total_mouvements,
            'mouvements_recents': mouvements_recents,
        }
        return render(request, 'stock/confirmer_suppression_entrepot.jinja', contexte)
        
    except Exception as e:
        messages.error(request, f'Erreur lors de la suppression : {str(e)}')
        return redirect('stock:liste_entrepots')



# ========== RAPPORTS ET STATISTIQUES ==========
@login_required
def rapport_stock(request):
    """Vue pour afficher le rapport de stock"""
    # Produits avec leur stock actuel
    produits_stock = Produit.objects.filter(
        est_actif=True
    ).annotate(
        stock_actuel=Sum('mouvementstock__quantite')
    ).order_by('nom')
    
    # Séparer les produits selon leur état de stock
    stock_ok = []
    stock_bas = []
    stock_critique = []
    
    for produit in produits_stock:
        stock = produit.stock_actuel or 0
        
        if stock <= produit.seuil_reapprovisionnement:
            stock_critique.append(produit)
        elif stock <= produit.stock_min:
            stock_bas.append(produit)
        else:
            stock_ok.append(produit)
    
    contexte = {
        'stock_ok': stock_ok,
        'stock_bas': stock_bas,
        'stock_critique': stock_critique,
        'total_produits': produits_stock.count(),
    }
    
    return render(request, 'stock/rapport_stock.jinja', contexte)
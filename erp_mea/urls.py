"""
URL configuration for erp_mea project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from base import views as vues_base


urlpatterns = [
    # Administration Django
    path('admin/', admin.site.urls),

    # Page d'accueil - Tableau de bord
    path('', vues_base.tableau_bord, name='tableau_bord'),

    # Inclure les URLs des différents modules
    path('', include('base.urls')),
    path('stock/', include('stock.urls')),
    path('ventes/', include('ventes.urls')),
    path('achats/', include('achats.urls')),
    path('comptabilite/', include('comptabilite.urls')),
    path('accounts/', include('accounts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# En mode DEBUG, servir les fichiers statiques
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
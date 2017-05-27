from django.conf.urls import *
from django.contrib.auth.urls import *
from .views import AffichageRecettes
from . import views

urlpatterns = [
    url('^ajout', views.ajout_recette, name='ajout'),
    url('^recettes$', AffichageRecettes.as_view(), name='recettes'),
    url('^recettes/(?P<pk>\d+)/$', views.affichage_recette, name='recette'),
    url('^modifier/(?P<pk>\d+)/$', views.modifier_recette, name='modifier_recette'),
]

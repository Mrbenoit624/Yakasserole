from django.conf.urls import *
from django.contrib.auth.urls import *
from .views import AffichageRecettes, AffichageRecette
from . import views

urlpatterns = [
    url('^ajout', views.ajout_recette, name='ajout'),
    url('^recettes$', AffichageRecettes.as_view(), name='recettes'),
    url('^recettes/(?P<pk>\d+)/$', AffichageRecette.as_view(), name='recette'),
    url('^modifier/(?P<pk>\d+)/$', views.modifier_recette, name='modifier_recette'),
]

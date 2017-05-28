from django.conf.urls import *
from django.contrib.auth.urls import *

from .views import AffichageAteliers, AffichageAtelier
from . import views

urlpatterns = [
    url('^ajout$', views.ajout_atelier, name='ajout_atelier'),
    url('^inscription/(?P<atelier_id>\d+)/$', views.inscription_atelier, name='inscription_atelier'),
    url('^desinscription/(?P<atelier_id>\d+)/$', views.desinscription_atelier, name='desinscription_atelier'),
    url('^ateliers$', AffichageAteliers.as_view(), name='ateliers'),
    url('^ateliers/(?P<pk>\d+)/$', views.affichage_atelier, name='atelier'),
    url('^modifier/(?P<pk>\d+)/$', views.modifier_atelier, name='modifier_atelier'),
]

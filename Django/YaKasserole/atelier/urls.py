from django.conf.urls import *
from django.contrib.auth.urls import *

from .views import AffichageAteliers, AffichageAtelier
from . import views

urlpatterns = [
    url('^ajout$', views.ajout_atelier, name='ajout_atelier'),
    url('^inscription$', views.inscription_atelier, name='inscription_atelier'),
    url('^ateliers$', AffichageAteliers.as_view(), name='ateliers'),
    url('^ateliers/(?P<pk>\d+)/$', AffichageAtelier.as_view(), name='atelier'),
]

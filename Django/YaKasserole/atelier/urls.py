from django.conf.urls import *
from django.contrib.auth.urls import *
from .views import AffichageAteliers, AffichageAtelier
from . import views

urlpatterns = [
    url('^ajout$', views.ajout_atelier, name='ajout'),
    url('^inscription$', views.inscription_atelier, name='inscription'),
    url('^ateliers$', AffichageAteliers.as_view(), name='ateliers'),
    url('^ateliers/(?P<pk>\d+)/$', AffichageAtelier.as_view(), name='atelier'),
]

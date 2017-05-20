from django.conf.urls import *
from django.contrib.auth.urls import *
from . import views

urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    url('^ajout', views.ajout_atelier, name='ajout'),
    url('^inscription', views.inscription_atelier, name='inscription'),
]

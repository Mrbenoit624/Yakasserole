from django.conf.urls import *
from django.contrib.auth.urls import *
from . import views

urlpatterns = [
    url('^ajout', views.ajout_recette, name='ajout'),
    url(r'^([a-z-]+)$', views.page, name='page'),
]

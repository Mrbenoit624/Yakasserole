from django.conf.urls import *
from django.contrib.auth.urls import *

from .views import search

urlpatterns = [
    url('^recherche/', search, name='search'),
]

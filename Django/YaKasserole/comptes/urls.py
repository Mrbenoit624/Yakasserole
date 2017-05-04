
from django.conf.urls import *
from django.contrib.auth.urls import *
from . import views

urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    url('^profile', views.profile, name='profile'),
    url(r'^register/$', views.inscription, name='inscription')
    url(r'^account/$', views.profile, name='compte')
]

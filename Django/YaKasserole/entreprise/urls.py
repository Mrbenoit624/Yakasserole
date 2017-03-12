
from django.conf.urls import url
from.import views

urlpatterns = [
    #url(r'^apropos$', views.apropos, name='apropos'),
    #url(r'^location$', views.location, name='location'),
    #url(r'^contact$', views.contact, name='contact'),
    url(r'^([a-z]+)$', views.page, name='page'),
]

from django.conf.urls import url
from . import views

urlpatterns = [
    url('^contact$', views.contact, name='contact'),
    url(r'^([a-z]+)$', views.page, name='page'),
]

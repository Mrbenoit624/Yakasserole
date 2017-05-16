
from django.conf.urls import *
from django.contrib.auth.urls import *
from . import views

urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    url('^profile', views.profile, name='profile'),
    url(r'^register/$', views.inscription, name='inscription'),
    url('^connect/', views.connect, name='connect'),
    url('^login/$', views.connect, name='connect'),
    url('^payments/', include('payments.urls')),
    url('^payments$', views.payment_details, name='payment_details'),
]

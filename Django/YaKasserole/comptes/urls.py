
from django.conf.urls import *
from django.contrib.auth.urls import *
from . import views
from . views import *

urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    url('^profile/$', views.profile, name='profile'),
    url('^profile/(?P<user_id>\d+)/$', views.public_profile, name='public_profile'),
    url(r'^register/$', views.inscription, name='inscription'),
    url('^connect/', views.connect, name='connect'),
    url('^login/$', views.connect, name='connect'),
    url('^payments/', include('payments.urls')),
    url('^detail_payments/(?P<payment_id>.*)/$', views.payment_details, name='payment_details'),
#    url('^payments$', views.payment, name='payment'),
    url('^payments$', Listpayments.as_view(), name='payment'),
    url('^payment_process/(?P<process_id>\d+)/$', views.payment_process, name='payment_process'),
    url('^devenir_premium$', views.devenir_premium, name='devenir_premium'),
]

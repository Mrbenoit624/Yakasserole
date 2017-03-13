
from django.conf.urls import url
from.import views

urlpatterns = [
    url(r'^([a-z]+)$', views.page, name='page'),
]

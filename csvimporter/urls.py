from django.conf.urls.defaults import *
from core.models import Customer, Product, Sale

urlpatterns = patterns('csvimporter.views',
    url(r'^customer/$', 'new', kwargs={'model': Customer}, name='new-csv'),
    url(r'^product/$', 'new', kwargs={'model': Product}, name='new-csv'),
    url(r'^sale/$', 'new', kwargs={'model': Sale}, name='new-csv'),
    url(r'^(?P<object_id>\d+)/(?P<modelname>[\w\d-]+)/$', 'associate', name='associate-csv'),
)

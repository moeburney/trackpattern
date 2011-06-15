from django.conf.urls.defaults import *
from core.models import Customer

urlpatterns = patterns('tracklist.csvimporter.views',
    url(r'^customer/$', 'new', kwargs={'model':Customer}, name='new-csv'),
    url(r'^product/$', 'new', name='new-csv'),
    url(r'^sale/$', 'new', name='new-csv'),
    url(r'^(?P<object_id>\d+)/$', 'associate', name='associate-csv'),
)

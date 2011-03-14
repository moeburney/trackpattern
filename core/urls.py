from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('tracklist.core.views',
    (r'^customer/add/$', 'add_customer'),
    (r'^customer/edit/(?P<id>.*)/$', 'edit_customer'),
)

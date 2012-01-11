from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()


urlpatterns = patterns('landing.views',
    (r'^$', 'landing'),
    (r'^stylesheets/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': '/landing/stylesheets'}),
    (r'^images/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': '/landing/images'}),
    (r'^javascripts/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': '/'}),
)

from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()


urlpatterns = patterns('tracklist.home.views',
    (r'^$', 'home'),
    (r'^settings/$', 'settings'),
    (r'^search/$', 'search'),
    (r'^faq/$', 'faq'),
    (r'^reports/$', 'reports')
)

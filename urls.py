from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    (r'^static/(?P<path>.*)/$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^admin/', include(admin.site.urls)),
                       
    (r'^home/', include('tracklist.home.urls')),
    (r'^$', redirect_to, {'url': '/home/'}),
    (r'^core/', include('tracklist.core.urls')),
                       
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'django.contrib.auth.views.logout'),
    (r'^forgot_password/$', 'tracklist.home.views.forgot_password'),
    (r'^signup/$', 'tracklist.home.views.signup'),

)

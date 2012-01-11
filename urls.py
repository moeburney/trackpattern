from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to
from django.views.generic.simple import direct_to_template
from home.views import tlogin

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()
urlpatterns = patterns('',
    (r'^static/(?P<path>.*)/$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    (r'^admin/', include(admin.site.urls)),
    (r'^home/', include('home.urls')),
    (r'^$', redirect_to, {'url': '/home/'}),
    (r'^core/', include('core.urls')),
    (r'^landing/', direct_to_template, {'template': settings.MEDIA_ROOT + '/landing/index.html'}),
    (r'^index-2/', direct_to_template, {'template': settings.MEDIA_ROOT + '/landing/index-2.html'}),
    (r'^about/', direct_to_template, {'template': settings.MEDIA_ROOT + '/landing/about.html'}),
    (r'^pricing/', direct_to_template, {'template': settings.MEDIA_ROOT + '/landing/pricing.html'}),
    (r'^blog/', direct_to_template, {'template': settings.MEDIA_ROOT + '/landing/blog.html'}),
    (r'^contact/', direct_to_template, {'template': settings.MEDIA_ROOT + '/landing/contact.html'}),

    (r'^login/$', tlogin),
    #(r'^login/$', login),
    (r'^logout/$', 'django.contrib.auth.views.logout'),
    (r'^forgot_password/$', 'home.views.forgot_password'),
    (r'^signup/$', 'home.views.signup'),
    (r'^signup_success/$', 'home.views.signup_success'),
    url(r'^groups/(?P<name>.+)/$', 'groups.views.detail', {}, name='group_detail'),

)

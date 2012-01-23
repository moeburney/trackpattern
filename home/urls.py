from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()


urlpatterns = patterns('home.views',
    (r'^$', 'home'),
    (r'^settings/$', 'settings'),
    (r'^search/$', 'search'),
    (r'^faq/$', 'faq'),
    (r'^stats_rev/$', 'reports')
    (r'^stats_pur/$', 'reports')
    (r'^stats_bottom_30/$', 'reports')
    (r'^stats_no_purchase_3_months/$', 'reports')
    (r'^stats_monthly_growth/$', 'reports')
)

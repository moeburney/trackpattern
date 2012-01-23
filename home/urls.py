from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()


urlpatterns = patterns('home.views',
    (r'^$', 'home'),
    (r'^settings/$', 'settingss'),
    (r'^search/$', 'search'),
    (r'^faq/$', 'faq'),
    (r'^stats_rev/$', 'stats_rev'),
    (r'^stats_pur/$', 'stats_pur'),
    (r'^stats_bottom_30/$', 'stats_bottom_30'),
    (r'^stats_no_purchase_3_months/$', 'stats_no_purchase_3_months'),
    (r'^stats_monthly_growth/$', 'stats_monthly_growth')
)

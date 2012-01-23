from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('core.views',
    (r'^customer/$', 'customer_home'),
    (r'^customer/view/(?P<id>.*)/$', 'customer_view'),
    (r'^customer/add/$', 'add_customer'),
    (r'^customer/edit/(?P<id>.*)/$', 'edit_customer'),
    (r'^customer/delete/(?P<id>.*)/$', 'delete_customer'),

    (r'^category/$', 'category_home'),
    (r'^category/view/(?P<id>.*)/$', 'category_view'),
    (r'^category/add/$', 'add_category'),
    (r'^category/edit/(?P<id>.*)/$', 'edit_category'),

    (r'^product/$', 'product_home'),
    (r'^product/view/(?P<id>.*)/$', 'product_view'),
    (r'^product/add/$', 'add_product'),
    (r'^product/edit/(?P<id>.*)/$', 'edit_product'),
    (r'^product/delete/(?P<id>.*)/$', 'delete_product'),

    (r'^sale/$', 'sale_home'),
    (r'^sale/view/(?P<id>.*)/$', 'sale_view'),
    (r'^sale/add/$', 'add_sale'),
    (r'^sale/random/$', 'add_random_sales'),
    (r'^sale/edit/(?P<id>.*)/$', 'edit_sale'),
    (r'^sale/delete/(?P<id>.*)/$', 'delete_sale'),

    (r'^campaign/$', 'campaign_home'),
    (r'^campaign/view/(?P<id>.*)/$', 'campaign_view'),
    (r'^campaign/add/$', 'add_campaign'),
    (r'^campaign/edit/(?P<id>.*)/$', 'edit_campaign'),
    (r'^campaign/delete/(?P<id>.*)/$', 'delete_campaign'),

    (r'^group/$', 'group_home'),
    (r'^group/view/(?P<id>.*)/$', 'group_view'),
    (r'^csv/', include('csvimporter.urls')),

)

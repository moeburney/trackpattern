from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('tracklist.core.views',
    (r'^customer/$', 'customer_home'),
    (r'^customer/view/(?P<id>.*)/$', 'customer_view'),
    (r'^customer/add/$', 'add_customer'),
    (r'^customer/edit/(?P<id>.*)/$', 'edit_customer'),

    (r'^category/$', 'category_home'),
    (r'^category/view/(?P<id>.*)/$', 'category_view'),
    (r'^category/add/$', 'add_category'),
    (r'^category/edit/(?P<id>.*)/$', 'edit_category'),

    (r'^product/$', 'product_home'),
    (r'^product/view/(?P<id>.*)/$', 'product_view'),
    (r'^product/add/$', 'add_product'),
    (r'^product/edit/(?P<id>.*)/$', 'edit_product'),

    (r'^purchase/$', 'purchase_home'),
    (r'^purchase/view/(?P<id>.*)/$', 'purchase_view'),
    (r'^purchase/add/$', 'add_purchase'),
    (r'^purchase/edit/(?P<id>.*)/$', 'edit_purchase'),

    (r'^group/$', 'group_home'),
    (r'^group/view/(?P<id>.*)/$', 'group_view'),

)

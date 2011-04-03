import operator

from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.conf import settings
from django.db.models import Count, Avg, Max
from core.models import Customer, Category, Product, Purchase

@login_required
def home(request):
    """
    renders dashboard.
    """
    
    return render_to_response('home/home.html',
                              {'stats': calculate_stats(request.user)},
                              context_instance=RequestContext(request))
def calculate_stats(user):
    # 1. most popular product
    popular_products = Product.objects.filter(user=user) \
                       .annotate(bought=Count('purchase')) \
                       .order_by('-bought')
        
    # 2. repeat customers percent
    total_customers = Customer.objects.filter(user=user)
    repeat_customers = Customer.objects.filter(user=user) \
                       .annotate(bought=Count('purchase')) \
                       .filter(bought__gte=2)
    
    # 3. repeat customers mostly bought x first, and then y
    repeat_buyers = Customer.objects.filter(user=user) \
                   .annotate(bought=Count('purchase')) \
                   .filter(bought__gte=2)
    # identify top repeat buyer, could be more than one buyer
    top_repeat_buyers = []
    for buyer in repeat_buyers:
        if not top_repeat_buyers:
            top_repeat_buyers.append(buyer)
        else:
            if buyer.bought == top_repeat_buyers[-1].bought:
                top_repeat_buyers.append(buyer)
            else:
                break
    repeat_buyers_purchases = Purchase.objects.filter(customer__in=[x.pk for x in top_repeat_buyers]) \
                             .order_by('customer','transaction_date')
    buyer_product_order= {}
    for p in repeat_buyers_purchases:
        if not p.customer in buyer_product_order:
            buyer_product_order[p.customer] = []
        buyer_product_order[p.customer].append(p.product)
    product_purchase_pattern = {}
    for buyer, products in buyer_product_order.iteritems():
        pattern = ', '.join(p.name for p in products)
        if not pattern in product_purchase_pattern:
            product_purchase_pattern[pattern] = 1
        else:
            product_purchase_pattern[pattern] = product_purchase_pattern[pattern] + 1
    # now we have purchase patterns & no of occurances of those pattern
    # { 'x,y': 1, 'y,x': 4, 'x,z': 2 }
    # let's sort them on pattern frequency, and identify top one. multiple also possible
    sorted_patterns_by_freq = sorted(product_purchase_pattern.iteritems(), reverse=True, key=operator.itemgetter(1))
    stats = {}
    stats['popular_products'] = popular_products
    stats['top_purchase_patterns'] = sorted_patterns_by_freq
    print sorted_patterns_by_freq
    if total_customers.count(): # avoid divide by 0 error
        stats['repeat_customer_percent'] = (repeat_customers.count() * 100)/total_customers.count()
    else:
        stats['repeat_customer_percent'] = 0
    return stats

@login_required
def search(request):
    """
    search for given name in categories, customer, product etc.
    """
    word = request.POST.get('word','')

    categories = Category.objects.filter(name__icontains=word)
    customers = Customer.objects.filter(first_name__icontains=word)
    products = Product.objects.filter(name__icontains=word)
    
    return render_to_response('home/search_result.html',
                              {'word': word,
                               'categories': categories,
                               'customers': customers,
                               'products': products,},
                              context_instance=RequestContext(request))


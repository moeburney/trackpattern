import operator

from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.conf import settings
from django.db.models import Count, Avg, Max
from core.models import Customer, Category, Product, Sale
from home.forms import PersonalForm

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
                       .annotate(bought=Count('sale')) \
                       .order_by('-bought')
        
    # 2. repeat customers percent
    total_customers = Customer.objects.filter(user=user)
    repeat_customers = Customer.objects.filter(user=user) \
                       .annotate(bought=Count('sale')) \
                       .filter(bought__gte=2)
    
    # 3. repeat customers mostly bought x first, and then y
    repeat_buyers = Customer.objects.filter(user=user) \
                   .annotate(bought=Count('sale')) \
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
    repeat_buyers_sales = Sale.objects.filter(customer__in=[x.pk for x in top_repeat_buyers]) \
                             .order_by('customer','transaction_date')
    buyer_product_order= {}
    for p in repeat_buyers_sales:
        if not p.customer in buyer_product_order:
            buyer_product_order[p.customer] = []
        buyer_product_order[p.customer].append(p.product)
    product_sale_pattern = {}
    for buyer, products in buyer_product_order.iteritems():
        pattern = ', '.join(p.name for p in products)
        if not pattern in product_sale_pattern:
            product_sale_pattern[pattern] = 1
        else:
            product_sale_pattern[pattern] = product_sale_pattern[pattern] + 1
    # now we have sale patterns & no of occurances of those pattern
    # { 'x,y': 1, 'y,x': 4, 'x,z': 2 }
    # let's sort them on pattern frequency, and identify top one. multiple also possible
    sorted_patterns_by_freq = sorted(product_sale_pattern.iteritems(), reverse=True, key=operator.itemgetter(1))
    stats = {}
    stats['popular_products'] = popular_products
    stats['top_sale_patterns'] = sorted_patterns_by_freq
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

def forgot_password(request):
    """
    resets user password and sends mail with new password
    """
    reset = False
    username = request.POST.get('username', None)
    if username:
        try:
            user = User.objects.get(username=username)
            import random
            import string
            new_password = ''.join(random.choice(string.letters + string.digits) for i in xrange(8))
            user.set_password(new_password)
            user.save()
            # send a mail with new password
            from django.template.loader import render_to_string
            from django.core.mail import EmailMessage
            email = EmailMessage('Tracklist: Password reset instructions',
                                 render_to_string('registration/password_reset_mail.txt',
                                                  {'password': new_password, 
                                                   'username': user.username,
                                                   }),
                                 from_email=['accounts@tracklist.com'],
                                 to=[user.email])
            email.send()
            reset = True
        except:
            pass
    return render_to_response('registration/forgot_password.html',
                              {'reset': reset,},
                              context_instance=RequestContext(request))

@login_required
def settings(request):
    """
    User settings page
    """
    if request.method == 'POST':
        form = PersonalForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            if "change_password" in form.cleaned_data:
                change_password = form.cleaned_data['change_password']
                if change_password:
                    user.set_password(change_password)
            user.save()
            return HttpResponseRedirect("/home/")
    return render_to_response('home/settings.html',
                              {'form': PersonalForm(instance=request.user),},
                              context_instance=RequestContext(request))

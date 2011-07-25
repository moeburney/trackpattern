import operator

import datetime

from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.conf import settings
from django.db.models import Count, Avg, Max
from core.models import Customer, Category, Product, Sale, Activity, Campaign, Group, UserProfile
from home.forms import PersonalForm
from django.utils.safestring import SafeString





@login_required
def home(request):
    """
    renders dashboard.
    """
    activities = Activity.objects.filter(user=request.user)


    return render_to_response('home/home.html',
                              {'activities': activities,
                              'charts': calculate_charts(request.user),
                              'stats': calculate_stats(request.user)},
                              context_instance=RequestContext(request))


#for chart calculations
def calculate_charts(user):
    # sales per campaign

    month_translate =  {1 : 'jan',
    2 : 'feb',
    3 : 'mar',
    4 : 'apr',
    5 : 'may',
    6 : 'jun',
    7 : 'jul',
    8 : 'aug',
    9 : 'sep',
    10 : 'oct',
    11 : 'nov',
    12 : 'dec',
    }

    total_profit_monthly_names = []
    total_profit_monthly_values = []

    top_3_popular_products = Product.objects.filter(user=user) \
            .annotate(bought=Count('sale')) \
            .order_by('-bought')[:3]


    monthly_sales_of_product = [[],[],[]]
    name_product = [[],[],[]]

    x = 0
    for product in top_3_popular_products:
        name_product[x] = product.name
        x += 1
    x = 0


    month = datetime.datetime.now().month
    year = datetime.datetime.now().year
    i = 0
    while i < 12:
        salez = Sale.objects.filter(user=user, transaction_date__year=str(year), transaction_date__month=str(month))
        total_profit_monthly_names.append(month_translate[month])
        profits = []
        profits = [int(sale.price) for sale in salez]
        total_profit_monthly_values.append(sum(profits))

        x = 0
        for product in top_3_popular_products:
            monthly_sales_of_product[x].append(int(product.turnover_generated_in_month(month)))
            x += 1



        i += 1
        if month != 1:
            month = month - 1
        else:
            year = year - 1
            month = 12

    for sale in salez:
        campaign_values.append(sale.campaign_count)
        campaign_names.append("%% " + str(sale.marketing_source.campaign_name))

    campaignz = Campaign.objects.filter(user=user)

    campaign_values = []
    campaign_names = []

    for campaign in campaignz:
        campaign_values.append(campaign.total_sales())
        campaign_names.append("%% " + str(campaign.campaign_name))


    group_values = []
    group_names = []

    g = Group(user)
    for id in xrange(1, 3):
        group_values.append(int(g.get_group(id)['total_turnover']))
        group_names.append("%% " + str(g.get_group(id)['name']))



    charts = {}
    if sum(campaign_values) == 0:
        charts['campaign_values'] = 0
    else:
        charts['campaign_values'] = campaign_values
    charts['campaign_names'] = SafeString(campaign_names)
    total_profit_monthly_names.reverse()
    total_profit_monthly_values.reverse()

    if sum(total_profit_monthly_values) == 0:
        charts['total_monthly_profit_values'] = 0 
    else:
        charts['total_monthly_profit_values'] = SafeString(total_profit_monthly_values)
    charts['total_monthly_profit_names'] = SafeString(total_profit_monthly_names)

    if sum(group_values) == 0:
        charts['group_values'] = 0 
    else:
        charts['group_values'] = group_values
    charts['group_names'] = SafeString(group_names)



    monthly_sales_of_product[0].reverse()
    monthly_sales_of_product[1].reverse()
    monthly_sales_of_product[2].reverse()
    
    if (sum(monthly_sales_of_product[0]) + sum(monthly_sales_of_product[1]) + sum(monthly_sales_of_product[2])) == 0:
        charts['monthly_sales_all_products'] = 0

    if name_product[0]:
        charts['name_product_one'] = SafeString(name_product[0])
    else:
        charts['name_product_one'] = ""
    if name_product[1]:
        charts['name_product_two'] = SafeString(name_product[1])
    else:
        charts['name_product_two'] = ""
    if name_product[2]:
        charts['name_product_three'] = SafeString(name_product[2])
    else:
        charts['name_product_three'] = ""

    charts['monthly_sales_product_one'] = SafeString(monthly_sales_of_product[0])
    charts['monthly_sales_product_two'] = SafeString(monthly_sales_of_product[1])
    charts['monthly_sales_product_three'] = SafeString(monthly_sales_of_product[2])


    return charts



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

    categories = Category.objects.filter(user=request.user, name__icontains=word)
    customers = Customer.objects.filter(user=request.user, full_name__icontains=word)
    products = Product.objects.filter(user=request.user, name__icontains=word)
    
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
            email = EmailMessage('Trackpattern: Password reset instructions',
                                 render_to_string('registration/password_reset_mail.txt',
                                                  {'password': new_password, 
                                                   'username': user.username,
                                                   }),
                                 from_email='accounts@tracklist.com',
                                 to=[user.email])
            email.send()
            reset = True
        except:
            pass
    return render_to_response('registration/forgot_password.html',
                              {'reset': reset,},
                              context_instance=RequestContext(request))

def signup(request):
    from forms import SignupForm
    if request.method == 'POST':
        # process signup form and create account
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User()
            user.username = form.cleaned_data['username']
            user.set_password(form.cleaned_data['password1'])
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.is_active=True
            user.save()

            profile = UserProfile(paid_user=False, user=user)
            profile.save()

            if user.username.startswith('test2011'):
                return redirect('https://marketlocomotion.chargify.com/h/46211/subscriptions/new/?first_name=%s&last_name=%s&email=%s' % (user.first_name, user.last_name, user.email))
            else:
                login_user = authenticate(username=user.username, password=form.cleaned_data['password1'])
                login(request, login_user)
                return redirect('/home/')

    else:
        form = SignupForm()
    return render_to_response('registration/signup.html',
                       {'form': form,},
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

@login_required
def faq(request):
    """
    faq page
    """
    return render_to_response('faq/faq.html',
                              {},
                              context_instance=RequestContext(request))

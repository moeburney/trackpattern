import logging
import operator

import datetime
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models.aggregates import Sum

from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, get_user
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.conf import settings
from django.db.models import Count, Avg, Max
from core.models import Customer, Category, Product, Sale, Activity, Campaign, Group, UserProfile
from home.forms import PersonalForm
from django.utils.safestring import SafeString
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.sites.models import get_current_site
import urlparse

logger = logging.getLogger("applog")
month_translate = {1: 'jan',
                   2: 'feb',
                   3: 'mar',
                   4: 'apr',
                   5: 'may',
                   6: 'jun',
                   7: 'jul',
                   8: 'aug',
                   9: 'sep',
                   10: 'oct',
                   11: 'nov',
                   12: 'dec',
                   }

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

@login_required
def stats_rev(request):
    temp = top_20_customers(request.user,"revenue")
    page = int(request.GET.get('page', '1'))
    duration = str(request.GET.get('dur','none'))
    if duration=='none' or duration == 'l1m':
        try:
            paginator = Paginator(temp['cust_one_month'], settings.DEFAULT_PAGESIZE)
            data = paginator.page(page)
        except (EmptyPage, InvalidPage):
        # if the supplied page number is beyond the scope
        # show last page
            data = paginator.page(paginator.num_pages)
    if duration=='l3m':
            try:
                paginator = Paginator(temp['cust_three_month'], settings.DEFAULT_PAGESIZE)
                data = paginator.page(page)
            except (EmptyPage, InvalidPage):
            # if the supplied page number is beyond the scope
            # show last page
                data = paginator.page(paginator.num_pages)
    if duration=='l12m':
            try:
                paginator = Paginator(temp['cust_one_year'], settings.DEFAULT_PAGESIZE)
                data = paginator.page(page)
            except (EmptyPage, InvalidPage):
            # if the supplied page number is beyond the scope
            # show last page
                data = paginator.page(paginator.num_pages)


    return render_to_response('home/stats_rev.html',
            {'stats_rev':data,
             'dur':duration
        },
        context_instance=RequestContext(request))
@login_required
def stats_pur(request):
    temp = top_20_customers(request.user,"purchases")
    page = int(request.GET.get('page', '1'))
    duration = str(request.GET.get('dur','l1m'))
    if duration == 'l1m':
        try:
            paginator = Paginator(temp['cust_one_month'], settings.DEFAULT_PAGESIZE)
            data = paginator.page(page)
        except (EmptyPage, InvalidPage):
        # if the supplied page number is beyond the scope
        # show last page
            data = paginator.page(paginator.num_pages)
    if duration=='l3m':
        try:
            paginator = Paginator(temp['cust_three_month'], settings.DEFAULT_PAGESIZE)
            data = paginator.page(page)
        except (EmptyPage, InvalidPage):
        # if the supplied page number is beyond the scope
        # show last page
            data = paginator.page(paginator.num_pages)
    if duration=='l12m':
        try:
            paginator = Paginator(temp['cust_one_year'], settings.DEFAULT_PAGESIZE)
            data = paginator.page(page)
        except (EmptyPage, InvalidPage):
        # if the supplied page number is beyond the scope
        # show last page
            data = paginator.page(paginator.num_pages)


    return render_to_response('home/stats_pur.html',
            {'stats_pur':data,
             'dur':duration
        },
        context_instance=RequestContext(request))
@login_required
def stats_bottom_30(request):
    temp = bottom_30_customers(request.user,"revenue")
    page = int(request.GET.get('page', '1'))
    try:
        paginator = Paginator(temp, settings.DEFAULT_PAGESIZE)
        data = paginator.page(page)
    except (EmptyPage, InvalidPage):
    # if the supplied page number is beyond the scope
    # show last page
        data = paginator.page(paginator.num_pages)


    return render_to_response('home/stats_bottom_30.html',
            {
             'stats_bottom_30':data
        },
        context_instance=RequestContext(request))
@login_required
def stats_no_purchase_3_months(request):
    temp = no_purchase_x_months(request.user,3)
    page = int(request.GET.get('page', '1'))
    try:
        paginator = Paginator(temp, settings.DEFAULT_PAGESIZE)
        data = paginator.page(page)
    except (EmptyPage, InvalidPage):
    # if the supplied page number is beyond the scope
    # show last page
        data = paginator.page(paginator.num_pages)


    return render_to_response('home/stats_no_purchase_3_months.html',
            {
             'stats_no_purchase_3_months':data
        },
        context_instance=RequestContext(request))
@login_required
def stats_monthly_growth(request):
    temp = monthly_growth(request.user)
    page = int(request.GET.get('page', '1'))
    try:
        paginator = Paginator(temp, settings.DEFAULT_PAGESIZE)
        data = paginator.page(page)
    except (EmptyPage, InvalidPage):
    # if the supplied page number is beyond the scope
    # show last page
        data = paginator.page(paginator.num_pages)


    return render_to_response('home/stats_monthly_growth.html',
            {
             'stats_monthly_growth' : data
        },
        context_instance=RequestContext(request))

#for chart calculations
def calculate_charts(user):
    # sales per campaign


    total_profit_monthly_names = []
    total_profit_monthly_values = []

    top_3_popular_products = Product.objects.filter(user=user)\
                             .annotate(bought=Count('sale'))\
                             .order_by('-bought')[:3]

    monthly_sales_of_product = [[], [], []]
    name_product = [[], [], []]

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
    campaignz = Campaign.objects.filter(user=user)

    campaign_values = []
    campaign_names = []

    for sale in salez:
        campaign_values.append(sale.marketing_source.total_sales())
        campaign_names.append("%% " + str(sale.marketing_source.campaign_name))


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
    total_growth_monthly_names = []
    total_growth_monthly_values = []
    total_map = dict()
    monthh = datetime.datetime.now().month
    yearr = datetime.datetime.now().year
    # try using timedelta and excludes on dates below.  ## TODO try to figure out the django ORM way to do below sales query
    i = 0
    total_customer_count = Customer.objects.filter(user=user).count()
    while i < 12:

        sales = Customer.objects.filter(user=user, sale__transaction_date__year=str(yearr), sale__transaction_date__month=str(monthh)).annotate(bought=Count('sale')).filter(bought__gte=1)
        #sales = Customer.objects.raw('Select * from ')
        logger.info("\n #### monthly %s %d\n" %(month_translate[monthh],yearr))
        logger.info(sales)
        total_growth_monthly_names.append(month_translate[monthh])
        growth = 0
        if sales.count()>0:
            growth = float(sales.count()/total_customer_count)
        if growth<1.0:
            total_growth_monthly_values.append(sales.count())
            total_map[month_translate[monthh]] = (sales.count(),False)

        if growth>1.0:
            total_growth_monthly_values.append(growth)
            total_map[month_translate[monthh]] = (growth,True)

        i += 1
        if monthh != 1:
            monthh -= 1
        else:
            yearr -= 1
            monthh = 12
    charts['total_growth_monthly_values'] = SafeString(total_growth_monthly_values)
    charts['total_growth_monthly_names'] = SafeString(total_growth_monthly_names)
    charts['total_growth_map'] = total_map
    logger.info(charts)
    return charts


def calculate_stats(user):
    # 1. most popular product
    popular_products = Product.objects.filter(user=user)\
    .annotate(bought=Count('sale'))\
    .order_by('-bought')

    # 2. repeat customers percent
    total_customers = Customer.objects.filter(user=user)
    repeat_customers = Customer.objects.filter(user=user)\
    .annotate(bought=Count('sale'))\
    .filter(bought__gte=2)

    # 3. repeat customers mostly bought x first, and then y
    repeat_buyers = Customer.objects.filter(user=user)\
    .annotate(bought=Count('sale'))\
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
    repeat_buyers_sales = Sale.objects.filter(customer__in=[x.pk for x in top_repeat_buyers])\
    .order_by('customer', 'transaction_date')
    buyer_product_order = {}
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
        stats['repeat_customer_percent'] = (repeat_customers.count() * 100) / total_customers.count()
    else:
        stats['repeat_customer_percent'] = 0
    return stats

def monthly_growth(user):
    charts = {}
    total_growth_monthly_names = []
    total_growth_monthly_values = []
    total_map = dict()
    monthh = datetime.datetime.now().month
    yearr = datetime.datetime.now().year
    # try using timedelta and excludes on dates below.  ## TODO try to figure out the django ORM way to do below sales query
    i = 0
    total_customer_count = Customer.objects.filter(user=user).count()
    while i < 12:

        sales = Customer.objects.filter(user=user, sale__transaction_date__year=str(yearr), sale__transaction_date__month=str(monthh)).annotate(bought=Count('sale')).filter(bought__gte=1)
        #sales = Customer.objects.raw('Select * from ')
        logger.info("\n #### monthly %s %d\n" %(month_translate[monthh],yearr))
        logger.info(sales)
        total_growth_monthly_names.append(month_translate[monthh])
        growth = float(sales.count()/total_customer_count)
        if growth<1.0:
            total_growth_monthly_values.append(sales.count())
            total_map[month_translate[monthh]] = (sales.count(),False)

        if growth>1.0:
            total_growth_monthly_values.append(growth)
            total_map[month_translate[monthh]] = (growth,True)

        i += 1
        if monthh != 1:
            monthh -= 1
        else:
            yearr -= 1
            monthh = 12
    charts['total_growth_monthly_values'] = SafeString(total_growth_monthly_values)
    charts['total_growth_monthly_names'] = SafeString(total_growth_monthly_names)
    charts['total_growth_map'] = total_map
    logger.info(charts)
    return charts['total_growth_map'].items()

@login_required
def search(request):
    """
    search for given name in categories, customer, product etc.
    """
    word = request.POST.get('word', '')

    categories = Category.objects.filter(user=request.user, name__icontains=word)
    customers = Customer.objects.filter(user=request.user, full_name__icontains=word)
    products = Product.objects.filter(user=request.user, name__icontains=word)

    return render_to_response('home/search_result.html',
            {'word': word,
             'categories': categories,
             'customers': customers,
             'products': products, },
        context_instance=RequestContext(request))

def top_20_customers(user,by):
    stat = {}
    #    total_customer_count = Customer.objects.filter(user=user).count()
    #    twenty_percent = int(total_customer_count*0.20)
    today = datetime.date.today()
    back_one_month = today - datetime.timedelta(days=31)
    back_three_months = today - datetime.timedelta(days=91)
    back_one_year = today - datetime.timedelta(days=365)
    if by in "revenue":
        cust_one_month = Customer.objects.filter(user=user,sale__transaction_date__range=(back_one_month,today)).annotate(tot_rev=Sum('sale__price')).order_by( '-tot_rev' )
        cust_three_month = Customer.objects.filter(user=user,sale__transaction_date__range=(back_three_months,today)).annotate(tot_rev=Sum('sale__price')).order_by( '-tot_rev' )
        cust_one_year = Customer.objects.filter(user=user,sale__transaction_date__range=(back_one_year,today)).annotate(tot_rev=Sum('sale__price')).order_by( '-tot_rev' )
        logger.info("\n\n $$$ raw-revenue \n\n")
        logger.info(cust_one_month)
        logger.info(cust_three_month)
        logger.info(cust_one_year)
        stat['cust_one_month'] = cust_one_month[:int(len(cust_one_month)*0.20)]
        stat['cust_three_month'] = cust_three_month[:int(len(cust_three_month)*0.20)] #[:twenty_percent]
        stat['cust_one_year'] = cust_one_year[:int(len(cust_one_year)*0.20)] #[:twenty_percent]
        logger.debug("\n\n $$$ revenue \n\n")
        logger.debug(stat)
    if by in "purchases":
        cust_one_month = Customer.objects.filter(user=user,sale__transaction_date__range=(back_one_month,today)).annotate(tot_purchase=Count('sale')).order_by( '-tot_purchase' )
        cust_three_month = Customer.objects.filter(user=user,sale__transaction_date__range=(back_three_months,today)).annotate(tot_purchase=Count('sale')).order_by( '-tot_purchase' )
        cust_one_year = Customer.objects.filter(user=user,sale__transaction_date__range=(back_one_year,today)).annotate(tot_purchase=Count('sale')).order_by( '-tot_purchase' )
        logger.info("\n\n $$$ raw-purchase \n\n")
        logger.info(cust_one_month)
        logger.info(cust_three_month)
        logger.info(cust_one_year)
        stat['cust_one_month'] = cust_one_month[:int(len(cust_one_month)*0.20)]
        stat['cust_three_month'] = cust_three_month[:int(len(cust_three_month)*0.20)] #[:twenty_percent]
        stat['cust_one_year'] = cust_one_year[:int(len(cust_one_year)*0.20)] #[:twenty_percent]
        logger.debug("\n\n $$$ purchase \n\n")
        logger.debug(stat)
    return stat
def bottom_30_customers(user,by):
    stat={}
    if by in "revenue":
        c_list = []
        customers = Customer.objects.filter(user=user).annotate(tot_rev=Sum('sale__price')).order_by('tot_rev')
        for item in customers:
            if item.total_turnover_generated() >0.0:
                c_list.append(item)
        bottom_30_count = int(len(c_list) * 0.30)
        stat['bottom_30_cust'] = c_list[:bottom_30_count]
        logger.info("\n\nbottom 30 %%%%%\n")
        logger.info(c_list)
    return stat['bottom_30_cust']


def no_purchase_x_months(user,x):
    stat={}
    today = datetime.date.today()
    back_3_months = today - datetime.timedelta(days=x*30)
    cust = Customer.objects.filter(user=user).exclude(sale__transaction_date__range=(back_3_months,today))
    stat['no_purchase_x_months'] = cust
    logger.info("\n\nNO PURCHASE %d months %%%% \n" %x)
    logger.info(cust)
    return stat['no_purchase_x_months']

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
                from_email='moe@trackpattern.com',
                to=[user.email])
            email.send()
            reset = True
        except:
            pass
    return render_to_response('registration/forgot_password.html',
            {'reset': reset, },
        context_instance=RequestContext(request))

import json
from collections import  OrderedDict
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
            user.is_active = True
            user.save()

            profile = UserProfile(paid_user=True, user=user)
            profile.save()

            # send a mail with registration details
            from django.template.loader import render_to_string
            from django.core.mail import EmailMessage

            email = EmailMessage('Welcome to Trackpattern',
                render_to_string('registration/welcome_mail.txt',
                        {'username': user.username,
                         'first_name': user.first_name}),
                from_email='moe@trackpattern.com',
                to=[user.email])
            email.send()
            _out = {'username':user.username,'email':user.email,'first_name':user.first_name,'last_name':user.last_name,'Would you like to sign up to our mailing list to receive free information about analytics and data driven marketing?' : form.cleaned_data['question_1'],'ts':str(datetime.datetime.now())}
            emailtoadmin = EmailMessage('Trackpattern - New user has registered',body=json.dumps(_out),from_email="moe@trackpattern.com",to=["moe@trackpattern.com",'kanaderohan@gmail.com'])
            emailtoadmin.send()
            #reset = True
#            return redirect(
#                'https://trackpattern.chargify.com/h/46549/subscriptions/new/?reference=%s&first_name=%s&last_name=%s&email=%s' % (
#                    user.id, user.first_name, user.last_name, user.email))

            login_user = authenticate(username=user.username, password=form.cleaned_data['password1'])
            auth_login(request, login_user)
            return redirect('/home/')

    else:
        form = SignupForm(initial={'question_1': True})
    return render_to_response('registration/signup.html',
            {'form': form, },
        context_instance=RequestContext(request))


def signup_success(request):
    user_id = int(request.GET.get('customer_reference', ''))
    this_user = User.objects.filter(id=user_id).get()
    UserProfile.objects.filter(user=this_user).update(paid_user=True)
    return render_to_response('registration/login.html',
            {'first_login': 1},
        context_instance=RequestContext(request))


@login_required
def settingss(request):
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
            {'form': PersonalForm(instance=request.user), },
        context_instance=RequestContext(request))


@login_required
def faq(request):
    """
    faq page
    """
    return render_to_response('faq/faq.html',
            {},
        context_instance=RequestContext(request))


@csrf_protect
@never_cache
def tlogin(request, template_name='registration/login.html',
           redirect_field_name=REDIRECT_FIELD_NAME,
           authentication_form=AuthenticationForm,
           current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.REQUEST.get(redirect_field_name, '')

    if request.method == "POST":
        form = authentication_form(data=request.POST)
        if form.is_valid():
            netloc = urlparse.urlparse(redirect_to)[1]

            # Use default setting if redirect_to is empty
            if not redirect_to:
                redirect_to = '/home'

            # Security check -- don't allow redirection to a different
            # host.
            elif netloc and netloc != request.get_host():
                redirect_to = '/home'

            # redirect to payment form if user is not paid user
            this_user = form.get_user()
            if this_user is not None:
                profile = this_user.profile
                if not profile.paid_user:
                    redirect_to = 'https://trackpattern.chargify.com/h/46549/subscriptions/new/?reference=%s&first_name=%s&last_name=%s&email=%s' % (
                        this_user.id, this_user.first_name, this_user.last_name, this_user.email)

                else:
                    auth_login(request, this_user)

            # If the user is 'None' log in anyway to get error
            else:
                auth_login(request, this_user)

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    request.session.set_test_cookie()

    current_site = get_current_site(request)
    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
        }
    context.update(extra_context or {})
    return render_to_response(template_name, context,
        context_instance=RequestContext(request, current_app=current_app))


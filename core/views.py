from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models import Sum, Avg, Count
from django.conf import settings

from core.models import Customer, Category, Product, Sale, Group, Campaign, Activity
from core.forms import CustomerForm, CategoryForm, ProductForm, SaleForm, CampaignForm

def add_activity(user, activity_string):
    a = Activity(activity_desc = activity_string, user = user)
    a.save()

@login_required
def customer_home(request):
    """
    renders list of customers associated.
    """
    customer_list = Customer.objects.filter(user=request.user)
    
    page = int(request.GET.get('page', '1'))
    sort = request.GET.get('sort','fname')
    if sort:
        if sort == 'fullname':
            customer_list = customer_list.order_by('full_name')
        #if sort == 'fname':
        #    customer_list = customer_list.order_by('first_name')
        #elif sort == 'lname':
        #    customer_list = customer_list.order_by('last_name')
        elif sort == 'cname':
            customer_list = customer_list.order_by('company_name')
        elif sort == 'turnover':
            customer_list = customer_list.annotate(turnover=Sum('sale__price')).order_by('-turnover')
            
    try:
        paginator = Paginator(customer_list, settings.DEFAULT_PAGESIZE)
        customers = paginator.page(page)
    except (EmptyPage, InvalidPage):
        # if the supplied page number is beyond the scope, show last page
        customers = paginator.page(paginator.num_pages)
        
    return render_to_response('core/customer.html',
                              {'customers': customers,
                               'sort': sort,},
                              context_instance=RequestContext(request))

@login_required
def customer_view(request, id):
    """
    renders a specific customer's view.
    note: this is not customers info.
    """
    customer = Customer.objects.get(pk=id)

    #activity_string = "Viewed Customer " + str(customer.first_name) + " " + str(customer.last_name)
    #add_activity(request.user, activity_string)

    return render_to_response('core/customer_view.html',
                              {'customer': customer,},
                              context_instance=RequestContext(request))
    
@login_required
def add_customer(request):
    """
    Creates a Customer instance
    """
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = request.user
            customer.save()

            #activity_string = "Added Customer " + str(customer.first_name) + " " + str(customer.last_name)
            #add_activity(request.user, activity_string)

            return HttpResponseRedirect('/core/customer/')
    else:
        form = CustomerForm()
    return render_to_response('core/manage_customer.html',
                              {'form': form, 'is_new': True},
                              context_instance=RequestContext(request))

def edit_customer(request, id):
    """
    Updates a Customer details
    """
    customer = Customer.objects.get(pk=id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()

            
            #activity_string = "Edited Customer " + str(customer.first_name) + " " + str(customer.last_name)
            #add_activity(request.user, activity_string)


            return HttpResponseRedirect('/core/customer/')
    else:
        form = CustomerForm(instance=customer)
    return render_to_response('core/manage_customer.html',
                              {'form': form, 'is_new': False},
                              context_instance=RequestContext(request))

def delete_customer(request, id):
    """
    Deletes a customer.
    NOTE: Also deletes dependent objects (Purchase)
    """
    customer = Customer.objects.get(pk=id)
    customer.sale_set.all().delete()
    customer.delete()

    
    #activity_string = "Deleted Customer " + str(customer.first_name) + " " + str(customer.last_name)
    #add_activity(request.user, activity_string)


    return HttpResponseRedirect('/core/customer/')


def group_home(request):
    """
    renders list of groups available
    """
    groups = Group(request.user).GROUP_DEFINITIONS
    return render_to_response('core/group.html',
                              {'groups': groups,},
                              context_instance=RequestContext(request))

@login_required
def group_view(request, id):
    """
    renders a specific group's view.
    """
    group = Group(request.user).get_group(id)
    paginator = Paginator(group, settings.DEFAULT_PAGESIZE)
    
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        group = paginator.page(page)
    except (EmptyPage, InvalidPage):
        # if the supplied page number is beyond the scope
        # show last page
        group = paginator.page(paginator.num_pages)
    return render_to_response('core/group_view.html',
                              {'group': group,},
                              context_instance=RequestContext(request))
@login_required
def category_home(request):
    """
    renders list of available categories
    """
    category_list = Category.objects.filter(user=request.user)
    paginator = Paginator(group_list, settings.DEFAULT_PAGESIZE)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        categories = paginator.page(page)
    except (EmptyPage, InvalidPage):
        # if the supplied page number is beyond the scope
        # show last page
        categories = paginator.page(paginator.num_pages)
        
    return render_to_response('core/category.html',
                              {'categories': categories,},
                              context_instance=RequestContext(request))

@login_required
def category_view(request, id):
    """
    renders a specific category's view.
    """
    category = Category.objects.get(pk=id)
    return render_to_response('core/category_view.html',
                              {'category': category,},
                              context_instance=RequestContext(request))

@login_required
def add_category(request):
    """
    Creates a Category instance
    """
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return HttpResponseRedirect('/core/category/')
    else:
        form = CategoryForm()
    return render_to_response('core/manage_category.html',
                              {'form': form},
                              context_instance=RequestContext(request))

def edit_category(request, id):
    """
    Updates a category details
    """
    category = Category.objects.get(pk=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/core/category/')
    else:
        form = CategoryForm(instance=category)
    return render_to_response('core/manage_category.html',
                              {'form': form},
                              context_instance=RequestContext(request))

@login_required
def product_home(request):
    """
    renders list of available products
    """
    product_list = Product.objects.filter(user=request.user)
    
    page = int(request.GET.get('page', '1'))
    sort = request.GET.get('sort','name')
    if sort:
        if sort == 'name':
            product_list = product_list.order_by('name')
        elif sort == 'date':
            product_list = product_list.order_by('date_released')
        elif sort == 'turnover':
            product_list = product_list.annotate(turnover=Sum('sale__price')).order_by('-turnover')
    try:
        paginator = Paginator(product_list, settings.DEFAULT_PAGESIZE)
        products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        # if the supplied page number is beyond the scope
        # show last page
        products = paginator.page(paginator.num_pages)
        
    return render_to_response('core/product.html',
                              {'products': products,
                               'sort': sort,},
                              context_instance=RequestContext(request))

@login_required
def product_view(request, id):
    """
    renders a specific products's view.
    """
    product = Product.objects.get(pk=id)

    
    activity_string = "Viewed Product " + str(product.name)
    add_activity(request.user, activity_string)


    return render_to_response('core/product_view.html',
                              {'product': product,},
                              context_instance=RequestContext(request))

@login_required
def add_product(request):
    """
    Creates a Product instance
    """
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()

            activity_string = "Added Product " + str(product.name)
            add_activity(request.user, activity_string)

            return HttpResponseRedirect('/core/product/')
    else:
        form = ProductForm()
    return render_to_response('core/manage_product.html',
                              {'form': form, 'is_new': True},
                              context_instance=RequestContext(request))

def edit_product(request, id):
    """
    Updates a Product details
    """
    product = Product.objects.get(pk=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()

            activity_string = "Edited Product " + str(product.name)
            add_activity(request.user, activity_string)

            return HttpResponseRedirect('/core/product/')
    else:
        form = ProductForm(instance=product)
    return render_to_response('core/manage_product.html',
                              {'form': form, 'is_new': False},
                              context_instance=RequestContext(request))

def delete_product(request, id):
    """
    Deletes a product.
    Note: Also delete other dependent entries. (Purchase)
    """
    product = Product.objects.get(pk=id)
    product.sale_set.all().delete()
    product.delete()

    activity_string = "Deleted Product " + str(product.name)
    add_activity(request.user, activity_string)
    return HttpResponseRedirect('/core/product/')

@login_required
def sale_home(request):
    """
    renders list of sales
    """
    sale_list = Sale.objects.filter(user=request.user)
    page = int(request.GET.get('page', '1'))
    sort = request.GET.get('sort', 'date')
    if sort:
        if sort == 'fullname':
            sale_list = sale_list.order_by('customer__full_name')
        #if sort == 'fname':
        #    sale_list = sale_list.order_by('customer__first_name')
        #elif sort == 'lname':
        #    sale_list = sale_list.order_by('customer__last_name')
        elif sort == 'date':
            sale_list = sale_list.order_by('-transaction_date')
        elif sort == 'product':
            sale_list = sale_list.order_by('product__name')

    try:
        paginator = Paginator(sale_list, settings.DEFAULT_PAGESIZE)
        sales = paginator.page(page)
    except (EmptyPage, InvalidPage):
        # if the supplied page number is beyond the scope
        # show last page
        sales = paginator.page(paginator.num_pages)
        
    return render_to_response('core/sale.html',
                              {'sales': sales,
                               'sort': sort,},
                              context_instance=RequestContext(request))

@login_required
def sale_view(request, id):
    """
    renders a specific sale view.
    """
    sale = Sale.objects.get(pk=id)
    return render_to_response('core/sale_view.html',
                              {'sale': sale,},
                              context_instance=RequestContext(request))

@login_required
def add_sale(request):
    """
    Creates a sale transaction
    """
    if request.method == 'POST':
        form = SaleForm(request.POST, user_id=request.user.pk)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.user = request.user
            sale.save()
            return HttpResponseRedirect('/core/sale/')
    else:
        form = SaleForm(user_id=request.user.pk)
    return render_to_response('core/manage_sale.html',
                              {'form': form, 'is_new': True, 'products': Product.objects.filter(user=request.user)},
                              context_instance=RequestContext(request))

def edit_sale(request, id):
    """
    Updates a sale transaction
    """
    sale = Sale.objects.get(pk=id)
    if request.method == 'POST':
        form = SaleForm(request.POST, instance=sale, user_id=request.user.pk)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/core/sale/')
    else:
        form = SaleForm(instance=sale, user_id=request.user.pk)
    return render_to_response('core/manage_sale.html',
                              {'form': form, 'is_new': False},
                              context_instance=RequestContext(request))

def delete_sale(request, id):
    """
    Deletes a sale.
    """
    sale = Sale.objects.get(pk=id)
    sale.delete()
    return HttpResponseRedirect('/core/sale/')



@login_required
def campaign_home(request):
    """
    renders list of sales
    """
    campaign_list = Campaign.objects.filter(user=request.user)
    page = int(request.GET.get('page', '1'))
    sort = request.GET.get('sort', 'date')
    if sort:
        if sort == 'name':
            campaign_list = campaign_list.order_by('campaign_name')
        elif sort == 'date':
            campaign_list = campaign_list.order_by('start_date')

    try:
        paginator = Paginator(campaign_list, settings.DEFAULT_PAGESIZE)
        campaigns = paginator.page(page)
    except (EmptyPage, InvalidPage):
        # if the supplied page number is beyond the scope
        # show last page
        campaigns = paginator.page(paginator.num_pages)
        
    return render_to_response('core/campaign.html',
                              {'campaigns': campaigns,
                               'sort': sort,},
                              context_instance=RequestContext(request))

@login_required
def campaign_view(request, id):
    """
    renders a specific sale view.
    """
    campaign = Campaign.objects.get(pk=id)
    return render_to_response('core/campaign_view.html',
                              {'campaign': campaign,},
                              context_instance=RequestContext(request))

@login_required
def add_campaign(request):
    """
    Creates a sale transaction
    """
    if request.method == 'POST':
        form = CampaignForm(request.POST)
        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.user = request.user
            campaign.save()
            return HttpResponseRedirect('/core/campaign/')
    else:
        form = CampaignForm()
    return render_to_response('core/manage_campaign.html',
                              {'form': form, 'is_new': True,},
                              context_instance=RequestContext(request))

def edit_campaign(request, id):
    """
    Updates a sale transaction
    """
    campaign = Campaign.objects.get(pk=id)
    if request.method == 'POST':
        form = CampaignForm(request.POST, instance=campaign)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/core/campaign/')
    else:
        form = CampaignForm(instance=campaign)
    return render_to_response('core/manage_campaign.html',
                              {'form': form, 'is_new': False},
                              context_instance=RequestContext(request))

def delete_campaign(request, id):
    """
    Deletes a sale.
    """
    campaign = Campaign.objects.get(pk=id)
    campaign.delete()
    return HttpResponseRedirect('/core/campaign/')

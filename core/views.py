from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, InvalidPage

from django.conf import settings

from core.models import Customer, Category, Product, Purchase, Group
from core.forms import CustomerForm, CategoryForm, ProductForm, PurchaseForm

    
@login_required
def customer_home(request):
    """
    renders list of customers associated.
    """
    customer_list = Customer.objects.filter(user=request.user)
    paginator = Paginator(customer_list, settings.DEFAULT_PAGESIZE)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        customers = paginator.page(page)
    except (EmptyPage, InvalidPage):
        # if the supplied page number is beyond the scope
        # show last page
        customers = paginator.page(paginator.num_pages)
        
    return render_to_response('core/customer.html',
                              {'customers': customers,},
                              context_instance=RequestContext(request))

@login_required
def customer_view(request, id):
    """
    renders a specific customer's view.
    note: this is not customers info.
    """
    customer = Customer.objects.get(pk=id)
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
            return HttpResponseRedirect('/core/customer/')
    else:
        form = CustomerForm(instance=customer)
    return render_to_response('core/manage_customer.html',
                              {'form': form, 'is_new': False},
                              context_instance=RequestContext(request))

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
    paginator = Paginator(product_list, settings.DEFAULT_PAGESIZE)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        # if the supplied page number is beyond the scope
        # show last page
        products = paginator.page(paginator.num_pages)
        
    return render_to_response('core/product.html',
                              {'products': products,},
                              context_instance=RequestContext(request))

@login_required
def product_view(request, id):
    """
    renders a specific products's view.
    """
    product = Product.objects.get(pk=id)
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
            return HttpResponseRedirect('/core/product/')
    else:
        form = ProductForm(instance=product)
    return render_to_response('core/manage_product.html',
                              {'form': form, 'is_new': False},
                              context_instance=RequestContext(request))

@login_required
def purchase_home(request):
    """
    renders list of purchases
    """
    purchase_list = Purchase.objects.filter(user=request.user)
    paginator = Paginator(purchase_list, settings.DEFAULT_PAGESIZE)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        purchases = paginator.page(page)
    except (EmptyPage, InvalidPage):
        # if the supplied page number is beyond the scope
        # show last page
        purchases = paginator.page(paginator.num_pages)
        
    return render_to_response('core/purchase.html',
                              {'purchases': purchases,},
                              context_instance=RequestContext(request))

@login_required
def purchase_view(request, id):
    """
    renders a specific purchase view.
    """
    purchase = Purchase.objects.get(pk=id)
    return render_to_response('core/purchase_view.html',
                              {'purchase': purchase,},
                              context_instance=RequestContext(request))

@login_required
def add_purchase(request):
    """
    Creates a Purchase transaction
    """
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            purchase = form.save(commit=False)
            purchase.user = request.user
            purchase.save()
            return HttpResponseRedirect('/core/purchase/')
    else:
        form = PurchaseForm()
    return render_to_response('core/manage_purchase.html',
                              {'form': form, 'is_new': True},
                              context_instance=RequestContext(request))

def edit_purchase(request, id):
    """
    Updates a Purchase transaction
    """
    purchase = Purchase.objects.get(pk=id)
    if request.method == 'POST':
        form = PurchaseForm(request.POST, instance=purchase)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/core/purchase/')
    else:
        form = PurchaseForm(instance=purchase)
    return render_to_response('core/manage_purchase.html',
                              {'form': form, 'is_new': False},
                              context_instance=RequestContext(request))

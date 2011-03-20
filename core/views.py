from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, InvalidPage

from django.conf import settings

from core.models import Customer, Group, Product
from core.forms import CustomerForm, GroupForm, ProductForm

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
                              {'form': form},
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
                              {'form': form},
                              context_instance=RequestContext(request))

@login_required
def group_home(request):
    """
    renders list of available groups
    """
    group_list = Group.objects.filter(user=request.user)
    paginator = Paginator(group_list, settings.DEFAULT_PAGESIZE)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        groups = paginator.page(page)
    except (EmptyPage, InvalidPage):
        # if the supplied page number is beyond the scope
        # show last page
        groups = paginator.page(paginator.num_pages)
        
    return render_to_response('core/group.html',
                              {'groups': groups,},
                              context_instance=RequestContext(request))

@login_required
def group_view(request, id):
    """
    renders a specific group's view.
    """
    group = Group.objects.get(pk=id)
    return render_to_response('core/group_view.html',
                              {'group': group,},
                              context_instance=RequestContext(request))

@login_required
def add_group(request):
    """
    Creates a Group instance
    """
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.user = request.user
            group.save()
            return HttpResponseRedirect('/core/group/')
    else:
        form = GroupForm()
    return render_to_response('core/manage_group.html',
                              {'form': form},
                              context_instance=RequestContext(request))

def edit_group(request, id):
    """
    Updates a Group details
    """
    group = Group.objects.get(pk=id)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/core/group/')
    else:
        form = GroupForm(instance=group)
    return render_to_response('core/manage_group.html',
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
                              {'form': form},
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
                              {'form': form},
                              context_instance=RequestContext(request))

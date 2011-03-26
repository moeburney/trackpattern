from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.conf import settings

from core.models import Customer, Group, Product, Purchase

@login_required
def home(request):
    """
    renders dashboard.
    """
    return render_to_response('home/home.html',
                              {},
                              context_instance=RequestContext(request))


@login_required
def search(request):
    """
    search for given name in group, customer, product etc.
    """
    word = request.POST.get('word','')

    groups = Group.objects.filter(name__icontains=word)
    customers = Customer.objects.filter(first_name__icontains=word)
    products = Product.objects.filter(name__icontains=word)
    
    return render_to_response('home/search_result.html',
                              {'word': word,
                               'groups': groups,
                               'customers': customers,
                               'products': products,},
                              context_instance=RequestContext(request))


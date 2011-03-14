from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404

from core.models import Customer
from core.forms import CustomerForm

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
            return HttpResponseRedirect('/home/')
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
            return HttpResponseRedirect('/home/')
    else:
        form = CustomerForm(instance=customer)
    return render_to_response('core/manage_customer.html',
                              {'form': form},
                              context_instance=RequestContext(request))

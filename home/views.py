from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.conf import settings

from core.models import Customer

@login_required
def show_dashboard(request):
    """
    renders dashboard.
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
        
    return render_to_response('home/dashboard.html',
                              {'customers': customers,},
                              context_instance=RequestContext(request))

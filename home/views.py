from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.conf import settings

@login_required
def home(request):
    """
    renders dashboard.
    """
    return render_to_response('home/home.html',
                              {},
                              context_instance=RequestContext(request))

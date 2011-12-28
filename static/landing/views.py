from django.template import RequestContext
from django.shortcuts import render_to_response

def landing(request):
    """
    renders dashboard.
    """
    return render_to_response('landing/index.html',
        context_instance=RequestContext(request))

# Create your views here.

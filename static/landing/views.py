from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.views import static

def landing(request):
    """
    renders dashboard.
    """
    return render_to_response('landing/index.html',
                              context_instance=RequestContext(request))
# Create your views here.

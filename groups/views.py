# Create your views here.
from django.shortcuts import  render_to_response
# ...
def detail(request):
    return render_to_response('groups/groups.html')


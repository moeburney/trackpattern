from django.http import HttpResponseRedirect
from django.http import HttpResponse
import re

subdomain_pattern = re.compile('(?P<subdomain>.*?)\..*?')


class SubdomainMiddleware(object):
    def process_request(self, request):
        if len(request.get_host().split('.')) > 2 and request.get_host().split('.')[0] != "app" and request.user.is_authenticated():
            match = subdomain_pattern.match(request.get_host())
            subdomain = match.group('subdomain')
            if subdomain != str(request.user).lower():
                uzer = str(request.user).lower()
                return HttpResponse(
                    "You are logged in as " + uzer + ", and your subdomain is " + subdomain + ". Please go to " + uzer + ".trackpattern.com")
        elif request.get_host().split('.')[0] == "app" and request.user.is_authenticated():
            uzer = str(request.user).lower()
            return HttpResponseRedirect("http://" + uzer + "." + "trackpattern.com" + '/home')
        elif len(request.get_host().split('.')) > 2 and request.get_host().split('.')[
                                                        0] != "app" and request.user.is_anonymous():
            return HttpResponseRedirect("http://app.trackpattern.com")

__author__ = 'rohan'
import sys
import os
path = '/srv/vrt/tracklist-prod'
if path not in sys.path:
    #sys.path.append('/srv')
    sys.path.append(path)


os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()

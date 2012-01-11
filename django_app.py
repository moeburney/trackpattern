__author__ = 'rohan'
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
path = '/root/tracklist'
if path not in sys.path:
    sys.path.append('/root')
    sys.path.append(path)


import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()

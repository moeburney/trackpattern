import os
import sys

path = '/home/tracklist_git'
if path not in sys.path:
	sys.path.append('/home')
	sys.path.append(path)


os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


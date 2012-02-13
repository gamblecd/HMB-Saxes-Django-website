import os
import sys
 
path = '/home/shadowstorm/husky_saxes/src'
if path not in sys.path:
    sys.path.insert(0, path)
 
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
 
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

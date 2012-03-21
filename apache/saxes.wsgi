import os
import sys

paths = [
      	 "/home/shadowstorm/husky_saxes",
	 	 "/home/shadowstorm/husky_saxes/src",
      	 "/home/shadowstorm/husky_saxes/src/saxes",
      	 
]
for path in paths:
    if path not in sys.path:
        sys.path.insert(0, path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

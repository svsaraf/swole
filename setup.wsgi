import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi

print "Hello"

application = django.core.handlers.wsgi.WSGIHandler()


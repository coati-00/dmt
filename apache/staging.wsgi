import os, sys, site

# enable the virtualenv
site.addsitedir('/var/www/dmt/dmt/ve/lib/python2.7/site-packages')

# paths we might need to pick up the project's settings
sys.path.append('/var/www/dmt/dmt/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'dmt.settings_staging'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()

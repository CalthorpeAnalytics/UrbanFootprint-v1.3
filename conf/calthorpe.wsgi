import os
import sys

path = '/srv/calthorpe/urbanfootprint/calthorpe/server'
if path not in sys.path:
  sys.path.append(path)

path = '/srv/calthorpe/urbanfootprint/calthorpe/server/calthorpe'
if path not in sys.path:
  sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'calthorpe.settings'
os.environ["CELERY_LOADER"] = "django"

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

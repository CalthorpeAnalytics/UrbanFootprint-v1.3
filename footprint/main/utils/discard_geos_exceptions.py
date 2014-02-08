__author__ = 'calthorpe'

# https://gist.github.com/tobych/6372218
# Monkey patch to work around https://code.djangoproject.com/ticket/13843

import django
from functools import wraps

def discard_exceptions(f):
  @wraps(f)
  def wrapper(*args, **kwds):
    try:
      f(*args, **kwds)
    except (AttributeError, TypeError):
      pass
  return wrapper

django.contrib.gis.geos.prototypes.threadsafe.GEOSContextHandle.__del__ = \
  discard_exceptions(django.contrib.gis.geos.prototypes.threadsafe.GEOSContextHandle.__del__)
django.contrib.gis.geos.prototypes.io.IOBase.__del__ = \
  discard_exceptions(django.contrib.gis.geos.prototypes.io.IOBase.__del__)
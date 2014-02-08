__author__ = 'calthorpe'

from django.db import models
from footprint.main.models.geospatial.feature import Feature


class VmtTripLengthsFeature(Feature):
    
    productions_hbw = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    productions_hbo = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    productions_nhb = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    attractions_hbw = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    attractions_hbo = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    attractions_nhb = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    emp_30min_transit = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    emp_45min_transit = models.DecimalField(max_digits=14, decimal_places=4, default=0)

    class Meta(object):
        abstract = True
        app_label = 'main'


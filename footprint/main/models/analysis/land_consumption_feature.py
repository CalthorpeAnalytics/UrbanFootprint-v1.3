from django.db import models
from footprint.main.models.geospatial.feature import Feature


__author__ = 'calthorpe_associates'



class LandConsumptionFeature(Feature):
    acres_gross = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    acres_consumed = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    acres_greenfield_consumed = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    acres_urban_consumed = models.DecimalField(max_digits=14, decimal_places=4, default=0)


    class Meta(object):
        abstract = True
        app_label = 'main'

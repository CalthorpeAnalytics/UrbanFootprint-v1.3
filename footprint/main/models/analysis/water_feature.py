
from django.db import models
from footprint.main.models.geospatial.feature import Feature


__author__ = 'calthorpe_associates'



class WaterFeature(Feature):

    evapotranspiration_zone = models.IntegerField(null=True, default=None)
    pop = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    hh = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    emp = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    total_water_use = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    residential_water_use = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    commercial_water_use = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    residential_indoor_water_use = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    commercial_indoor_water_use = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    residential_outdoor_water_use = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    commercial_outdoor_water_use = models.DecimalField(max_digits=14, decimal_places=4, default=0)

    class Meta(object):
        abstract = True
        app_label = 'main'
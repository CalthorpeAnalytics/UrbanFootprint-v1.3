from footprint.main.managers.geo_inheritance_manager import GeoInheritanceManager

__author__ = 'calthorpe'
from django.contrib.gis.db import models


class AgricultureAttributeSet(models.Model):
    """
    A set of agricultural attributes for a place

    all values except unit price are per-acre densities
    """

    objects = GeoInheritanceManager()

    crop_yield = models.FloatField(default=0)
    unit_price = models.FloatField(default=0)
    cost = models.FloatField(default=0)
    water_consumption = models.FloatField(default=0)
    labor_input = models.FloatField(default=0)
    truck_trips = models.FloatField(default=0)

    class Meta(object):
        abstract = False
        app_label = 'main'

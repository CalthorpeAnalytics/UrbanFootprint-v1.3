__author__ = 'calthorpe'

from django.db import models
from footprint.main.models.geospatial.feature import Feature


class VmtFeature(Feature):

    acres_gross = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    pop = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    du = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    hh = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    emp = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    final_prod_hbo = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    final_prod_hbw = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    final_prod_nhb = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    final_attr_hbo = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    final_attr_hbw = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    final_attr_nhb = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    vmt_daily = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    vmt_daily_w_trucks = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    vmt_daily_per_capita = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    vmt_daily_per_hh = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    vmt_annual = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    vmt_annual_w_trucks = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    vmt_annual_per_capita = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    vmt_annual_per_hh = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    raw_trips_total = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    internal_capture_trips_total = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    walking_trips_total = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    transit_trips_total = models.DecimalField(max_digits=14, decimal_places=4, default=0)

    class Meta(object):
        abstract = True
        app_label = 'main'
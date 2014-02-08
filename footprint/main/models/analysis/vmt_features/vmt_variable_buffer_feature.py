__author__ = 'calthorpe'

from django.db import models
from footprint.main.models.geospatial.feature import Feature


class VmtVariableBufferFeature(Feature):

    distance = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    acres_parcel_res = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    acres_parcel_emp = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    acres_parcel_mixed = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    du = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    pop = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    emp = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    emp_ret = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    hh = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    du_mf = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    hh_inc_00_10 = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    hh_inc_10_20 = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    hh_inc_20_30 = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    hh_inc_30_40 = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    hh_inc_40_50 = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    hh_inc_50_60 = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    hh_inc_60_75 = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    hh_inc_75_100 = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    hh_inc_75_100 = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    hh_inc_100p = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    pop_employed = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    pop_age16_up = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    pop_age65_up = models.DecimalField(max_digits=14, decimal_places=4, default=0)
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
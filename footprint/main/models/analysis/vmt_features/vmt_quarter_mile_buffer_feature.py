__author__ = 'calthorpe'

from django.db import models
from footprint.main.models.geospatial.feature import Feature


class VmtQuarterMileBufferFeature(Feature):

    acres_parcel_res = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    acres_parcel_emp = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    acres_parcel_mixed = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    du = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    pop = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    emp = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    emp_ret = models.DecimalField(max_digits=14, decimal_places=4, default=0)

    class Meta(object):
        abstract = True
        app_label = 'main'

__author__ = 'calthorpe'

from django.db import models
from footprint.main.models.geospatial.feature import Feature


class VmtQuarterMileBufferFeature(Feature):

    acres_parcel_res = models.DecimalField(max_digits=14, decimal_places=4, default=0, null=True)
    acres_parcel_emp = models.DecimalField(max_digits=14, decimal_places=4, default=0, null=True)
    acres_parcel_mixed = models.DecimalField(max_digits=14, decimal_places=4, default=0, null=True)
    du = models.DecimalField(max_digits=14, decimal_places=4, default=0, null=True)
    pop = models.DecimalField(max_digits=14, decimal_places=4, default=0, null=True)
    emp = models.DecimalField(max_digits=14, decimal_places=4, default=0, null=True)
    emp_ret = models.DecimalField(max_digits=14, decimal_places=4, default=0, null=True)

    class Meta(object):
        abstract = True
        app_label = 'main'

from django.db import models
from footprint.main.models.geospatial.feature import Feature


__author__ = 'calthorpe_associates'


class FiscalFeature(Feature):
    residential_capital_costs = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    residential_operations_maintenance_costs = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    residential_revenue = models.DecimalField(max_digits=14, decimal_places=4, default=0)

    class Meta(object):
        abstract = True
        app_label = 'main'

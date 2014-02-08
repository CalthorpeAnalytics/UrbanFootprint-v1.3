__author__ = 'calthorpe'

from django.db import models
from footprint.main.models.geospatial.feature import Feature


class VmtOneMileBufferFeature(Feature):

    emp = models.DecimalField(max_digits=14, decimal_places=4, default=0)

    class Meta(object):
        abstract = True
        app_label = 'main'
__author__ = 'calthorpe_associates'

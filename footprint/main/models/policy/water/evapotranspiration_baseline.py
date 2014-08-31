from django.db import models
from model_utils.managers import InheritanceManager

__author__ = 'calthorpe_associates'


class EvapotranspirationBaseline(models.Model):

    objects = InheritanceManager()

    zone = models.IntegerField(null=False)
    annual_evapotranspiration = models.DecimalField(max_digits=14, decimal_places=4, default=0)

    class Meta(object):
        abstract = False
        app_label = 'main'

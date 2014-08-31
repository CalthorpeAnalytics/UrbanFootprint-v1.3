from django.db import models
from model_utils.managers import InheritanceManager


__author__ = 'calthorpe_associates'


class ResidentialEnergyBaseline(models.Model):
    
    objects = InheritanceManager()
    zone = models.IntegerField(null=False)
    du_detsf_ll_electricity = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    du_detsf_sl_electricity = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    du_attsf_electricity = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    du_mf_electricity = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    du_detsf_ll_gas = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    du_detsf_sl_gas = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    du_attsf_gas = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    du_mf_gas = models.DecimalField(max_digits=14, decimal_places=4, default=0)

    class Meta(object):
        abstract = False
        app_label = 'main'

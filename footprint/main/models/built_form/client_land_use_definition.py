from django.contrib.gis.db import models
from footprint.main.managers.geo_inheritance_manager import GeoInheritanceManager

__author__ = 'calthorpe_associates'


class ClientLandUseDefinition(models.Model):
    """
        A generic land use definition class for clients to subclass
    """
    objects = GeoInheritanceManager()
    class Meta(object):
        abstract = True
        app_label = 'main'
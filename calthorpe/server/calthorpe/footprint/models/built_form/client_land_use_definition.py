from django.contrib.gis.db import models
from footprint.managers.geo_inheritance_manager import GeoInheritanceManager

__author__ = 'calthorpe'


class ClientLandUseDefinition(models.Model):
    """
        A generic land use definition class for clients to subclass
    """
    objects = GeoInheritanceManager()
    class Meta(object):
        abstract = True
        app_label = 'footprint'
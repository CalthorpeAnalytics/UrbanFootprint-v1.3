from footprint.main.models.geographies.geography import Geography

__author__ = 'calthorpe_associates'

from django.contrib.gis.db import models


class Geographic(models.Model):
    """
    a mixin to add a reference to the Geography class
    """
    geography = models.ForeignKey(Geography, null=True)

    @classmethod
    def geography_type(cls):
        return None

    # todo: we don't need to use the layermapping importer for peer tables, so let's only put this on the base tables
    # Because of the layer importer we need this even though the geometry is in the Geography instance
    #wkb_geometry = models.GeometryField()

    class Meta(object):
        abstract = True


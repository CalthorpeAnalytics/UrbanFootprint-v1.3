from django.contrib.gis.db import models

from footprint.models.geospatial.feature import Feature

__author__ = 'calthorpe'


class ScagFloodplainFeature(Feature):
    zone = models.CharField(max_length=50, null=False)
    cobra = models.CharField(max_length=50, null=False)
    special_flood_hazard_area = models.CharField(max_length=50, null=False)
    symbol = models.IntegerField(null=False)
    panel_type = models.CharField(max_length=50, null=False)


    class Meta(object):
        abstract = True
        app_label = 'footprint'


class TemplateScagFloodplainFeature(ScagFloodplainFeature):
    """
        Template subclass so that south generates migrations that we can apply to the dynamically generated subclasses
    """

    class Meta(object):
        app_label = 'footprint'
        abstract = False

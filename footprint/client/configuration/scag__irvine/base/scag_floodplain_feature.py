from django.contrib.gis.db import models

from footprint.main.models.geospatial.feature import Feature

__author__ = 'calthorpe_associates'


class ScagFloodplainFeature(Feature):
    zone = models.CharField(max_length=50, null=False)
    cobra = models.CharField(max_length=50, null=False)
    special_flood_hazard_area = models.CharField(max_length=50, null=False)
    symbol = models.IntegerField(null=False)
    panel_type = models.CharField(max_length=50, null=False)


    class Meta(object):
        abstract = True
        app_label = 'main'


class TemplateScagFloodplainFeature(ScagFloodplainFeature):
    """
        Template subclass so that south generates migrations that we can apply to the dynamically generated subclasses
    """

    class Meta(object):
        app_label = 'main'
        abstract = False

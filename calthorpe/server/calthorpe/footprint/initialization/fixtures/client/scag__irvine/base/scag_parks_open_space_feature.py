from django.contrib.gis.db import models

from footprint.models.geospatial.feature import Feature

__author__ = 'calthorpe'


class ScagParksOpenSpaceFeature(Feature):
    site_name = models.CharField(max_length=100, null=False)
    agency = models.CharField(max_length=50, null=False)
    access = models.CharField(max_length=50, null=False)
    land_use_designation = models.CharField(max_length=50, null=False)
    acres = models.DecimalField(max_digits=10, decimal_places=3)


    class Meta(object):
        abstract = True
        app_label = 'footprint'


class TemplateScagParksOpenSpaceFeature(ScagParksOpenSpaceFeature):
    """
        Template subclass so that south generates migrations that we can apply to the dynamically generated subclasses
    """

    class Meta(object):
        app_label = 'footprint'
        abstract = False

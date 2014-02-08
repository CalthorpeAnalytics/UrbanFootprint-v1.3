from django.contrib.gis.db import models

from footprint.main.models.geospatial.feature import Feature

__author__ = 'calthorpe_associates'


class ScagHabitatConservationAreasFeature(Feature):
    name = models.CharField(max_length=50, null=False)
    hcp = models.CharField(max_length=50, null=False)
    nccp = models.CharField(max_length=50, null=False)
    stage = models.CharField(max_length=50, null=False)

    class Meta(object):
        abstract = True
        app_label = 'main'


class TemplateScagHabitatConservationAreasFeature(ScagHabitatConservationAreasFeature):
    """
        Template subclass so that south generates migrations that we can apply to the dynamically generated subclasses
    """

    class Meta(object):
        app_label = 'main'
        abstract = False

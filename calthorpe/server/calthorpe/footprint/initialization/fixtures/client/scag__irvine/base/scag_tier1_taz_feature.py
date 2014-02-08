from django.contrib.gis.db import models

from footprint.models.geospatial.feature import Feature

__author__ = 'calthorpe'


class ScagTier1TazFeature(Feature):
    id_taz12a = models.CharField(max_length=50, null=False)
    taz_id = models.IntegerField(null=False)

    class Meta(object):
        abstract = True
        app_label = 'footprint'


class TemplateScagTier1TazFeature(ScagTier1TazFeature):
    """
        Template subclass so that south generates migrations that we can apply to the dynamically generated subclasses
    """

    class Meta(object):
        app_label = 'footprint'
        abstract = False

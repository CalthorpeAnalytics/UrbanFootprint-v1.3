from django.contrib.gis.db import models

from footprint.main.models.geospatial.feature import Feature

__author__ = 'calthorpe_associates'


class ScagTier1TazFeature(Feature):
    id_taz12a = models.CharField(max_length=50, null=False)
    taz_id = models.IntegerField(null=False)

    class Meta(object):
        abstract = True
        app_label = 'main'

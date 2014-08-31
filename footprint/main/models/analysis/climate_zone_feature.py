from django.db import models
from footprint.main.models.geospatial.feature import Feature


__author__ = 'calthorpe_associates'


class ClimateZoneFeature(Feature):

    evapotranspiration_zone_id = models.IntegerField(null=True)
    forecasting_climate_zone_id = models.IntegerField(null=True)
    title_24_zone_id = models.IntegerField(null=True)

    class Meta(object):
        abstract = True
        app_label = 'main'

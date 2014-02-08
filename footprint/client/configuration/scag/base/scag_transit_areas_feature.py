from footprint.main.models.geospatial.feature import Feature

__author__ = 'calthorpe_associates'


class ScagTransitAreasFeature(Feature):
    class Meta(object):
        abstract = True
        app_label = 'main'

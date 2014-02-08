__author__ = 'calthorpe_associates'

from footprint.main.models.geospatial.feature import Feature

class Spz(Feature):
    """
        Represents an SCAG authoritative SPZ definition, whose pk is referenced by other geospatial tables
    """
    class Meta(object):
        app_label = 'main'

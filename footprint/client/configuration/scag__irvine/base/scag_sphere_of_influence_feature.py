from footprint.main.models.geospatial.feature import Feature

__author__ = 'calthorpe_associates'

class ScagSphereOfInfluenceFeature(Feature):
    class Meta(object):
        abstract = True
        app_label = 'main'


class TemplateScagSphereOfInfluenceFeature(ScagSphereOfInfluenceFeature):
    """
        Template subclass so that south generates migrations that we can apply to the dynamically generated subclasses
    """

    class Meta(object):
        app_label = 'main'
        abstract = False


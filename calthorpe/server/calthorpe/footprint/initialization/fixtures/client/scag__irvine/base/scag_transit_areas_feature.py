from footprint.mixins.geographic import Geographic

__author__ = 'calthorpe'


class ScagTransitAreasFeature(Geographic):
    class Meta(object):
        abstract = True
        app_label = 'footprint'


class TemplateScagTransitAreasFeature(ScagTransitAreasFeature):
    """
        Template subclass so that south generates migrations that we can apply to the dynamically generated subclasses
    """

    class Meta(object):
        app_label = 'footprint'
        abstract = False

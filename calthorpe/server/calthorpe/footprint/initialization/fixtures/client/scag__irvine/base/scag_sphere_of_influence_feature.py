from footprint.mixins.geographic import Geographic

__author__ = 'calthorpe'


class ScagSphereOfInfluenceFeature(Geographic):
    class Meta(object):
        abstract = True
        app_label = 'footprint'


class TemplateScagSphereOfInfluenceFeature(ScagSphereOfInfluenceFeature):
    """
        Template subclass so that south generates migrations that we can apply to the dynamically generated subclasses
    """

    class Meta(object):
        app_label = 'footprint'
        abstract = False


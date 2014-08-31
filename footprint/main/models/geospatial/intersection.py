from django.db import models
from footprint.main.lib.functions import merge
from footprint.main.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.main.models.keys.keys import Keys

__author__ = 'calthorpe'

class IntersectionKey(Keys):
    """
        A key class to describe geographic intersection types
    """
    class Fab(Keys.Fab):
        @classmethod
        def prefix(cls):
            # No prefix is used, since these aren't stored as keys in a key column
            return ''
    # Intersect based on the polygon of the feature
    POLYGON = 'polygon'
    # Intersect based on the centroid of the feature
    CENTROID = 'centroid'
    # Intersect based on an attribute of the feature
    ATTRIBUTE = 'attribute'
    GEOGRAPHIC = 'geographic'

class Intersection(models.Model):
    """
        Describes an intersection from on geographic table to another.
    """

    def __init__(self, *args, **kwargs):
        super(Intersection, self).__init__(*args, **merge(
            kwargs,
            dict(join_type=kwargs.get('join_type',
                                      IntersectionKey.GEOGRAPHIC if kwargs.get('from_type') or kwargs.get('to_type') else None)
            )
        ))

    # Indicates whether the intersection type is geographic or attribute based. The default is geographic
    # IntersectionKey.(GEOGRAPHIC|ATTRIBUTE)
    # This will default to IntersectionKey.GEOGRAPHIC if either from_type or to_type is set
    join_type = models.CharField(max_length=50, null=False)
    # An geographic shape for the DbEntity containing the FeatureBehavior that
    # has the intersection. IntersectionKey.(POLYGON|CENTROID)
    from_type = models.CharField(max_length=50, null=True)
    # An geographic shape for the target DbEntity of the intersection.
    # IntersectionKey.(POLYGON|CENTROID)
    to_type = models.CharField(max_length=50, null=True)

    objects = GeoInheritanceManager()

    class Meta(object):
        abstract = False
        app_label = 'main'


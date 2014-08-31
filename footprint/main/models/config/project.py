# coding=utf-8
from django.contrib.gis.geos import Polygon, MultiPolygon
from django.db import models
from django.conf import settings

from footprint.main.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.main.models.config.region import Region
from footprint.main.models.config.config_entity import ConfigEntity

__author__ = 'calthorpe_associates'


class Project(ConfigEntity):
    """
        A Project references a single Region and serves as the parent configuration for one or more Scenarios
    """
    objects = GeoInheritanceManager()

    base_year = models.IntegerField(default=2005)

    def __init__(self, *args, **kwargs):
        super(Project, self).__init__(*args, **kwargs)
        self.srid = settings.DEFAULT_SRID

    def recalculate_bounds(self):
        authority_feature_classes = [self.db_entity_feature_class(db_entity.key)
                                     for db_entity in self.computed_db_entities() if db_entity.extent_authority]
        extents = []
        for authority_feature_class in authority_feature_classes:
            all_features = authority_feature_class.objects.all()
            if len(all_features) > 0:
                bounds = all_features.extent_polygon()
                extents.append(bounds)
                self.bounds = MultiPolygon(extents)
                # Disable publishers for this simple update
                self._no_post_save_publishing = True
                self.save()
                self._no_post_save_publishing = False
            else:
                pass

    def region(self):
        return self.parent_config_entity

    def save(self, force_insert=False, force_update=False, using=None):
        super(Project, self).save(force_insert, force_update, using)

    @classmethod
    def parent_classes(cls):
        """
            Projects may only have a Region for a parent
        :param cls:
        :return:
        """
        return [Region]

    class Meta(object):
        app_label = 'main'
# coding=utf-8
from django.contrib.gis.geos import Polygon, MultiPolygon
from django.db import models
from django.conf import settings

from footprint.initialization.fixture import ProjectFixture
from footprint.initialization.utils import resolve_fixture
from footprint.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.models.config.region import Region
from footprint.models.config.config_entity import ConfigEntity

__author__ = 'calthorpe'


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
        bounds_authorities = [db_entity['feature_class'] for db_entity in self.default_db_entity_setups() if
                              db_entity.get('extent_authority', False)]
        extents = []
        for authority in bounds_authorities:
            all_features = authority.objects.all()
            if len(all_features) > 0:
                extent = all_features.extent()
                bounds = Polygon((
                    (extent[0], extent[1]),
                    (extent[0], extent[3]),
                    (extent[2], extent[3]),
                    (extent[2], extent[1]),
                    (extent[0], extent[1]),
                ))
                extents.append(bounds)
                self.bounds = MultiPolygon(extents)
                self.save()
            else:
                pass

    def region(self):
        return self.parent_config_entity

    def save(self, force_insert=False, force_update=False, using=None):
        super(Project, self).save(force_insert, force_update, using)

    def default_db_entity_setups(self):
        client_project = resolve_fixture("config_entity", "project", ProjectFixture, self.schema(), config_entity=self)
        return client_project.default_db_entity_setups()

    @classmethod
    def parent_classes(cls):
        """
            Projects may only have a Region for a parent
        :param cls:
        :return:
        """
        return [Region]

    class Meta(object):
        app_label = 'footprint'
# coding=utf-8
# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
#
# Copyright (C) 2012 Calthorpe Associates
#
# This program is free software: you can redistribute it and/or modify it under the terms of the
 # GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.
#
# Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates.
# Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709.
# Phone: (510) 548-6800. Web: www.calthorpe.com
from django.db import models
from footprint.initialization.fixture import ScenarioFixture
from footprint.initialization.utils import resolve_fixture
from footprint.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.models.config.config_entity import ConfigEntity
from footprint.models.config.project import Project

__author__ = 'calthorpe'


class Scenario(ConfigEntity):
    """
        ProjectScenario is a temporary name while the old Scenario class exists
        Scenarios configure future conditions relatives to the base conditions of their project
    """
    objects = GeoInheritanceManager()

    year = models.IntegerField(null=False, blank=False)

    def set_parent_config_entity(self):
        self.bounds = self.parent_config_entity.bounds

    def save(self, force_insert=False, force_update=False, using=None):
        self.expect_parent_config_entity()
        super(Scenario, self).save(force_insert, force_update, using)

    def project(self):
        return self.parent_config_entity

    def full_name(self):
        """
            Concatinates all ancestor names except for that of the GlobalConfig and adds self.name. Scenario also
            includes the year
        """
        return ' '.join(self.parent_config_entity.full_name().extend([self.name, self.year])[1:])

    @classmethod
    def parent_classes(cls):
        """
            Scenarios may only have Projects as a parent
        :param cls:
        :return:
        """
        return [Project]

    def default_db_entity_setups(self):
        client_scenario = resolve_fixture(
            "config_entity",
            "scenario",
            ScenarioFixture,
            self.schema(),
            config_entity=self)
        return client_scenario.default_db_entity_setups()

    class Meta(object):
        # Make abstract = False so that a Scenario table is created to store common Scenario attributes
        # Callers may also choose to deal with Scenarios generally and not with the subclasses
        abstract = False
        app_label = 'footprint'

class BaseScenario(Scenario):
    """
        BaseScenarios represent an editing of primary or BaseFeature data.
    """
    objects = GeoInheritanceManager()
    class Meta(object):
        abstract = False
        app_label = 'footprint'

class FutureScenario(Scenario):
    """
        FutureScenarios represent and editing of a BuiltFormFeature table
        that is derived from an UrbanFootprint BaseFeature table
    """
    objects = GeoInheritanceManager()
    class Meta(object):
        abstract = False
        app_label = 'footprint'

def resolve_config_entity(config_entity):
    """
        Hack to deal with subclasses
    :param params:
    :return:
    """

    # TODO hack to handle lack of multi-level subclass relation resolution
    scenarios = FutureScenario.objects.filter(id=int(config_entity.id))
    if len(list(scenarios)) > 0:
        # Scenario subclass instance
        return scenarios[0]
    else:
        scenarios = BaseScenario.objects.filter(id=int(config_entity.id))
        if len(list(scenarios)) > 0:
            return scenarios[0]
        else:
            return ConfigEntity.objects.filter(id=int(config_entity.id)).select_subclasses()[0]


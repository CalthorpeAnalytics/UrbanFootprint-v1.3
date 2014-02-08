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
from footprint.initialization.fixture import GlobalConfigFixture
from footprint.initialization.utils import resolve_fixture

from footprint.managers.geo_inheritance_manager import FootprintGeoManager
from footprint.models.config.config_entity import ConfigEntity
from footprint.models.keys.keys import Keys
import settings

__author__ = 'calthorpe'


class GlobalConfig(ConfigEntity):
    """
        A singleton whose adoptable attributes are adopted by other ConfigEntity instances
    """

    objects = FootprintGeoManager()

    def __init__(self, *args, **kwargs):
        super(GlobalConfig, self).__init__(*args, **kwargs)
        self.key = Keys.GLOBAL_CONFIG_KEY
        self.name = Keys.GLOBAL_CONFIG_NAME

    def full_name(self):
        """
            Overrides the default and return name
        """
        return self.name

    def db_entity_owner(self, db_entity):
        if self.schema() == db_entity.schema:
            return self
        raise Exception("Reached GlobalConfig without finding an owner for the db_entity {0}".format(db_entity))

    def default_db_entity_setups(self):
        client_global_config = resolve_fixture(
            "config_entity", "global_config", GlobalConfigFixture, settings.CLIENT, config_entity=self)
        return client_global_config.default_db_entity_setups()

    @classmethod
    def parent_classes(cls):
        """
            GlobalConfig can not have a parent
        """
        return []

    class Meta(object):
        app_label = 'footprint'


def global_config_singleton():
    """
        Returns the lone GlobalConfig, throwing an ObjectNotFound Exception if it hasn't yet been created
    :return:
    """
    return GlobalConfig.objects.get(key=Keys.GLOBAL_CONFIG_KEY)


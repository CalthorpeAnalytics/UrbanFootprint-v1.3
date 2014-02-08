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
from footprint.main.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.main.models.config.global_config import GlobalConfig, global_config_singleton
from footprint.main.models.config.config_entity import ConfigEntity

__author__ = 'calthorpe_associates'


class Region(ConfigEntity):
    """
        The Region may have a parent Region.
    """
    objects = GeoInheritanceManager()

    def __init__(self, *args, **kwargs):
        super(Region, self).__init__(*args, **kwargs)
        self.parent_config_entity = self.parent_config_entity or global_config_singleton()

    def save(self, force_insert=False, force_update=False, using=None):
        super(Region, self).save(force_insert, force_update, using)

    @classmethod
    def parent_classes(cls):
        return [GlobalConfig]


    class Meta(object):
        app_label = 'main'


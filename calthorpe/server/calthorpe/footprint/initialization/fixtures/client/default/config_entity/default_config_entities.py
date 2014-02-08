# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
#
# Copyright (C) 2013 Calthorpe Associates
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
from footprint.initialization.fixture import ConfigEntitiesFixture
from footprint.initialization.fixtures.client.default.default_mixin import DefaultMixin
from footprint.models.keys.keys import Keys

__author__ = 'calthorpe'


class ConfigEntityMediumKey(Keys):
    class Fab(Keys.Fab):
        @classmethod
        def prefix(cls):
            return 'config_entity_medium'


class DefaultConfigEntitiesFixture(DefaultMixin, ConfigEntitiesFixture):
    def regions(self):
        return [
        ]

    def projects(self, region=None):
        return [
        ]

    def scenarios(self, project=None, class_scope=None):
        return self.matching_keys([], project_key=project.key if project else None, class_scope=class_scope)

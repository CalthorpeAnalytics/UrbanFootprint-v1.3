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

from nose import with_setup
from footprint.models.config.global_config import global_config_singleton
from footprint.models.database.information_schema import PGNamespace
from footprint.tests.test_models.test_config_entity.test_config_entity import TestConfigEntity

__author__ = 'calthorpe'

class TestGlobal(TestConfigEntity):

    def setup(self):
        super(TestGlobal, self).__init__()

    def teardown(self):
        super(TestGlobal, self).__init__()

    @with_setup(setup, teardown)
    def test_application_initialization(self):
        global_config = global_config_singleton()
        # Assert that the schema is created
        assert PGNamespace.objects.schema_exists(global_config.schema()), "The global schema %s does not exist" % global_config.schema()
        # Assert that the singleton method returns the single global_config
        assert global_config_singleton() == global_config

    @with_setup(setup, teardown)
    def test_global_add_policy_set(self):
        pass

    @with_setup(setup, teardown)
    def test_global_add_policy_set(self):
        pass

    @with_setup(setup, teardown)
    def test_global_add_db_entity(self):
        pass


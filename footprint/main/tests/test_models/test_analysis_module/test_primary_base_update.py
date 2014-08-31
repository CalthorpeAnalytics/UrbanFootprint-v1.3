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
from footprint.main.models.application_initialization import application_initialization, \
    update_or_create_config_entities
from footprint.main.models.base.primary_base_feature import PrimaryParcelFeature
from footprint.main.tests.test_models.test_config_entity.test_config_entity import TestConfigEntity

__author__ = 'calthorpe_associates'

class TestPrimaryBaseUpdate(TestConfigEntity):

    def setup(self):
        super(TestPrimaryBaseUpdate, self).__init__()
        application_initialization()
        update_or_create_config_entities()

    def teardown(self):
        super(TestPrimaryBaseUpdate, self).__init__()

    @with_setup(setup, teardown)
    def test_primary_base_update(self):
        """
            Tests scenario creation
        :return:
        """
        pass

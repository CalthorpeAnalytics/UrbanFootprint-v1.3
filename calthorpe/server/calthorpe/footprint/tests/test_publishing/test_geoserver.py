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

from django.utils import unittest
from nose import with_setup
from footprint.publishing.geoserver import validate_geoserver_configuration
from footprint.tests.data_provider import DataProvider

__author__ = 'calthorpe'

class TestGeoserver(unittest.TestCase):

    def setup(self):
        pass

    def teardown(self):
        pass

    @with_setup(setup, teardown)
    def test_geoserver_presentation(self):
        """
            The Geoserver observer classes will create a Presentation and publish DbEntity tables and Media styles for
            each scenarios and projects. Test here to ensure that they are created as expected
        :return:
        """
        scenarios = DataProvider().scenarios()
        smart_scenario = scenarios[0]
        # Assert that the project assets exist
        validate_geoserver_configuration(smart_scenario.project)
        # Assert that a scenario's assets exist
        validate_geoserver_configuration(smart_scenario)

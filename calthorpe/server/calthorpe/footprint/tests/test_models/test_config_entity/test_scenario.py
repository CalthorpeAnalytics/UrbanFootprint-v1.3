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
from footprint.models.database.information_schema import InformationSchema
from footprint.tests.data_provider import DataProvider
from footprint.tests.test_models.test_config_entity.test_config_entity import TestConfigEntity
from footprint.utils.utils import parse_schema_and_table

__author__ = 'calthorpe'

class TestScenario(TestConfigEntity):

    def setup(self):
        super(TestScenario, self).__init__()

    def teardown(self):
        super(TestScenario, self).__init__()

    @with_setup(setup, teardown)
    def test_scenario_creation(self):
        """
            Tests scenario creation
        :return:
        """
        scenarios = DataProvider().scenarios()
        smart_scenario = scenarios[0]
        trend_scenario = scenarios[1]
        project = smart_scenario.project()

        project_geo_json_layers = project.computed_db_entities(tags__tag='geojson')
        assert(len(project_geo_json_layers) > 0)
        # Test that the trend scenario has the geojson layers of the project
        assert(len(trend_scenario.computed_db_entities(tags__tag='geojson')) == len(project_geo_json_layers))
        # Test that the smart scenario has the geojson layers that it registered and those of the project
        assert(len(smart_scenario.computed_db_entities(tags__tag='geojson')) > len(project_geo_json_layers))

        # Verify that the scenarios each have a selected policy_set and built_form_set
        for index, scenario in enumerate(scenarios[0:2]):
            assert(project.computed_policy_sets()[index]==scenarios[index].selected_policy_set())
            assert(project.computed_built_form_sets()[index]==scenarios[index].selected_built_form_set())
            # Expect all the db_entity_interests to be selected since they have unique keys
            # TODO do better testing of key selections
            assert(len(scenario.computed_db_entity_interests())==len(scenarios[index].selected_db_entity_interests()))

            self.assertDbEntityTablesAndSubclasses(scenario)

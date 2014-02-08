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
from datetime import datetime
import random
from time import sleep
from nose import with_setup
from footprint.main.initialization.data_provider import DataProvider
from footprint.main.models.analysis_module.core_module.core import Core
from footprint.main.models.application_initialization import application_initialization
from footprint.main.models.keys.keys import Keys
from footprint.main.tests.test_models.test_config_entity.test_config_entity import TestConfigEntity

__author__ = 'calthorpe_associates'


class TestCore(TestConfigEntity):
    def setup(self):
        super(TestCore, self).__init__()
        application_initialization()

    def teardown(self):
        super(TestCore, self).__init__()

    @with_setup(setup, teardown)
    def test_scenario_core(self):
        """
            Tests scenario creation
        :return:
        """
        scenarios = DataProvider().scenarios()
        scenario = scenarios[0]
        scenario_built_form_feature_manager = scenario.feature_class_of_db_entity_key('scenario_built_form_layer').objects
        built_form_set = scenario.selected_built_form_set()
        built_form_ids = map(lambda built_form: built_form.id, built_form_set.built_form_definitions.all())

        length = scenario_built_form_feature_manager.count()
        assert (length > 0)
        # Dirty up the features
        for scenario_built_form_feature_manager in scenario_built_form_feature_manager.all():
            scenario_built_form_feature_manager.built_form_id = random.choice(built_form_ids)
            scenario_built_form_feature_manager.dirty = True
        scenario_built_form_feature_manager.save()

        core = Core.objects.get(config_entity=scenario)
        timestamp = datetime.now()
        core.start()
        sleep(3)

        # Make sure we have values for all the analysis table classes
        for db_entity_key in [Keys.DB_ABSTRACT_GROSS_INCREMENT_FEATURE, Keys.DB_ABSTRACT_INCREMENT_FEATURE,
                              Keys.DB_ABSTRACT_END_STATE_FEATURE]:
            db_entity = scenario.selected_db_entity(db_entity_key)
            FeatureClass = scenario.feature_class_of_db_entity_key(db_entity_key)
            # Assert that the correct number of rows exist
            assert (FeatureClass.objects.count() == length)
            # Assert that all rows were updated
            assert (len(FeatureClass.objects.filter(updated__gte=timestamp)) == length,
                    "For table {0}.{1}, not all rows were updated by the core, rather {2} out of {3}".format(
                        scenario.schema(),
                        db_entity.table,
                        len(FeatureClass.objects.filter(updated__gte=timestamp)),
                        length))

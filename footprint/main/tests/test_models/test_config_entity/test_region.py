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
from footprint.main.tests.data_provider import DataProvider
from footprint.main.tests.test_models.test_config_entity.test_config_entity import TestConfigEntity
from footprint.main.tests.test_models.test_config_entity.utiltities import SetComparer
from footprint.main.utils.utils import chop_geom
from footprint.main.models.config.global_config import global_config_singleton

__author__ = 'calthorpe_associates'

class TestRegion(TestConfigEntity):

    def setup(self):
        super(TestRegion, self).__init__()

    def teardown(self):
        super(TestRegion, self).__init__()

    @with_setup(setup, teardown)
    def test_region_creation(self):
        """
            Tests the ability to add regions and their relationship with the global_config
        :return:
        """
        regions = DataProvider().regions()
        reduced_config_entity = regions[1]
        parent = global_config_singleton()

        enhanced_config_entity= regions[0]
        # Add a DbEntity to the enhanced_config_entity
        add_db_entity(enhanced_config_entity)

        # Compare the enhanced_config_entity to its parent to ensure that their count of DbEntities with key='geojson_test' differ. This will also temporary add a DbEntity to the parent to ensure that the child adopts it
        SetComparer(
            self,
            parent,
            enhanced_config_entity,
            None,
            'db_entities',
            add_db_entity).compare_sets(db_entity__key='geojson_test')

        SetComparer(self, parent,enhanced_config_entity, reduced_config_entity, 'policy_sets', add_policy_set).compare_sets()
        # Compare the built_form_sets of the two regions to the global_config
        SetComparer(self, parent, enhanced_config_entity, reduced_config_entity, 'built_form_sets', add_built_form_set).compare_sets()

    @with_setup(setup, teardown)
    def test_subregion_creation(self):
        """
            Tests the ability to embed regions with another region
        :return:
        """
        regions = DataProvider().regions()
        enhanced_region = regions[0]
        # Create a subregion with an extra policy_set sired by the enhanced_region
        enhanced_subregion = DataProvider().generate_region(chop_geom(enhanced_region.bounds), enhanced_region)
        enhanced_subregion.add_policy_sets(DataProvider().generate_policy_set())
        enhanced_subregion.save()
        # Create a subregion with a removed policy_set sired by the enhanced_region
        reduced_subregion = DataProvider().generate_region(chop_geom(enhanced_region.bounds), enhanced_region)
        reduced_subregion.remove_policy_sets(reduced_subregion.computed_policy_sets()[0])
        reduced_subregion.save()
        # Confirm that manipulating the parent's policy_sets are reflected in the children
        SetComparer(enhanced_region, enhanced_subregion, reduced_subregion, 'policy_sets', add_policy_set).compare_sets()
        # Now the confirm the relationship to the global_config
        assert len(enhanced_subregion.computed_policy_sets()) == len(global_config_singleton().computed_policy_sets()) + 2
        assert len(reduced_subregion.computed_policy_sets()) == len(global_config_singleton().computed_policy_sets())
        SetComparer(global_config_singleton(), enhanced_subregion, reduced_subregion, 'policy_sets', add_policy_set).confirm_set_added_to_parent(2, 0)

def add_db_entity(config_entity):
    """
        This will create the DbEntity instance and the through instance
    :param config_entity:
    :return:
    """
    return DataProvider().create_geojson_layer_and_associate(config_entity)['layer']

def add_built_form_set(config_entity):
    built_form_set = DataProvider().generate_built_form_set()
    config_entity.add_built_form_sets(built_form_set)
    return built_form_set

def add_policy_set(config_entity):
    policy_set = DataProvider().generate_policy_set()
    config_entity.add_policy_sets(policy_set)
    return policy_set


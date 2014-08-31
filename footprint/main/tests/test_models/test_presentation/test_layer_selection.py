# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
#
# Copyright (C) 2014 Calthorpe Associates
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com

from django.utils import unittest
from django.contrib.gis.geos import MultiPolygon
from nose import with_setup
from footprint.main.initialization.data_provider import DataProvider
from footprint.main.models import LayerLibrary
from footprint.main.models.application_initialization import minimum_initialization
from footprint.main.models.config.global_config import global_config_singleton
from footprint.main.models.keys.keys import Keys
from footprint.main.models.presentation.layer_selection import get_or_create_dynamic_layer_selection_class_and_table
from footprint import settings

__author__ = 'calthorpe_associates'

class TestLayerSelection(unittest.TestCase):

    def setUp(self):
        pass

    def teardown(self):
        pass

    @with_setup(setUp, teardown)
    def test_selection(self):
        # For some reason this module with signal receivers doesn't get imported in the test environment. It does normally
        import footprint.main.publishing

        # Create a test Scenario
        minimum_initialization()
        scenario = DataProvider().scenarios()[0]
        # Fetch a Default Layer Library instance
        layer_library = LayerLibrary.objects.get(key=Keys.LAYER_LIBRARY_DEFAULT, config_entity=scenario)
        # Fetch the layer that displays FutureScenarioFeature DbEntity
        layer = layer_library.presentationmedium_set.filter(db_entity_key=DbEntityKey.FUTURE_SCENARIO).all().select_subclasses()[0]
        # Create the LayerSelection dynamic subclass
        layer_selection_class = get_or_create_dynamic_layer_selection_class_and_table(layer)

        # Get the instance for the user
        user = DataProvider().user()['user']
        user_layer_selection = layer_selection_class.objects.update_or_create(user=user, layer=layer)[0]
        # Set the geography to the whole world. This should cause all features to be added to the features attribute
        user_layer_selection.bounds = global_config_singleton().bounds
        feature_class = user_layer_selection.feature_class()
        # Assert that the features are all selected
        #assert(len(user_layer_selection.features) == len(feature_class.objects.all()))
        assert(len(user_layer_selection.selected_features) == len(feature_class.objects.all()))
        # Clear the SelectionLayer instance
        user_layer_selection.bounds = MultiPolygon([], srid=settings.DEFAULT_SRID)
        # Assert that no features are selected
        assert(len(user_layer_selection.selected_features) == 0)

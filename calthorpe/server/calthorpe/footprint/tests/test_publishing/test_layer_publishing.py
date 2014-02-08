# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
#
# Copyright (C) 2013 Calthorpe Associates
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
from django.core.management import call_command
from django.utils import unittest
from footprint.initialization.fixture import LayerConfigurationFixture
from footprint.initialization.publishing.layer_initialization import LayerLibraryKey, LayerTag
from footprint.initialization.utils import resolve_fixture
from footprint.models import Region
from footprint.models.application_initialization import minimum_initialization
from footprint.models.config.scenario import FutureScenario
from footprint.models.keys.keys import Keys
from nose.tools import assert_equal

class TestLayerPublishing(unittest.TestCase):

    def test_layer_setup(self):
        minimum_initialization()
        region = Region.objects.get()
        # Call footprint_init to update the layer publishing in case something changed since the last test run
        # and we didn't clear the database
        call_command('footprint_init', skip=True, layer=True)
        client_layer_configuration = resolve_fixture(
            "publishing",
            "layer",
            LayerConfigurationFixture,
            region.schema())
        future_scenario = FutureScenario.objects.all()[0]
        layer_library = future_scenario.presentation_set.filter(key=LayerLibraryKey.DEFAULT)[0]
        # Make sure that all client layers exist
        assert_equal(
            len(layer_library.presentationmedium_set.all()),
            len(client_layer_configuration.layers()))
        # Make sure specifically background layers exist
        assert_equal(
            len(layer_library.presentation_media.filter(tag__contains=[LayerTag.BACKGROUND])),
            len(client_layer_configuration.background_layers()))
        # Make sure specifically main layers exist
        assert_equal(
            len(layer_library.presentation_media.filter(tag__contains=[LayerTag.MAIN])),
            len(client_layer_configuration.background_layers()))

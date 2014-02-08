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
from footprint.main.initialization.data_provider import DataProvider
from footprint.main.models import Presentation
from footprint.main.models.application_initialization import minimum_initialization
from footprint.main.models.keys.keys import Keys

__author__ = 'calthorpe_associates'

class TestPresentation(unittest.TestCase):

    def setup(self):
        pass

    def teardown(self):
        pass

    @with_setup(setup, teardown)
    def test_default_map_creation(self):
        scenarios = DataProvider().scenarios()
        smart_scenario = scenarios[0]
        # Assert that the Scenario has its default map presentation and not that of its parent
        assert len(smart_scenario.presentation_set.filter(key=Keys.LAYER_LIBRARY_DEFAULT)) == 1
        assert smart_scenario.presentation_set.get(key=Keys.LAYER_LIBRARY_DEFAULT).pk != smart_scenario.parent_config_entity.presentation_set.get(key=Keys.LAYER_LIBRARY_DEFAULT).pk

    @with_setup(setup, teardown)
    def test_presentation_config_entities(self):
        minimum_initialization()
        DataProvider().scenarios()
        presentations = Presentation.objects.all()
        for presentation in presentations:
            assert presentation.subclassed_config_entity, "Presentation {0} has no config_entity".format(presentation)

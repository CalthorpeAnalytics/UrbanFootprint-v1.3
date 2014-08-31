# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
#
# Copyright (C) 2012 Calthorpe Associates
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
from nose.tools import assert_equal
from django.utils.datetime_safe import strftime
from django.utils.timezone import now
from footprint.main.models import Presentation
from footprint.main.models.application_initialization import application_initialization, minimum_initialization
from footprint.main.models.config.scenario import FutureScenario

__author__ = 'calthorpe_associates'

from django.utils import unittest

__author__ = 'calthorpe_associates'

class TestConfigEntity(unittest.TestCase):

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_clone(self):
        minimum_initialization()
        scenario = FutureScenario.objects.all()[0]
        key = strftime(now(), '%Y_%m_%d_%H_%M_%S')
        future_scenario = FutureScenario(
            parent_config_entity=scenario.project,
            origin_instance=scenario,
            year=scenario.year,
            name=key,
            description='Clone of %s' % scenario.name,
            bounds=scenario.bounds,
            key=key
        )
        future_scenario.save()
        assert_equal(len(scenario.computed_built_form_sets()), len(future_scenario.computed_built_form_sets()))
        assert_equal(len(scenario.computed_policy_sets()), len(future_scenario.computed_policy_sets()))
        assert_equal(len(scenario.computed_db_entity_interests()), len(future_scenario.computed_db_entity_interests()))
        assert_equal(len(Presentation.objects.filter(config_entity=scenario)), len(Presentation.objects.filter(config_entity=future_scenario)))

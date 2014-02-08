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
from optparse import make_option
from random import randrange
import logging

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from footprint.models import Placetype
from footprint.models.analysis_module.core import executeCore
from footprint.models.application_initialization import application_initialization, create_data_provider_data
from footprint.models.config.scenario import FutureScenario
from footprint.models.keys.keys import Keys


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
        This command initializes/syncs the footprint server with default and sample data. I'd like this to happen automatically in response to the post_syncdb event, but that event doesn't seem to fire (see management/__init__.py for the attempted wiring)
    """
    option_list = BaseCommand.option_list + (
        make_option('-r', '--resave', action='store_true', default=False,
                    help='Resave all the config_entities to trigger signals'),
        make_option('-s', '--skip', action='store_true', default=False,
                    help='Skip initialization and data creation (for just doing resave)'),
        make_option('--scenario', default='', help='String matching a key of or more Scenario to run'),
    )

    def handle(self, *args, **options):
        if not options['skip']:
            application_initialization()
            create_data_provider_data()

        scenarios = FutureScenario.objects.filter(key__contains=options['scenario']) if options[
            'scenario'] else FutureScenario.objects.all()
        for scenario in scenarios:
            ScenarioBuiltFormFeatureSubclass = scenario.feature_class_of_db_entity(
                Keys.DB_ABSTRACT_FUTURE_SCENARIO_FEATURE)
            scenario_built_form_features = ScenarioBuiltFormFeatureSubclass.objects.all()
            built_forms = Placetype.objects.all()
            for scenario_built_form_feature in scenario_built_form_features.all():
                scenario_built_form_feature.built_form = built_forms[randrange(0, len(built_forms) - 1)]
                scenario_built_form_feature.dirty = True
                scenario_built_form_feature.save()

            user = User.objects.all()[0]
            executeCore.delay(user, scenario)
            #async_result = executeCore.delay(user, scenario)
            #logger.warn("Status" + async_result.status)
            #core = Core.objects.update_or_create(config_entity=scenario)
            #core.start()



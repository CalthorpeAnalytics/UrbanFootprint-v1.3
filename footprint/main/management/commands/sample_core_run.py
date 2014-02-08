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

from footprint.main.models import Placetype
from footprint.main.models.analysis_module.core_module.core import executeCore
from footprint.main.models.analysis_module.fiscal_module.fiscal import Fiscal, executeFiscal
from footprint.main.models.analysis_module.vmt_module.vmt import Vmt, executeVmt
from footprint.main.models.application_initialization import application_initialization, create_data_provider_data
from footprint.main.models.config.scenario import FutureScenario, Scenario
from footprint.main.models.keys.keys import Keys


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
        make_option('--core', action='store_true', default=False, help='Run core'),
        make_option('--fiscal', action='store_true', default=False, help='Run fiscal'),
        make_option('--vmt', action='store_true', default=False, help='Run VMT'),
        make_option('--scenario', default='', help='String matching a key of or more Scenario to run')
    )

    def handle(self, *args, **options):
        if not options['skip']:
            application_initialization()
            create_data_provider_data()

        scenarios = FutureScenario.objects.filter(key__contains=options['scenario']) if options[
            'scenario'] else FutureScenario.objects.all()

        all_scenarios = Scenario.objects.all()

        user = User.objects.all()[0]
        for scenario in scenarios:
            if options['core']:
                future_scenario_feature_class = scenario.feature_class_of_db_entity_key(
                    Keys.DB_ABSTRACT_FUTURE_SCENARIO_FEATURE)
                future_scenario_features = future_scenario_feature_class.objects.all()
                built_forms = Placetype.objects.all()
                for scenario_built_form_feature in future_scenario_features.filter()[:100]:
                    scenario_built_form_feature.built_form = built_forms[randrange(0, len(built_forms) - 1)]
                    scenario_built_form_feature.dirty = True
                    scenario_built_form_feature.save()
                executeCore(None, user, scenario)

            if options['fiscal']:
                fiscal = Fiscal.objects.update_or_create(config_entity=scenario)[0]
                fiscal.start(user.id)

        if options['vmt']:
            for scenario in all_scenarios:
                executeVmt(None, user, scenario)
                # vmt = Vmt.objects.update_or_create(config_entity=scenario)[0]
                # vmt.start(user.id)





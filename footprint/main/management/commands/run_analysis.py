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
import datetime
import uuid

from django.core.management.base import BaseCommand
from django.utils.timezone import utc

from footprint.main.models import CropType, Job
from footprint.main.models.analysis_module.analysis_module import AnalysisModuleKey, AnalysisModule
from footprint.main.models.analysis_module.energy_module.test_energy import test_execute_energy
from footprint.main.models.analysis_module.vmt_module.test_vmt import test_execute_vmt
from footprint.main.models.analysis_module.water_module.test_water import test_execute_water
from footprint.main.models.application_initialization import application_initialization, \
    update_or_create_config_entities
from footprint.main.models.config.scenario import FutureScenario, Scenario, BaseScenario
from footprint.main.models.geospatial.db_entity_keys import DbEntityKey


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
        make_option('--energy', action='store_true', default=False, help='Run Energy'),
        make_option('--water', action='store_true', default=False, help='Run Water'),
        make_option('--rucs', action='store_true', default=False, help='Run AG'),
        make_option('--constraint', action='store_true', default=False, help='Run Environmental Constraints'),
        make_option('--test', action='store_true', default=False, help='setup test data before running'),
        make_option('--all', action='store_true', default=False, help='runs all analysis modules'),

        make_option('--scenario', default='', help='String matching a key of or more Scenario to run')
    )

    def handle(self, *args, **options):
        from django.contrib.auth.models import User
        user = User.objects.filter()[0]
        if not options['skip']:
            application_initialization()
            update_or_create_config_entities()

        scenarios = FutureScenario.objects.filter(key__contains=options['scenario']) if options[
            'scenario'] else FutureScenario.objects.all()

        all_scenarios = Scenario.objects.all()

        for scenario in scenarios:
            if options['core'] or options['all']:
                from footprint.main.models import Placetype
                end_state_feature_class = scenario.db_entity_feature_class(
                    DbEntityKey.END_STATE)
                future_scenario_features = end_state_feature_class.objects.all()
                built_forms = Placetype.objects.all()
                for scenario_built_form_feature in future_scenario_features.filter()[:100]:
                    scenario_built_form_feature.built_form = built_forms[randrange(0, len(built_forms) - 1)]
                    scenario_built_form_feature.dirty = True
                    scenario_built_form_feature.save()

                end_state_feature_class.post_save(user.id, end_state_feature_class.objects.all())

                # job = Job(user=user, hashid=uuid.uuid4(), type="Core")
                # job.save()
                # kwargs = dict(
                #     user=user,
                #     job=job,
                #     analysis_module=AnalysisModule.objects.get(
                #         config_entity=config_entity,
                #         key=AnalysisModuleKey.CORE)
                # )
                # execute_core(scenario, **kwargs)
                # job.status = "Complete"
                # job.save()


            if options['fiscal'] or options['all']:
                job = Job(user=user, hashid=uuid.uuid4(), type="Fiscal")
                job.save()
                kwargs = dict(
                    user=user,
                    job=job,
                    analysis_module=AnalysisModule.objects.get(
                        config_entity=scenario,
                        key=AnalysisModuleKey.FISCAL)
                )
                AnalysisModule.objects.get(config_entity=scenario, key=AnalysisModuleKey.FISCAL).update(**kwargs)


        if options['constraint'] or options['all']:
            pass
            # initialize(one_scenario)

        for scenario in all_scenarios:
            if options['energy'] or options['all']:
                test_execute_energy(scenario)

            if options['water'] or options['all']:
                test_execute_water(scenario)

            if options['vmt'] or options['all']:
                test_execute_vmt(scenario)

            if options['rucs'] or options['all']:
                job = Job(user=user, hashid=uuid.uuid4(), type="Agriculture")
                job.save()
                kwargs = dict(
                    user=user,
                    job=job,
                    analysis_module=AnalysisModule.objects.get(
                        config_entity=scenario,
                        key=AnalysisModuleKey.AGRICULTURE)
                )
                if isinstance(scenario.subclassed_config_entity, BaseScenario):
                    ag_scenario_feature_class = scenario.db_entity_feature_class(
                        DbEntityKey.BASE_AGRICULTURE)
                else:
                    ag_scenario_feature_class = scenario.db_entity_feature_class(
                        DbEntityKey.FUTURE_AGRICULTURE)

                if options['test']:
                    if ag_scenario_feature_class.objects.count() > 1000:
                        ag_features = ag_scenario_feature_class.objects.all()[:1000]
                    else:
                        ag_features = ag_scenario_feature_class.objects.all()
                    for f in ag_features:
                        f.dirty_flag = True
                        f.built_form = CropType.objects.all()[randrange(0, CropType.objects.count())]
                        f.save()

                else:

                    ag_scenario_feature_class.post_save(user.id, ag_scenario_feature_class.objects.all())

                # AnalysisModule.objects.get(key=AnalysisModuleKey.AGRICULTURE, config_entity=scenario).test_agriculture_core(**kwargs)








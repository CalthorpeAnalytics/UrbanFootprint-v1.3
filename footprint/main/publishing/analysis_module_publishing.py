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
import logging
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from footprint.main.lib.functions import remove_keys
from footprint.main.models.analysis_module.analysis_tool import AnalysisTool
from footprint.main.models.config.project import Project
from footprint.main.models.analysis_module.analysis_module import AnalysisModule
from footprint.main.models.config.scenario import Scenario
from footprint.main.utils.subclasses import receiver_subclasses

__author__ = 'calthorpe_associates'

logger = logging.getLogger(__name__)


def on_config_entity_post_save_analysis_modules(sender, **kwargs):
    """
        Sync a ConfigEntity's ResultPage presentation
    """
    config_entity = kwargs['instance']
    logger.debug("\t\tHandler: on_config_entity_post_save_analysis_module. ConfigEntity: %s" % config_entity.name)
    update_or_create_analysis_modules(config_entity, **kwargs)


def update_or_create_analysis_modules(config_entity, **kwargs):
    """
        Creates a results library and Result instances upon saving a config_entity if they do not yet exist.
    :param config_entity
    :return:
    """
    from footprint.client.configuration.fixture import ConfigEntityFixture

    if isinstance(config_entity, Scenario) or isinstance(config_entity, Project):
        client_fixture = ConfigEntityFixture.resolve_config_entity_fixture(config_entity)

        for analysis_module_configuration in client_fixture.default_analysis_module_configurations():

            # Create the table the first time
            analysis_module, created, updated = AnalysisModule.objects.update_or_create(
                config_entity=config_entity,
                key=analysis_module_configuration.key,
                defaults=dict(
                    name=analysis_module_configuration.name,
                    description=analysis_module_configuration.description,
                    configuration=remove_keys(analysis_module_configuration.configuration, ['key', 'name', 'description']))
            )

            # TODO this should be the admin user
            if not analysis_module.updater:
                analysis_module.updater = User.objects.all()[0]
            if not analysis_module.creator:
                analysis_module.creator = analysis_module.updater
            # update_or_create will kick off the run for updates.
            # don't let it run here
            previous = analysis_module._no_post_save_task_run
            analysis_module._no_post_save_task_run = True
            analysis_module.save()
            analysis_module._no_post_save_task_run = previous
            analysis_module.init()

def on_db_entity_post_save_analysis_modules(sender, **kwargs):
    """
    Respond to whenever a db entity is added or updated
    :return:
    """
    db_entity_interest = kwargs['instance']
    behavior = db_entity_interest.db_entity.feature_behavior.behavior
    main_config_entity = db_entity_interest.config_entity
    # Todo children() should be all_scenario_descendents or similar to handle region
    config_entities = [main_config_entity] if isinstance(main_config_entity, Scenario) else [main_config_entity]+list(main_config_entity.children())

    for config_entity in config_entities:
        analysis_modules = config_entity.analysis_modules
        for analysis_module in analysis_modules:
            for analysis_tool in analysis_module.analysis_tools.all().select_subclasses():
                # If the tool matches the behavior, update the tool
                if analysis_tool.behavior and analysis_tool.behavior.has_behavior(behavior):
                    logger.info("Updating AnalysisTool %s for AnalysisModule %s for ConfigEntity %s" % \
                                (analysis_tool.key, analysis_module.key, config_entity.name))
                    analysis_tool.update()

def on_config_entity_pre_delete_analysis_modules(sender, **kwargs):
    config_entity = kwargs['instance']
    AnalysisModule.objects.filter(config_entity=config_entity).delete()
    AnalysisTool.objects.filter(config_entity=config_entity).delete()

@receiver_subclasses(post_save, AnalysisModule, "analysis_module_post_save")
def on_analysis_module_post_save(sender, **kwargs):
    analysis_module = kwargs['instance']
    if not kwargs.get('created', None):
        # Automatically start the analysis module on update since the client simply updates the
        # analysis module to force it to run.
        # If already started, don't start again. Saves happen during the task run in order
        # to update the analysis_module timestamps
        # The instance flag is used by post_save_config_entity_publishing to turn it off
        if not analysis_module._started and \
                not analysis_module._no_post_save_task_run and \
                not AnalysisModule._no_post_save_task_run_global:
            analysis_module.start()

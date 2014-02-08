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
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import DatabaseError
from django.db.models.signals import pre_delete
from footprint.lib.functions import merge
from footprint.models import ConfigEntity, GlobalConfig, Scenario, Region, Project, Presentation, BuiltForm, Layer
from footprint.models.application_initialization import application_initialization, create_data_provider_data, initialize_default_media, initialize_geography_data
from footprint.models.config.global_config import global_config_singleton
from footprint.models.config.scenario import BaseScenario, FutureScenario, resolve_config_entity
from footprint.models.presentation.layer_selection import create_dynamic_layer_selection_class_and_table, drop_layer_selection_table
from footprint.models.signals import post_post_save_config_entity, initialize_presentations
import logging
from footprint.publishing import data_import, layer_publishing, result, built_form_publishing, tilestache
from footprint.publishing.data_import import on_config_entity_post_save_data_import

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
        This command initializes/syncs the footprint server with default and sample data. I'd like this to happen
        automatically in response to the post_syncdb event, but that event doesn't seem to fire
        (see management/__init__.py for the attempted wiring)
    """
    option_list = BaseCommand.option_list + (
        # The following allow you to turn off publishers that are part of the initialization
        make_option('--nolayer', action='store_true', default=False, help='Skip layer publishing'),
        make_option('--noimport', action='store_true', default=False, help='Skip data import'),
        make_option('--notilestache', action='store_true', help='Skip tilestache'),
        make_option('--nobuiltforms', action='store_true', help='Skips the builtform setup and updating'),

        # If skip is not specified, the full application initialization will occur
        # Use skip with the options below to limit initialization
        make_option('--skip', action='store_true', default=False,
                    help='Skip initialization and data creation (for just doing resave)'),

        make_option('--initializers', action='store_true', default=False,
                    help='Rerun application initializers'),
        make_option('--tilestache', action='store_true', default=False,
                    help='Republish all tilestache configurations'),
        make_option('--results', action='store_true', default=False, help='Republish all result configurations'),
        make_option('--data_import', action='store_true', default=False, help="Explicitly run the data import"),
        make_option('--addnew', action='store_true', default=False,
                    help='Add new config_entity configurations, namely default db_entities'),
        make_option('--deleteorphans', action='store_true', default=False, help='Delete orphan instances'),
        make_option('--recreate', action='store_true', default=False,
                    help='Rerun the config_entity recreate code, creating db_entities, schemas and their data if missing'),

        # Limit which projects and scenarios are acted upon
        # TODO not implemented
        make_option('--projects', help='Comma separated project key list to init. The default it all'),
        make_option('--scenarios', help='Comma separated scenario key list to init. The default is all'),
        make_option('--built_forms', action='store_true', default=False, help='Update the built forms'),
        make_option('--layer', action='store_true', default=False, help='Update the layer'),

        make_option('--db_entity_keys', help='Comma separated db_entity key list to init to limit data import to given keys'),
        make_option('--destroy_layer_selection_tables', action='store_true', help='Deletes all layer_selection tables (so they can be recreated)'),
        make_option('--resave', action='store_true', default=False,
                help='Resave all the config_entities to trigger signals')
    )

    def handle(self, *args, **options):

        project_keys = options.get('projects', []).split(',') if options['projects'] else None
        scenario_keys = options.get('scenarios', []).split(',') if options['scenarios'] else None
        db_entity_keys = options.get('db_entity_keys', []).split(',') if options['db_entity_keys'] else None

        project_filter = dict(key__in=project_keys) if project_keys else dict()
        scenario_filter = merge(
            dict(parent_config_entity__key__in=project_keys) if project_keys else dict(),
            dict(key__in=scenario_keys) if scenario_keys else dict())

        #
        # Recreation Stuff
        #
        if options['recreate']:
            global_config_singleton().post_create()
            for region in Region.objects.all():
                logger.info('Creating region {config_entity}'.format(config_entity=region.name))
                region.post_create()
            for project in Project.objects.filter(**project_filter):
                logger.info('Creating project {config_entity}'.format(config_entity=project.name))
                project.post_create()
            for scenario in BaseScenario.objects.filter(**scenario_filter):
                logger.info('Creating base scenario {config_entity}'.format(config_entity=scenario.name))
                scenario.post_create()
            for scenario in FutureScenario.objects.filter(**scenario_filter):
                logger.info('Creating base scenario {config_entity}'.format(config_entity=scenario.name))
                scenario.post_create()

        if options['destroy_layer_selection_tables']:
            try:
                layers = Layer.objects.all()

                for selection_layer in layers:
                    # Drop the table
                    layer_selection_class = create_dynamic_layer_selection_class_and_table(selection_layer, True)
                    layer_selection_features_class = layer_selection_class.features.through
                    drop_layer_selection_table(layer_selection_features_class)
                    drop_layer_selection_table(layer_selection_class)
                    # Recreate
                    create_dynamic_layer_selection_class_and_table(selection_layer)
            except DatabaseError, e:
                logger.warning("Couldn't destroy LayerSelection tables. Maybe the public.layer table no longer exists: %s" % e.message)

        # Publishing disabling stuff
        #

        if options['noimport']:
            # Skip long importing
            for cls in [FutureScenario, BaseScenario, Project, Region]:
                post_post_save_config_entity.disconnect(data_import.on_config_entity_post_save_data_import, cls, True,
                                                        "data_import_on_config_entity_post_save")
                pre_delete.disconnect(data_import.on_config_entity_pre_delete_data_import, cls, True,
                                      "data_import_on_config_entity_pre_delete")
        if options['nolayer']:
            # Skip long importing
            for cls in [FutureScenario, BaseScenario, Project, Region]:
                post_post_save_config_entity.disconnect(layer_publishing.on_config_entity_post_save_layer, cls, True,
                                                        "layer_on_config_entity_post_save")
                pre_delete.disconnect(layer_publishing.on_config_entity_pre_delete_layer, cls, True,
                                      "layer_on_config_entity_pre_delete")

        if options['notilestache']:
            for cls in [FutureScenario, BaseScenario, Project, Region]:
                post_post_save_config_entity.disconnect(tilestache.on_config_entity_post_save_tilestache, cls, True,
                                                        "tilestache_on_config_entity_post_save")
                pre_delete.disconnect(tilestache.on_config_entity_pre_delete_tilestache, cls, True,
                                      "tilestache_on_config_entity_pre_delete")

        if options['nobuiltforms']:
            # Skip builtform publishing
            post_post_save_config_entity.disconnect(built_form_publishing.on_config_entity_post_save_built_form, GlobalConfig, True,
                                  "built_form_on_config_entity_post_save")

        # If skip is not specified, the full application initialization will occur
        # Use skip with the options below to limit initialization
        if not options['skip']:
            application_initialization()
            create_data_provider_data()

        if options['initializers']:
            # Redo initializers
            initialize_default_media()
            initialize_geography_data()

        if options['addnew']:
            # Pick up new stuff in the config_entity configurations, namely default db_entities
            for config_entity in ConfigEntity.objects.select_subclasses():
                config_entity.sync_default_db_entities()
        if options['resave']:
            for config_entity in Region.objects.all():
                logger.info('Re-saving region {config_entity}'.format(config_entity=config_entity.name))
                config_entity.save()
            for config_entity in Project.objects.filter(**project_filter):
                logger.info('Re-saving project {config_entity}'.format(config_entity=config_entity.name))
                config_entity.save()
            for config_entity in BaseScenario.objects.filter(**scenario_filter):
                logger.info('Re-saving base scenario {config_entity}'.format(config_entity=config_entity.name))
                config_entity.save()
            for config_entity in FutureScenario.objects.filter(**scenario_filter):
                logger.info('Re-saving future scenario {config_entity}'.format(config_entity=config_entity.name))
                config_entity.save()

        # Manually invoke the tilestache publisher on each config_entity.
        if options['layer']:
            for config_entity in all_config_entities():
                layer_publishing.on_config_entity_post_save_layer(None, instance=resolve_config_entity(config_entity))
        if options['tilestache']:
            for config_entity in ConfigEntity.objects.select_subclasses():
                tilestache.on_config_entity_post_save_tilestache(None, instance=resolve_config_entity(config_entity))
        if options['results']:
            for config_entity in ConfigEntity.objects.select_subclasses():
                result.on_config_entity_post_save_result(None, instance=resolve_config_entity(config_entity))
        if options['built_forms']:
            import footprint.publishing
            global_config = global_config_singleton()
            built_form_publishing.on_config_entity_post_save_built_form(None, instance=resolve_config_entity(global_config))
        if options['data_import']:
            for config_entity in Project.objects.filter():
                on_config_entity_post_save_data_import(None, instance=config_entity)

        call_command('collectstatic', interactive=False)

def all_config_entities():
    config_entities = ConfigEntity.objects.select_subclasses()
    return map(
        lambda config_entity: resolve_scenario(config_entity) if isinstance(config_entity, Scenario) else config_entity,
        config_entities
    )
def resolve_scenario(scenario):
    for scenario_type in ['basescenario', 'futurescenario']:
        if hasattr(scenario, scenario_type):
            return getattr(scenario, scenario_type)
    return scenario

def config_entity_classes():
    return [BaseScenario, FutureScenario] + Scenario.lineage()


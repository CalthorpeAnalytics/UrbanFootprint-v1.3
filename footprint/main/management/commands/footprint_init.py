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
import logging
from cProfile import Profile
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import DatabaseError
from footprint.client.configuration.fixture import ConfigEntitiesFixture
from footprint.main.initialization.data_provider import DataProvider

from footprint.main.lib.functions import merge
from footprint.main.models import DbEntityInterest
from footprint.main.models.config.config_entity import ConfigEntity
from footprint.main.models.config.global_config import GlobalConfig
from footprint.main.models.config.region import Region
from footprint.main.models.config.project import Project
from footprint.main.models.database.information_schema import InformationSchema, PGNamespace
from footprint.main.models.keys.keys import Keys
from footprint.main.models.presentation.layer import Layer
from footprint.main.models.geospatial.db_entity import DbEntity
from footprint.main.models.application_initialization import application_initialization, initialize_default_media, recalculate_project_bounds
from footprint.main.models.config.global_config import global_config_singleton
from footprint.main.models.config.scenario import BaseScenario, FutureScenario, Scenario
from footprint.main.models.presentation.layer_selection import get_or_create_dynamic_layer_selection_class_and_table, drop_layer_selection_table
from footprint.client.configuration import resolve_fixture, InitFixture
from footprint import settings


from footprint.main.publishing import data_import_publishing, layer_publishing, result_publishing, analysis_module_publishing, built_form_publishing, tilestache_publishing, db_entity_publishing, policy_publishing

from footprint.main.publishing.config_entity_publishing import post_save_config_entity_db_entities, post_save_config_entity_initial, post_save_config_entity_layers
from footprint.main.publishing.data_import_publishing import on_config_entity_post_save_data_import
from footprint.main.publishing.db_entity_publishing import update_or_create_db_entity_and_interest
from footprint.main.publishing.layer_publishing import update_or_create_layer, clone_or_update_cloned_layer
from footprint.main.utils.dynamic_subclassing import create_tables_for_dynamic_classes, drop_tables_for_dynamic_classes
from footprint.main.utils.utils import resolve_model, map_property_path
from footprint.main.models.geospatial.feature_class_creator import FeatureClassCreator

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    """
        This command initializes/syncs the footprint server with default and sample data. I'd like this to happen
        automatically in response to the post_syncdb event, but that event doesn't seem to fire
        (see management/__init__.py for the attempted wiring)
    """
    option_list = BaseCommand.option_list + (
        # The following allow you to turn off publishers that are part of the initialization
        make_option('--nolayer', action='store_true', default=False, help='Skips layer publisher'),
        make_option('--noimport', action='store_true', default=False, help='Skips data import publisher'),
        make_option('--noinitializer', action='store_true', default=False, help='Skips initializer publishers'),
        make_option('--notilestache', action='store_true', help='Skips tilestache publisher'),
        make_option('--nobuilt_form', action='store_true', help='Skips built_form publisher'),
        make_option('--nosproutore', action='store_true', help='Skips sproutcore publisher'),
        make_option('--noresult', action='store_true', help='Skips result publisher'),
        make_option('--nodb_entity', action='store_true', help='Skips db_entity publisher'),

        # If skip is not specified, the full application initialization will occur
        # Use skip with the options below to limit initialization
        make_option('--skip', action='store_true', default=False,
                    help='Skip initialization and data creation (for just doing resave)'),
        # Use this to skip config_entities and save all db_entity_interests directly
        make_option('--save_db_entity_interests', action='store_true', default=False,
                    help="Saves the db_entity_interests directly to run their publishers, instead of going through the config_entities"),

        make_option('--recreate', action='store_true', default=False,
                    help='Deletes model instances prior to anything else'),
        make_option('--resave', action='store_true', default=False,
                    help='Resave all the config_entities to trigger signals'),
        make_option('--reimport', action='store_true', default=False,
                    help='Delete imported feature tables and reimport'),
        make_option('--recalculate_bounds', action='store_true', default=False,
                    help='Recalculates the project bounds'),

        make_option('--initializer', action='store_true', default=False,
                    help='Rerun application initializers'),
        make_option('--tilestache', action='store_true', default=False,
                    help='Explicitly run tilestache publisher'),
        make_option('--result', action='store_true', default=False, help='Explicitly run result publisher'),
        make_option('--policy', action='store_true', default=False, help='Explicitly run policy publisher'),
        make_option('--import', action='store_true', default=False, help="Explicitly run data_import publisher"),
        make_option('--db_entity', action='store_true', default=False,
                    help='Rerun through default db_entities to pick up configuration changes'),
        make_option('--built_form', action='store_true', default=False, help='Explicitly run built_form publisher'),
        make_option('--layer', action='store_true', default=False, help='Explicitly run layer publisher'),
        make_option('--analysis', action='store_true', default=False, help='Explicitly run analysis publisher'),
        make_option('--recreate_layer', action='store_true', default=False, help='Delete all layers and then explicitly run layer publisher'),
        make_option('--selections', action='store_true', help='Reset config_enitty selections', default=False),

        make_option('--test_clone_scenarios', action='store_true', help='Clone scenarios to simulate a UI clone', default=False),
        make_option('--test_upload_layers', action='store_true', help='Upload layers to simulate a UI upload', default=False),
        make_option('--test_layer_from_selection', action='store_true', help='Tests creating a layer/db_entity from from a selection', default=False),
        make_option('--inspect', action='store_true', help='Specify DbEntity key(s) with db_entity_keys to inspect feature class info about it/them'),

        # Limit which projects and scenarios are acted upon
        # TODO not implemented
        make_option('--projects', help='Comma separated project key list to init. The default it all'),
        make_option('--scenarios', help='Comma separated scenario key list to init. The default is all'),

        # Limit which db_entities are acted on, where aplicable
        make_option('--db_entity_keys', help='Comma separated db_entity key list to init to limit data import to given keys'),

        make_option('--recycle', action='store_true', default=False, help='Delete config_entities marked deleted'),
        make_option('--delete_clones', action='store_true', default=False, help='Deletes cloned scenarios, db_entities, and layers'),

        make_option('--relayer_selection', action='store_true', help='Recreates all layer selections'),

        make_option('--class', help='Comma separated classes in the form FutureScenario, Project, etc'),
        make_option('--profile', action='store_true', help='Profile the command', default=False),
        make_option('--memory', action='store_true', help='Profile the command', default=False)
    )

    def handle(self, *args, **options):

        if options['profile']:
            profiler = Profile()
            profiler.runcall(self._handle, *args, **options)
            profiler.print_stats()
        else:
            self._handle(*args, **options)


    def _handle(self, *args, **options):
        project_keys = options.get('projects', []).split(',') if options['projects'] else None
        scenario_keys = options.get('scenarios', []).split(',') if options['scenarios'] else None
        db_entity_keys = options.get('db_entity_keys', []).split(',') if options['db_entity_keys'] else None

        project_filter = dict(key__in=project_keys) if project_keys else dict()
        scenario_filter = merge(
            dict(parent_config_entity__key__in=project_keys) if project_keys else dict(),
            dict(key__in=scenario_keys) if scenario_keys else dict())
        limit_to_classes = map(
            lambda cls: resolve_model('main.%s' % cls), (options['class'].split(',') if options['class'] else [])
        )

        # Perforance testing
        if options['memory']:
            ConfigEntity.init_heapy()
            ConfigEntity.start_heapy_diagnosis()

        # Delete all ConfigEntity intances so they can be recreated.
        # This will cascade delete related models, but it doesn't delete
        # BuiltForms and other independent models
        if options['recreate']:
            for cls in filter_classes(limit_to_classes):
                cls.objects.all().delete()

        # Delete deleted config_entities
        if options['recycle']:
            for cls in filter_classes(limit_to_classes):
                cls.objects.filter(deleted=True).delete()
        if options['delete_clones']:
            for cls in filter_classes(limit_to_classes):
                all_config_entities = cls.objects.all()
                for config_entity in all_config_entities:
                    db_entities = filter(
                        lambda db_entity: db_entity.feature_class_configuration and db_entity.feature_class_configuration.get('generated', None),
                        map(
                            lambda db_entity_interest: db_entity_interest.db_entity,
                            DbEntityInterest.objects.filter(config_entity=config_entity)))
                    Layer.objects.filter(presentation__config_entity=config_entity, db_entity_key__in=map(lambda db_entity: db_entity.key, db_entities)).delete()
                    for db_entity in db_entities:
                        feature_class = FeatureClassCreator(config_entity, db_entity).dynamic_feature_class()
                        if InformationSchema.objects.table_exists(db_entity.schema, db_entity.table):
                            drop_tables_for_dynamic_classes(feature_class.__base__, feature_class)
                        db_entity.delete()
                cloned_config_entities = cls.objects.filter(origin_config_entity__isnull=False)
                for config_entity in cloned_config_entities:
                    PGNamespace.objects.drop_schema(config_entity.schema())
                cloned_config_entities.delete()

        if options['save_db_entity_interests']:
            # Save just existing db_entity_interests--invoke dependent publishers
            for config_entity in filter_config_entities(limit_to_classes):
                for db_entity_interest in config_entity.owned_db_entity_interests(**dict(db_entity__key__in=db_entity_keys) if db_entity_keys else {}):
                    db_entity_interest.save()

        else:
            # Default, run through everything, creating/updating config_entities and running
            # Dependent publishers that are not explictly disabled
            if not options['skip']:
                if options['nodb_entity']:
                    for cls in filter_classes(limit_to_classes):
                        post_save_config_entity_initial.disconnect(db_entity_publishing.on_config_entity_post_save_db_entity, cls, True,
                                                                   "db_entity_on_config_entity_post_save")

                if options['noimport']:
                    # Skip long importing
                    for cls in filter_classes(limit_to_classes):
                        post_save_config_entity_db_entities.disconnect(data_import_publishing.on_config_entity_post_save_data_import, cls, True,
                                                                       "data_import_on_config_entity_post_save")

                if options['nolayer']:
                    for cls in [FutureScenario, BaseScenario, Project, Region]:
                        post_save_config_entity_db_entities.disconnect(layer_publishing.on_config_entity_post_save_layer, cls, True,
                                                                       "layer_on_config_entity_post_save")

                if options['noresult']:
                    for cls in [FutureScenario, BaseScenario, Project, Region]:
                        post_save_config_entity_db_entities.disconnect(result_publishing.on_config_entity_post_save_result, cls, True,
                                                                       "result_on_config_entity_post_save")

                if options['notilestache']:
                    for cls in [FutureScenario, BaseScenario, Project, Region]:
                        post_save_config_entity_layers.disconnect(tilestache_publishing.on_config_entity_post_save_tilestache, cls, True,
                                                                  "tilestache_on_config_entity_post_save")

                if options['nobuilt_form']:
                    # Skip builtform publishing
                    for cls in [FutureScenario, BaseScenario, Project, Region, GlobalConfig]:
                        post_save_config_entity_initial.disconnect(built_form_publishing.on_config_entity_post_save_built_form, cls, True,
                                                                   "built_form_publishing_on_config_entity_post_save")
                # If skip is not specified, the full application initialization will occur
                # Use skip with the options below to limit initialization
                application_initialization(limit_to_classes=limit_to_classes)
            else:
                # If skip is specified, use one or more of the following options
                # to run publishers directly for all or filtered config_entities

                if options['initializer']:
                    # Redo initializers. This is non-config_entity dependent stuff,
                    # like default style templates
                    initialize_default_media()
                    client_init = resolve_fixture(None, "init", InitFixture, settings.CLIENT)
                    client_init.populate_models()

                if options['db_entity']:
                    # Pick up new stuff in the config_entity configurations, namely default db_entities
                    #for config_entity in filter_config_entities(limit_to_classes):
                    #    db_entity_publishing.update_or_create_db_entities(config_entity)
                    missing_schemas = filter(lambda x: not x.schema, DbEntity.objects.all())
                    if missing_schemas:
                        logger.error("No schemas for the following db_entities %s" % map_property_path(missing_schemas, 'name'))

                if options['built_form']:
                    for config_entity in filter_config_entities(limit_to_classes):
                        built_form_publishing.on_config_entity_post_save_built_form(None, instance=config_entity)

                if options['import']:
                    for config_entity in filter_config_entities(limit_to_classes):
                        on_config_entity_post_save_data_import(None, instance=config_entity)
                elif options['reimport']:
                    for config_entity in filter_config_entities(limit_to_classes):
                        # Use the predelete to drop the tables
                        data_import_publishing.on_config_entity_pre_delete_data_import(None, instance=config_entity, db_entity_keys=db_entity_keys)
                        # Reimport the db_entity tables for the specified config_entities/db_entity_keys
                        data_import_publishing.on_config_entity_post_save_data_import(None, instance=config_entity, db_entity_keys=db_entity_keys)

                if options['analysis']:
                    for config_entity in filter_config_entities(limit_to_classes):
                        analysis_module_publishing.on_config_entity_post_save_analysis_modules(None, instance=config_entity)

                if options['layer'] or options['recreate_layer'] or options['relayer_selection']:
                    for config_entity in filter_config_entities(limit_to_classes):
                        if options['recreate_layer']:
                            layers = Layer.objects.filter(**merge(dict(presentation__config_entity=config_entity),
                                                                  dict(db_entity_key__in=db_entity_keys) if db_entity_keys else {}))
                            for layer in layers:
                                # Remove layer_selection classes
                                layer_selection_class = get_or_create_dynamic_layer_selection_class_and_table(layer, False)
                                if layer_selection_class:
                                    layer_selection_class.objects.all().delete()
                            # Delete the layers
                            layers.delete()
                        elif options['relayer_selection']:
                            # Redo just the layer selection tables
                            for config_entity in filter_config_entities(limit_to_classes, [FutureScenario, BaseScenario]):
                                FeatureClassCreator(config_entity).ensure_dynamic_models()
                                layers = Layer.objects.filter(presentation__config_entity=config_entity)
                                for selection_layer in layers:
                                    try:
                                        # Drop the table
                                        layer_selection_class = get_or_create_dynamic_layer_selection_class_and_table(selection_layer, True)

                                        if layer_selection_class:
                                            if hasattr(layer_selection_class.features, 'through'):
                                                layer_selection_features_class = layer_selection_class.features.through
                                                drop_layer_selection_table(layer_selection_features_class)
                                            drop_layer_selection_table(layer_selection_class)

                                    except DatabaseError, e:
                                        logger.warning("Couldn't destroy LayerSelection tables. Maybe the public.layer table no longer exists: %s" % e.message)
                                        # Recreate
                                    get_or_create_dynamic_layer_selection_class_and_table(selection_layer)
                                layer_publishing.update_or_create_layer_selections(config_entity=None)
                        layer_publishing.on_config_entity_post_save_layer(None, instance=config_entity, db_entity_keys=db_entity_keys)

                if options['result']:
                    for config_entity in filter_config_entities(limit_to_classes):
                        result_publishing.on_config_entity_post_save_result(None, instance=config_entity)

                if options['policy']:
                    for config_entity in filter_config_entities(limit_to_classes):
                        policy_publishing.on_config_entity_post_save_policy(None, instance=config_entity)

                if options['tilestache']:
                    for config_entity in filter_config_entities(limit_to_classes):
                        tilestache_publishing.on_config_entity_post_save_tilestache(None,
                                                                                instance=config_entity,
                                                                                db_entity_keys=db_entity_keys)

        if options['recalculate_bounds']:
            recalculate_project_bounds()

        if options['selections']:
            for config_entity in filter_config_entities(limit_to_classes):
                # TODO need to do other selections?
                for db_entity in config_entity.computed_db_entities():
                    config_entity.select_db_entity_of_key(db_entity.key, db_entity)
                config_entity._no_post_save_publishing = True
                config_entity.save()
                config_entity._no_post_save_publishing = False

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


        def test_upload_layer(db_entity_configuration, config_entity):
            # Wipe out the previous import data since we're just testing
            data_import_publishing.on_config_entity_pre_delete_data_import(
                None, instance=config_entity, db_entity_keys=[db_entity_configuration['key']])
            config_entity.db_entities.filter(key=db_entity_configuration['key']).delete()
            # Create the db_entity_interest based on the upload configuration
            config_entity._no_post_save_db_entity_interest_publishing = True
            db_entity_interest = update_or_create_db_entity_and_interest(config_entity, db_entity_configuration)[0]
            config_entity._no_post_save_db_entity_interest_publishing = False
            # Resave to trigger publishers
            # This will cause the data_import publishing to happen and other dependent publishers
            db_entity_interest.save()
            return Layer.objects.get(presentation__config_entity=config_entity, db_entity_key=db_entity_interest.db_entity.key)

        def test_upload_layers(config_entity):
            # Tests layer upload
            from footprint.client.configuration.fixture import ConfigEntityFixture
            client_fixture = ConfigEntityFixture.resolve_config_entity_fixture(config_entity)
            return map(lambda db_entity_configuration: test_upload_layer(db_entity_configuration, config_entity), client_fixture.import_db_entity_configurations())

        if options['test_upload_layers']:
            config_entity = FutureScenario.objects.filter()[0]
            test_upload_layers(config_entity)

        if options['test_layer_from_selection']:
            config_entity = FutureScenario.objects.filter()[0]
            layer = Layer.objects.get(presentation__config_entity=config_entity, db_entity_key=Keys.DB_ABSTRACT_BASE_FEATURE)
            # Create the db_entity_interest based on the upload configuration
            config_entity._no_post_save_db_entity_interest_publishing = True
            db_entity_interest = update_or_create_db_entity_and_interest(config_entity, layer.db_entity)[0]
            config_entity._no_post_save_db_entity_interest_publishing = False
            # Resave to trigger publishers
            # This will cause the data_import publishing to happen and other dependent publishers
            db_entity_interest.save()


        if options['test_clone_scenarios']:
            from footprint.client.configuration.fixture import ConfigEntityFixture
            data_provider = DataProvider()
            scenario = FutureScenario.objects.filter()[0]
            # First do a test layer upload. This way we can ensure that non-default db_entities clone
            # along with the defaults
            cloned_layers = test_upload_layers(scenario)

            import_scenario_configurations = resolve_fixture("config_entity",
                            "config_entities",
                            ConfigEntitiesFixture).import_scenarios(scenario)

            for new_scenario_configuration in import_scenario_configurations:
                # Wipe out data and instance if it already exists
                matches = scenario.__class__.objects.filter(key=new_scenario_configuration['key'])
                if matches:
                    data_import_publishing.on_config_entity_pre_delete_data_import(
                        None, instance=matches[0])
                    matches.delete()

            # Save the scenario to simulate cloning
            # Cloning happens because future_scenario is the clone's origin_config_entity
            cloned_scenarios = data_provider.scenarios_per_project(
                scenario.project,
                import_scenario_configurations)

        if options['inspect']:
            for config_entity in filter_config_entities(limit_to_classes):
                for db_entity_key in db_entity_keys:
                    db_entities = config_entity.computed_db_entities(key=db_entity_key)
                    if db_entities.count() == 1:
                        db_entity = db_entities[0]
                        feature_class_creator = FeatureClassCreator(config_entity, db_entity)
                        feature_class = feature_class_creator.dynamic_feature_class()
                        logger.info("ConfigEntity: %s, DbEntity key: %s, Feature class: %s" % (config_entity.name, db_entity.name, feature_class.__name__))
                        feature_class_configuration = feature_class_creator.feature_class_configuration_from_introspection()
                        logger.info("Feature Class configuration from introspection: %s" % feature_class_configuration)

        call_command('collectstatic', interactive=False)

def all_config_entities():
    config_entities = ConfigEntity.objects.filter(deleted=False).select_subclasses()

    sort_priority = {GlobalConfig: 1, Region: 2, Project: 3, BaseScenario: 4, FutureScenario: 5}
    return sorted(map(
        lambda config_entity: resolve_scenario(config_entity) if isinstance(config_entity, Scenario) else config_entity,
        config_entities
    ), key=lambda config_entity: sort_priority[config_entity.__class__])

def resolve_scenario(scenario):
    for scenario_type in ['basescenario', 'futurescenario']:
        if hasattr(scenario, scenario_type):
            return getattr(scenario, scenario_type)
    return scenario

def config_entity_classes():
    return [BaseScenario, FutureScenario] + Scenario.lineage()

def filter_classes(limit_to_classes):
    classes = [GlobalConfig, Region, Project, BaseScenario, FutureScenario]
    if len(limit_to_classes)==0:
        return classes
    return filter(lambda cls: cls in limit_to_classes, classes)

def filter_config_entities(limit_to_classes, pre_limited_classes=[]):
    config_entities = all_config_entities()
    if len(limit_to_classes + pre_limited_classes)==0:
        return config_entities
    return filter(lambda config_entity: issubclass(config_entity.__class__, tuple(limit_to_classes+pre_limited_classes)), config_entities)

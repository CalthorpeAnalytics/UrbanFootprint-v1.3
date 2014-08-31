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
from django.contrib.auth.models import User

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import DatabaseError
from django.db.models import Count
from footprint import settings
from footprint.celery import app
from footprint.client.configuration.fixture import ConfigEntitiesFixture
from footprint.main.initialization.data_provider import DataProvider
from footprint.main.lib.functions import merge, unfold_until, flat_map, unique
from footprint.main.models import PrimaryComponentPercent, PlacetypeComponentPercent, Result, FeatureBehavior
from footprint.main.models.built_form.built_form_set import BuiltFormSet
from footprint.main.models.presentation.medium import Medium
from footprint.main.models.config.db_entity_interest import DbEntityInterest
from footprint.main.models.built_form.built_form import BuiltForm
from footprint.main.models.built_form.urban.building_attribute_set import BuildingAttributeSet
from footprint.main.models.analysis_module.analysis_module import AnalysisModule
from footprint.main.models.config.config_entity import ConfigEntity
from footprint.main.models.config.global_config import GlobalConfig
from footprint.main.models.config.region import Region
from footprint.main.models.config.project import Project
from footprint.main.models.database.information_schema import InformationSchema, PGNamespace
from footprint.main.models.geospatial.db_entity_keys import DbEntityKey
from footprint.main.models.geospatial.intersection import Intersection
from footprint.main.models.presentation.built_form_example import BuiltFormExample
from footprint.main.models.presentation.layer import Layer
from footprint.main.models.geospatial.db_entity import DbEntity
from footprint.main.models.application_initialization import application_initialization, recalculate_project_bounds, \
    update_or_create_config_entities
from footprint.main.models.config.scenario import BaseScenario, FutureScenario, Scenario
from footprint.main.models.presentation.layer_selection import get_or_create_dynamic_layer_selection_class_and_table, drop_layer_selection_table
from footprint.client.configuration.utils import resolve_fixture
from footprint.main.publishing import data_import_publishing, layer_publishing, result_publishing, analysis_module_publishing, built_form_publishing, tilestache_publishing, db_entity_publishing, policy_publishing, config_entity_publishing
from footprint.main.publishing.analysis_module_publishing import update_or_create_analysis_modules
from footprint.main.publishing.crud_key import CrudKey
from footprint.main.publishing.data_import_publishing import on_config_entity_post_save_data_import
from footprint.main.publishing.db_entity_publishing import update_or_create_db_entity_and_interest
from footprint.main.publishing.layer_publishing import on_config_entity_post_save_layer
from footprint.main.utils.dynamic_subclassing import drop_tables_for_dynamic_classes
from footprint.main.utils.utils import resolve_model, map_property_path, full_module_path, resolve_module_attr, resolvable_module_attr_path
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
        make_option('--noanalysis', action='store_true', help='Skips analysis publisher'),

        # If skip is not specified, the full application initialization will occur
        # Use skip with the options below to limit initialization
        make_option('--skip', action='store_true', default=False,
                    help='Skip initialization and data creation (for just doing resave)'),
        # Use this to skip config_entities and save all db_entity_interests directly
        make_option('--save_db_entity_interests', action='store_true', default=False,
                    help="Saves the db_entity_interests directly to run their publishers, instead of going through the "
                         "config_entities"),

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
        make_option('--reuser', action='store_true', default=False, help='Explicitly delete and recreate users and their assets'),
        make_option('--result', action='store_true', default=False, help='Explicitly run result publisher'),
        make_option('--reresult', action='store_true', default=False, help='Clear results and explicitly run result publisher'),
        make_option('--policy', action='store_true', default=False, help='Explicitly run policy publisher'),
        make_option('--import', action='store_true', default=False, help="Explicitly run data_import publisher"),
        make_option('--db_entity', action='store_true', default=False,
                    help='Rerun through default db_entities to pick up configuration changes'),
        make_option('--built_form', action='store_true', default=False, help='Explicitly run built_form publisher'),
        make_option('--rebuilt_form', action='store_true', default=False, help='Delete all built_form instances and then explicitly run built_form publisher'),
        make_option('--rebuilt_form_relations', action='store_true', default=False, help='Delete all relations between built_forms and then rerun built_form publisher'),
        make_option('--layer', action='store_true', default=False, help='Explicitly run layer publisher'),
        make_option('--analysis', action='store_true', default=False, help='Explicitly run analysis publisher'),
        make_option('--run_analysis', action='store_true', default=False, help='Explicitly run analysis publisher + run the modules too'),

        make_option('--reanalysis', action='store_true', default=False, help='Explicitly run analysis publisher after deleting the analysis module tables'),
        make_option('--recreate_layer', action='store_true', default=False, help='Delete all layers and then explicitly run layer publisher'),
        make_option('--selections', action='store_true', help='Reset config_enitty selections', default=False),

        make_option('--test_clone_scenarios', action='store_true', help='Clone scenarios to simulate a UI clone', default=False),
        make_option('--test_upload_layers', action='store_true', help='Upload layers to simulate a UI upload', default=False),
        make_option('--test_layer_from_selection', action='store_true', help='Tests creating a layer/db_entity from from a selection', default=False),
        make_option('--inspect', action='store_true', help='Specify DbEntity key(s) with db_entity_keys to inspect feature class info about it/them'),
        make_option('--dump_behaviors', action='store_true', help='Dump the Behaviors of each DbEntity of each ConfigEntity'),

        # Limit which projects and scenarios are acted upon
        # TODO not implemented
        make_option('--projects', help='Comma separated project key list to init. The default it all'),
        make_option('--scenarios', help='Comma separated scenario key list to init. The default is all'),

        # Limit which db_entities are acted on, where aplicable
        make_option('--db_entity_keys', help='Comma separated db_entity key list to init to limit data import to given keys'),

        make_option('--recycle', action='store_true', default=False, help='Delete config_entities marked deleted'),
        make_option('--delete_clones', action='store_true', default=False, help='Deletes cloned scenarios, db_entities, and layers'),
        make_option('--delete_scenario_clones', action='store_true', default=False, help='Deletes cloned scenarios'),

        make_option('--delete_layer_clones', action='store_true', default=False, help='Deletes cloned layers'),

        make_option('--relayer_selection', action='store_true', help='Recreates all layer selections'),


        make_option('--class', help='Comma separated classes in the form FutureScenario, Project, etc'),
        make_option('--profile', action='store_true', help='Profile the command', default=False),
        make_option('--memory', action='store_true', help='Profile the command', default=False),

    )

    def handle(self, *args, **options):

        AnalysisModule._no_post_save_task_run_global = True

        if options['profile']:
            profiler = Profile()
            profiler.runcall(self._handle, *args, **options)
            profiler.print_stats()
        else:
            self._handle(*args, **options)

    def delete_layer_selections(self, limit_to_classes):
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
                    logger.warning(
                        "Couldn't destroy LayerSelection tables. Maybe the public.layer table no longer exists: %s" % e.message)

    def create_layer_selections(self, limit_to_classes):
        for config_entity in filter_config_entities(limit_to_classes, [FutureScenario, BaseScenario]):
            FeatureClassCreator(config_entity).ensure_dynamic_models()
            layers = Layer.objects.filter(presentation__config_entity=config_entity)
            for selection_layer in layers:
                # Recreate
                get_or_create_dynamic_layer_selection_class_and_table(selection_layer)
            layer_publishing.update_or_create_layer_selections(config_entity=None)

    def _handle(self, *args, **options):
        project_keys = options.get('projects', []).split(',') if options['projects'] else None
        scenario_keys = options.get('scenarios', []).split(',') if options['scenarios'] else None
        db_entity_keys = options.get('db_entity_keys', []).split(',') if options['db_entity_keys'] else None
        if not options['run_analysis']:
            AnalysisModule._no_post_save_task_run_global = True
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

        if options['delete_layer_clones']:
             for cls in filter_classes(limit_to_classes):
                all_config_entities = cls.objects.all()
                for config_entity in all_config_entities:
                    try:
                        db_entities = map(lambda db_entity_interest: db_entity_interest.db_entity,
                                          DbEntityInterest.objects.filter(config_entity=config_entity, db_entity__origin_instance__isnull=False)) +\
                            list(DbEntity.objects.filter(deleted=True)) + \
                            filter(lambda db_entity: db_entity.feature_class_configuration and (isinstance(db_entity.feature_class_configuration, dict) or db_entity.feature_class_configuration.generated), config_entity.computed_db_entities())
                    except:
                        db_entities = map(lambda db_entity_interest: db_entity_interest.db_entity,
                                          DbEntityInterest.objects.filter(config_entity=config_entity, db_entity__origin_instance__isnull=False)) + \
                                      list(DbEntity.objects.filter(deleted=True))

                    Layer.objects.filter(presentation__config_entity=config_entity, db_entity_key__in=map(lambda db_entity: db_entity.key, db_entities)).delete()
                    for layer in Layer.objects.all():
                        try:
                            layer.db_entity_interest.db_entity
                        except:
                            # orphan
                            try:
                                layer.delete()
                            except:
                                pass

        if options['delete_clones'] or options['delete_scenario_clones']:
            # Delete clones and uploads
            for cls in filter_classes(limit_to_classes):
                all_config_entities = cls.objects.all()
                for config_entity in all_config_entities:
                    if options['delete_clones']:
                        try:
                            db_entities = map(lambda db_entity_interest: db_entity_interest.db_entity,
                                              DbEntityInterest.objects.filter(config_entity=config_entity, db_entity__origin_instance__isnull=False)) +\
                                list(DbEntity.objects.filter(deleted=True)) + \
                                filter(lambda db_entity: db_entity.feature_class_configuration and (isinstance(db_entity.feature_class_configuration, dict) or db_entity.feature_class_configuration.generated), config_entity.computed_db_entities())
                        except:
                            db_entities = map(lambda db_entity_interest: db_entity_interest.db_entity,
                                              DbEntityInterest.objects.filter(config_entity=config_entity, db_entity__origin_instance__isnull=False)) + \
                                          list(DbEntity.objects.filter(deleted=True))

                        Layer.objects.filter(presentation__config_entity=config_entity, db_entity_key__in=map(lambda db_entity: db_entity.key, db_entities)).delete()
                        for layer in Layer.objects.all():
                            try:
                                layer.db_entity_interest.db_entity
                            except:
                                # orphan
                                try:
                                    layer.delete()
                                except:
                                    pass
                        # DbEntities
                        for db_entity in db_entities:
                            feature_class = None
                            try:
                                feature_class = FeatureClassCreator(config_entity, db_entity).dynamic_model_class()
                            except Exception, e:
                                logger.warn("No feature class for db_entity %s could be created. Exception: %s" % (db_entity.name, e.message))
                            if feature_class and InformationSchema.objects.table_exists(db_entity.schema, db_entity.table):
                                drop_tables_for_dynamic_classes(feature_class.__base__, feature_class)
                            db_entity.delete()
                config_entities_fixture = resolve_fixture("config_entity", "config_entities", ConfigEntitiesFixture, settings.CLIENT)
                if issubclass(cls, Scenario):
                    scenario_fixture_keys = unique(flat_map(
                        lambda config_entity: map(lambda fixture: fixture['key'],
                                                  config_entities_fixture.scenarios(config_entity.parent_config_entity)),
                        cls.objects.all()))
                    cloned_config_entities = cls.objects.exclude(key__in=scenario_fixture_keys)

                    # ConfigEntities and their schemas
                    if options['delete_clones'] or options['delete_scenario_clones']:
                        for config_entity in cloned_config_entities:
                            PGNamespace.objects.drop_schema(config_entity.schema())
                        cloned_config_entities.delete()

                if options['delete_clones']:
                    for built_form_set in BuiltFormSet.objects.all():
                        built_form_set.built_forms.remove(*built_form_set.built_forms.filter(origin_instance__isnull=False))
                    # BuiltForms
                    BuiltForm.objects.filter(origin_instance__isnull=False).delete()
                    # Orphaned BuiltForm assets (only an issue when corrupt saves have happened)
                    BuildingAttributeSet.objects.annotate(
                        num_buildings=Count('building'), num_buildingtypes=Count('buildingtype'), num_placetypes=Count('building')).filter(
                        num_buildings=0, num_buildingtypes=0, num_placetypes=0).delete()
                    Medium.objects.annotate(num_built_form_sets=Count('builtform')).filter(num_built_form_sets=0, key__startswith='built_form').delete()
                    BuiltFormExample.objects.annotate(num_built_form_sets=Count('builtform')).filter(num_built_form_sets=0).delete()

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
                    disable_signal_handler(
                        resolvable_module_attr_path(config_entity_publishing.__name__, 'post_save_config_entity_initial'),
                        db_entity_publishing.on_config_entity_post_save_db_entity,
                        "db_entity_on_config_entity_post_save",
                        limit_to_classes)

                if options['noimport']:
                    # Skip data importing
                    disable_signal_handler(
                        resolvable_module_attr_path(config_entity_publishing.__name__, 'post_save_config_entity_db_entities'),
                        data_import_publishing.on_config_entity_post_save_data_import,
                        "data_import_on_config_entity_post_save",
                        limit_to_classes)

                if options['nolayer']:
                    disable_signal_handler(
                        resolvable_module_attr_path(config_entity_publishing.__name__, 'post_save_config_entity_db_entities'),
                        layer_publishing.on_config_entity_post_save_layer,
                        "layer_on_config_entity_post_save",
                        limit_to_classes)

                if options['noresult']:
                    disable_signal_handler(
                        resolvable_module_attr_path(config_entity_publishing.__name__, 'post_save_config_entity_db_entities'),
                        result_publishing.on_config_entity_post_save_result,
                        "result_on_config_entity_post_save",
                        limit_to_classes)

                if options['notilestache']:
                    disable_signal_handler(
                        resolvable_module_attr_path(config_entity_publishing.__name__, 'post_save_config_entity_layers'),
                        tilestache_publishing.on_config_entity_post_save_tilestache,
                        "tilestache_on_config_entity_post_save",
                        limit_to_classes)

                if options['nobuilt_form']:
                    # Skip builtform publishing
                    disable_signal_handler(
                        resolvable_module_attr_path(config_entity_publishing.__name__, 'post_save_config_entity_initial'),
                        built_form_publishing.on_config_entity_post_save_built_form,
                        "built_form_publishing_on_config_entity_post_save",
                        limit_to_classes)

                if options['noanalysis']:
                    disable_signal_handler(
                        resolvable_module_attr_path(config_entity_publishing.__name__, 'post_save_config_entity_imports'),
                        analysis_module_publishing.on_config_entity_post_save_analysis_modules,
                        "analysis_module_on_config_entity_post_save",
                        limit_to_classes)

                # If skip is not specified, the full application initialization will occur
                # Use skip with the options below to limit initialization
                application_initialization(limit_to_classes=limit_to_classes)
                # Update/Create the config_entities
                update_or_create_config_entities(limit_to_classes=limit_to_classes)
            else:
                # If skip is specified, use one or more of the following options
                # to run publishers directly for all or filtered config_entities
                if options['initializer']:
                    # Redo initializers. This is non-config_entity dependent stuff,
                    # like default style templates
                    application_initialization(
                        limit_to_classes=limit_to_classes,
                        no_post_save_publishing=True
                    )

                if options['db_entity']:
                    # Pick up new stuff in the config_entity configurations, namely default db_entities
                    for config_entity in filter_config_entities(limit_to_classes):
                        db_entity_publishing.crud_db_entities(config_entity, CrudKey.SYNC)
                    missing_schemas = filter(lambda x: not x.schema, DbEntity.objects.all())
                    if len(missing_schemas) > 0:
                        logger.error("No schemas for the following db_entities %s" % map_property_path(missing_schemas, 'key'))

                if options['built_form']:
                    for config_entity in filter_config_entities(limit_to_classes):
                        built_form_publishing.on_config_entity_post_save_built_form(None, instance=config_entity)
                if options['rebuilt_form']:
                    # This only works if their are no feature tables that reference the built forms
                    BuiltFormSet.objects.all().delete()
                    BuiltForm.objects.all().delete()
                    for config_entity in filter_config_entities(limit_to_classes):
                        built_form_publishing.on_config_entity_post_save_built_form(None, instance=config_entity)
                if options['rebuilt_form_relations']:
                    # Redo the relationships between the built forms.
                    PrimaryComponentPercent.objects.all().delete()
                    PlacetypeComponentPercent.objects.all().delete()
                    for config_entity in filter_config_entities(limit_to_classes):
                        built_form_publishing.on_config_entity_post_save_built_form(None, instance=config_entity)

                if options['import']:
                    for config_entity in filter_config_entities(limit_to_classes):
                        on_config_entity_post_save_data_import(None, instance=config_entity, db_entity_keys=db_entity_keys)
                elif options['reimport']:
                    for config_entity in filter_config_entities(limit_to_classes):
                        # Use the predelete to drop the tables
                        data_import_publishing.on_config_entity_pre_delete_data_import(None, instance=config_entity, db_entity_keys=db_entity_keys)
                        # Reimport the db_entity tables for the specified config_entities/db_entity_keys
                        data_import_publishing.on_config_entity_post_save_data_import(None, instance=config_entity, db_entity_keys=db_entity_keys)

                if options['analysis']:
                    for config_entity in filter_config_entities(limit_to_classes):
                        update_or_create_analysis_modules(config_entity)

                if options['reanalysis']:
                    for config_entity in filter_config_entities(limit_to_classes):
                        analysis_module_publishing.on_config_entity_pre_delete_analysis_modules(None, instance=config_entity)
                        analysis_module_publishing.on_config_entity_post_save_analysis_modules(None, instance=config_entity)

                if options['layer'] or options['recreate_layer'] or options['relayer_selection']:
                    for config_entity in filter_config_entities(limit_to_classes):
                        if options['recreate_layer']:
                            layers = Layer.objects.filter(**merge(dict(presentation__config_entity=config_entity),
                                                                  Intersection(db_entity_key__in=db_entity_keys) if db_entity_keys else {}))
                            for layer in layers:
                                # Remove layer_selection classes
                                layer_selection_class = get_or_create_dynamic_layer_selection_class_and_table(layer, False)
                                if layer_selection_class:
                                    layer_selection_class.objects.all().delete()
                            # Delete the layers
                            layers.delete()
                        elif options['relayer_selection']:
                            # Redo just the layer selection tables
                            self.delete_layer_selections(limit_to_classes)
                            self.create_layer_selections(limit_to_classes)
                        layer_publishing.on_config_entity_post_save_layer(None, instance=config_entity, db_entity_keys=db_entity_keys)

                if options['reuser']:
                    # We don't actually recreate users since they are referenced by too many models
                    self.delete_layer_selections(limit_to_classes)
                    DataProvider().users()
                    self.create_layer_selections(limit_to_classes)

                if options['result'] or options['reresult']:
                    if options['reresult']:
                        for result in Result.objects.all():
                            try:
                                result.db_entity_interest.db_entity.delete()
                            except:
                                pass
                        Result.objects.all().delete()
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
                previous = config_entity._no_post_save_publishing
                config_entity._no_post_save_publishing = True
                config_entity.save()
                config_entity._no_post_save_publishing = previous

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


        def test_upload_layer(config_db_entity, config_entity):
            # Wipe out the previous import data since we're just testing
            data_import_publishing.on_config_entity_pre_delete_data_import(
                None, instance=config_entity, db_entity_keys=[config_db_entity.key])
            config_entity.db_entities.filter(key=config_db_entity.key).delete()
            # Create the db_entity_interest based on the upload configuration
            previous = DbEntityInterest._no_post_save_publishing
            DbEntityInterest._no_post_save_publishing = True
            db_entity_interest = update_or_create_db_entity_and_interest(config_entity, config_db_entity)[0]
            # Indicates the from
            db_entity_interest.db_entity.feature_class_configuration.primary_key = 'gid' # primary_key should be 'from_column'
            db_entity_interest.db_entity.save()
            DbEntityInterest._no_post_save_publishing = previous
            # Resave to trigger publishers
            # This will cause the data_import publishing to happen and other dependent publishers
            db_entity_interest.save()
            on_config_entity_post_save_layer(config_entity, instance=config_entity, db_entity_keys=[db_entity_interest.db_entity.key])
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
            layer = Layer.objects.get(presentation__config_entity=config_entity, db_entity_key=DbEntityKey.BASE)
            # Create the db_entity_interest based on the upload configuration
            previous = DbEntityInterest._no_post_save_publishing
            DbEntityInterest._no_post_save_publishing = True
            db_entity_interest = update_or_create_db_entity_and_interest(config_entity, layer.db_entity)[0]
            DbEntityInterest._no_post_save_publishing = previous
            # Resave to trigger publishers
            # This will cause the data_import publishing to happen and other dependent publishers
            db_entity_interest.save()


        if options['test_clone_scenarios']:
            from footprint.client.configuration.fixture import ConfigEntityFixture
            data_provider = DataProvider()
            scenario = FutureScenario.objects.filter()[0]
            # First do a test layer upload. This way we can ensure that non-default db_entities clone
            # along with the defaults
            #cloned_layers = test_upload_layers(scenario)

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
            # Cloning happens because future_scenario is the clone's origin_instance
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
                        feature_class = feature_class_creator.dynamic_model_class()
                        logger.info("ConfigEntity: %s, DbEntity key: %s, Feature class: %s" % (config_entity.name, db_entity.name, feature_class.__name__))
                        feature_class_configuration = feature_class_creator.feature_class_configuration_from_introspection()
                        logger.info("Feature Class configuration from introspection: %s" % feature_class_configuration)

        if options['dump_behaviors']:
            for config_entity in filter_config_entities(limit_to_classes):
                for db_entity in config_entity.computed_db_entities(**dict(key__in=db_entity_keys) if db_entity_keys else dict()):
                    logger.info("ConfigEntity: %s, DbEntity key: %s, Behaviors:\n%s" % (config_entity.name, db_entity.name, db_entity.feature_behavior.behavior.dump_behaviors()))
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

def disable_signal_handler(signal_ref_path, handler, uid, limit_to_classes):
    for cls in filter_classes(limit_to_classes):
        resolve_module_attr(signal_ref_path).disconnect(handler, cls, True, uid)

    disable_signal_handler_for_celery.apply_async(
        args=(signal_ref_path, full_module_path(handler), uid, map(lambda cls: full_module_path(cls), limit_to_classes)),
        soft_time_limit=3600,
        time_limit=3600,
        countdown=1
    )

@app.task
def disable_signal_handler_for_celery(signal_ref_path, handler_path, uid, limit_to_classes_paths):
    for cls in filter_classes(limit_to_classes_paths):
        resolve_module_attr(signal_ref_path).disconnect(resolve_module_attr(handler_path), resolve_module_attr(cls), True, uid)

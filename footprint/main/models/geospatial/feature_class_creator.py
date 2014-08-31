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
from __builtin__ import staticmethod
import logging
from django.contrib.gis.db import models
from django.contrib.gis.db.models import GeometryField
from django.db.models import ForeignKey
from django.db.models.fields import Field, AutoField
from tastypie.fields import ToManyField, OneToOneField
from footprint.main.lib.functions import map_to_dict, merge, unique, flat_map, filter_dict, map_dict_to_dict, dual_map_to_dict, my_deep_copy
from footprint.main.models.dynamic_model_class_creator import DynamicModelClassCreator
from footprint.main.models.geospatial.feature import Feature
from footprint.main.models.geospatial.feature_class_configuration import FeatureClassConfiguration
from footprint.main.utils.dynamic_subclassing import get_dynamic_model_class_name, dynamic_model_class
from footprint.main.utils.inline_inspectdb import InlineInspectDb
from footprint.main.utils.utils import resolve_module_attr, full_module_path, resolve_model, split_filter
from footprint.main.models.config.config_entity import ConfigEntity

logger = logging.getLogger(__name__)

class FeatureClassCreator(DynamicModelClassCreator):

    def __init__(self, config_entity=None, db_entity=None, no_ensure=False):
        """
            Creates a FeatureClassCreator for the given ConfigEntity, and optionally specific to a DbEntity of the ConfigEntity.
            The DbEntity must have a feature_class_configuration in order to create a Feature class
        """
        if isinstance(db_entity, FeatureClassConfiguration):
            # Some base class methods pass in the configuration to the constructor--resolve the DbEntity
            self.db_entity = config_entity.computed_db_entities(key=db_entity.key)[0]
        else:
            self.db_entity = db_entity
        super(FeatureClassCreator, self).__init__(config_entity, self.db_entity and self.resolve_configuration(self.db_entity), no_ensure)

    @classmethod
    def resolve_configuration(cls, db_entity):
        return db_entity.feature_class_configuration

    def db_entity_to_feature_class_lookup(self):
        """
            Returns the db_entity to feature_classes of the config_entity.computed_db_entities()
        :return:
        """
        return map_to_dict(lambda db_entity: [db_entity, FeatureClassCreator(self.config_entity, db_entity).dynamic_model_class()],
                           filter(lambda db_entity: db_entity.feature_class_configuration, self.config_entity.computed_db_entities()))

    def dynamic_model_configurations(self):
        """
            Returns all of the DbEntities of the config_entity that have a feature_class_configuration
        """
        db_entities = self.config_entity.computed_db_entities(no_feature_class_configuration=False, feature_class_configuration__isnull=False)
        valid_db_entities, invalid_db_entities = split_filter(lambda db_entity: not db_entity.feature_class_configuration or db_entity.is_valid, db_entities)
        if len(invalid_db_entities) > 0:
            logger.warn("The following db_entities have invalid feature_class_configurations: %s" % map(lambda db_entity: db_entity.key, invalid_db_entities))
        return valid_db_entities

    def dynamic_model_configuration(self, key):
        """
            Find the DbEntity matching the key. Then get its FeatureClassConfiguration version
        """
        try:
            return filter(
                lambda feature_class_configuration: feature_class_configuration.key==key,
                self.dynamic_model_configurations())[0]
        except:
            raise Exception("No FeatureClassConfiguration exists with key %s" % key)

    def ensure_dynamic_models(self):
        """
            For a given run of the application, make sure that all the dynamic model classes of the config_entity have been created.
            We only want to create model classes once per application run, and once they are created below we shouldn't have to check
            to see if they exist. If need models are created by layer import, etc, that process is responsible for creating the classes,
            and then they will be created here on the subsequent application runs
        """

        if self.no_ensure or self.config_entity._feature_classes_created:
            return False

        # Create all feature classes, both the base version and the rel version
        # TODO the filter_dict is here to filter out null values due to DbEntity corruption. This should go away as things stablize
        def get_db_entity(key):
            try:
                return self.config_entity.computed_db_entities(key=key).get()
            except Exception, e:
                logger.error("Error fetching DbEntity key %s" % key)
                raise e

        db_entity_to_feature_class = filter_dict(lambda key, value: value,
                                                 map_dict_to_dict(
                                                    lambda key, feature_class: [get_db_entity(key), feature_class],
                                                    self.__class__(self.config_entity, no_ensure=True).key_to_dynamic_model_class_lookup()))

        # Ensure that the dynamic geography class of each uniquely represented self.db_entity-owning config_entity
        for db_entity in unique(db_entity_to_feature_class.keys(),
                                lambda db_entity: db_entity.feature_class_configuration.geography_scope):
            FeatureClassCreator(self.config_entity, db_entity, no_ensure=True).dynamic_geography_class()

        # Prevent a rerun by setting this flag to True now that we're done
        self.config_entity._feature_classes_created = True

    def dynamic_geography_class_name(self):
        return get_dynamic_model_class_name(resolve_module_attr('footprint.main.models.geographies.geography.Geography'),
                                            self.configuration.geography_scope)

    def dynamic_geography_class(self):
        """
            Return the geography class based on the db_entity or config_entity
        """
        scope = ConfigEntity._subclassed_config_entity_by_id(self.configuration.geography_scope if self.configuration.key else self.config_entity)
        return dynamic_model_class(
            resolve_module_attr('footprint.main.models.geographies.geography.Geography'),
            scope.schema(),
            'geography',
            self.dynamic_geography_class_name(),
            scope=scope
        )

    def has_dynamic_model_class(self):
        """
            Returns true if the instance has an abstract_class configured
        """
        feature_class_configuration = self.configuration
        if not feature_class_configuration:
            return None
        return feature_class_configuration.abstract_class_name

    def dynamic_model_class(self, base_only=False, schema=None, table=None):
        """
            Gets or creates a DbEntity Feature subclass based on the given configuration.
            There are two classes get or created. The base models the imported table.
            The child subclasses the base and adds relations. This way the imported table is not manipulated.
            The child class is returned unless base_only=True is specified
        :params base_only: Default False, indicates that only the base feature class is desired, not the subclass
            that contains the relationships
        :return: The dynamic subclass of the subclass given in feature_class_configuration or None
        """
        if not self.configuration:
            # Return none if no self.configuration exists
            return None

        if not self.configuration.class_attrs or len(self.configuration.class_attrs) == 0:
            raise Exception("Class attributes missing from configuration for db_entity %s" % self.db_entity.full_name)

        if self.configuration.feature_class_owner:
            # If a different DbEntity owners owns the feature_class (e.g. for Result DbEntities), delegate
            self.__class__(
                self.config_entity,
                self.config_entity.computed_db_entities().get(key=self.configuration.feature_class_owner),
                # Same config_entity, ensuring would cause infinite recursion
                no_ensure=True
            ).dynamic_model_class(base_only)

        # Create the base class to represent the "raw" table
        try:
            abstract_feature_class = resolve_module_attr(self.configuration.abstract_class_name)
        except Exception, e:
            # TODO. This shouldn't ever happen once DbEntity/Layer saving is stable
            logger.error("Corrupt DbEntity %s. Have you configured the imports properly so that Django can find the class?" % self.db_entity.name)
            return

        existing_field_names = map(lambda field: field.name,
                                   filter(lambda field: isinstance(field, Field), abstract_feature_class._meta.fields))
        fields = filter(lambda field: isinstance(field, Field) and field.name not in existing_field_names+['id'], self.configuration.fields or [])

        base_feature_class = dynamic_model_class(
            abstract_feature_class,
            self.db_entity.schema,
            self.db_entity.table,
            class_name="{0}{1}".format(abstract_feature_class.__name__, self.db_entity.id),
            fields=map_to_dict(lambda field: [field.name, field], fields),
            # (no extra fields defined here in the parent)
            class_attrs=self.configuration.class_attrs or {},
            related_class_lookup=self.configuration.related_class_lookup or {}
        )

        if base_only:
            # If the child class isn't needed, return the base
            return base_feature_class

        # Create the child class that subclasses the base and has the related fields
        return dynamic_model_class(
            base_feature_class,
            self.db_entity.schema,
            '{0}rel'.format(self.db_entity.table),
            class_name="{0}{1}Rel".format(abstract_feature_class.__name__, self.db_entity.id),
            fields=merge(
                # Create all related fields. These are ForeignKey fields for single values and ManyToMany for many values
                self.create_related_fields(),
                # Create the ManyToMany geographies association that associates the feature to the primary geographies that it intersects.
                # Even if this feature contains primary geographies remains a many property in case there are multiple primary geography tables
                dict(geographies=models.ManyToManyField(self.dynamic_geography_class_name(),
                                                        db_table='"{schema}"."{table}_geography"'.format(
                                                            schema=self.db_entity.schema,
                                                            table=self.db_entity.table)))
            ),
            class_attrs=self.configuration.class_attrs or {},
            related_class_lookup=self.configuration.related_class_lookup or {}
        )

    def dynamic_join_model_class(self, related_models):
        """
            Creates an unmanaged version of the feature class with extra fields to represent the dicts of a joined
            ValuesQuerySet
        """
        from footprint.main.utils.query_parsing import main_field_paths_to_fields, related_field_paths_to_fields
        manager = self.dynamic_model_class().objects
        # Exclude the following field types Since the base Feature defines an id we'll still get that, which we want
        exclude_field_types = (AutoField, ForeignKey, ToManyField, OneToOneField, GeometryField)
        all_field_paths_to_fields = merge(
            main_field_paths_to_fields(manager, exclude_field_types=exclude_field_types, fields=manager.model.limited_api_fields()),
            *map(lambda related_model: related_field_paths_to_fields(manager, related_model, exclude_field_types=exclude_field_types, fields=related_model.limited_api_fields(), separator='_x_'), related_models))

        abstract_feature_class = resolve_module_attr(self.configuration.abstract_class_name)
        return dynamic_model_class(
            Feature,
            self.db_entity.schema,
            self.db_entity.table,
            class_name="{0}{1}Join".format(abstract_feature_class.__name__, self.db_entity.id),
            fields=all_field_paths_to_fields,
            class_attrs=self.configuration.class_attrs or {},
            related_class_lookup=self.configuration.related_class_lookup or {},
            is_managed=False,
            cacheable=False)

    @staticmethod
    def remove_auto(field):
        modified_field = my_deep_copy(field)
        modified_field.auto_created = False
        modified_field.primary_key = False
        return modified_field


    def feature_class_configuration_from_introspection(self):
        """
            Creates a dynamic Feature class configuration by introspecting the db_entity's Feature table.
        :return: The Feature class configuration
        """
        fields = InlineInspectDb.get_fields(self.db_entity.full_table_name)
        return self.generate_configuration(fields.values())

    def feature_class_configuration_from_geojson_introspection(self, data):
        """
            Creates a dynamic Feature class configuration by introspecting the db_entity's Feature table.
        :return: The Feature class configuration
        """
        properties = unique(flat_map(lambda feature: feature.properties.keys(), data.features))
        fields = map(lambda property: models.CharField(property), properties)
        return self.generate_configuration(fields)

    def resolve_geography_scope(self):
        """
            The config_entity id ancestor whose geography table is used by this ConfigEntity depends on its class.
            If it is a Scenario it uses that of the Project, otherwise it uses the one in its own schema.
            The reason for this is that Scenario feature tables needed to be joined
            to Project primary geographies for querying. Really the way this is should work is that geography association tables
            are created at the Project and Region scopes, but for now we just do one.
        """
        return self.config_entity.project.id if isinstance(self.config_entity, resolve_model('main.Scenario')) else self.config_entity.id

    def generate_configuration(self, fields=[]):
        """
            Creates a feature_class_configuration for db_entities not pre-configured, in other words, those that
            were uploaded.
        """

        # Use the pk for the source_id_column
        primary_key_fields = filter(lambda field: field.primary_key, fields)
        # Use the existing primary key or default to the default Django one
        # The former case applies to imported tables that have primary keys, the latter to tables that are
        # created by Django
        source_id_column = primary_key_fields[0].name if primary_key_fields else 'id'

        return self.complete_or_create_feature_class_configuration(
            FeatureClassConfiguration(
                fields=fields,
                source_id_column=source_id_column,
                # Generated tells us that the feature_class_configuration wasn't pre-configured in code
                generated=True
            )
        )

    def complete_or_create_feature_class_configuration(self, feature_class_configuration, **overrides):
        """
            Clones the given feature_class_configuration to make it specific to the ConfigEntity
            If the feature_class_configuration is null a simple one is created
            :param feature_class_configuration: Used for the basis of cloning from another DbEntity, or
            as the preconfigured instance that was defined in an initializer, such as default_project.py
            :param overrides: Override anything in the feature_class_configuration. This is used for cloning
            when we need to specify generated=YES, source_from_origin_layer_selection=True, etc
        """
        if not feature_class_configuration:
            # If nothing is passed it means that the DbEntity doesn't represent a feature table, e.g. background imagery
            return None
        from footprint.main.publishing import data_import_publishing
        return FeatureClassConfiguration(**merge(
            dict(
                related_class_lookup=dict(config_entity='footprint.main.models.config.config_entity.ConfigEntity'),
                # Indicates that the configuration was generated by introspecting a table, rather than by deliberate configuration
                generated=False,
                # Indicates that the features should be created from an origin LayerSelection features.
                source_from_origin_layer_selection=False,
                # The origin Layer id
                origin_layer_id=None,
                # The user of the origin layer
                origin_user=None,
                # The default data_importer for features
                # The default imports based on the url of the db_entity--usually a special database url
                data_importer=full_module_path(data_import_publishing.DefaultImportProcessor),
            ),
            # Override the above with any configured attributes
            merge(feature_class_configuration.__dict__, overrides) if feature_class_configuration else {},
            # Override or define ConfigEntity specific attributes
            dict(
                key=self.db_entity.key,
                # The scope is the id of the config_entity
                scope=self.config_entity and self.config_entity.id,
                # The scope of the Geography table. Scenarios always scope to the Project geography table, for now
                geography_scope=self.resolve_geography_scope(),
                schema=self.config_entity.schema(),
                class_attrs=merge(
                    feature_class_configuration.class_attrs if feature_class_configuration else {},
                    {'config_entity__id': self.config_entity.id, 'override_db': self.config_entity.db, 'db_entity_key': self.db_entity.key}),
            ) if self.config_entity else dict(
                # Abstract case
                key=self.db_entity.key,
                class_attrs=merge(
                    feature_class_configuration.class_attrs if feature_class_configuration else {},
                    {'db_entity_key': self.db_entity.key})
            )
        ))


    def update_db_entity(self, feature_class_configuration):
        # Update our DbEntity so we have the configuration available for future operations
        # Note that we always want to generate the feature_class_configuration here if its generated in case
        # the table schema is updated and we need to modify the configuration
        self.db_entity.feature_class_configuration.__dict__.update(feature_class_configuration.__dict__)
        # Disable signals and update the DbEntity
        self.db_entity._no_post_post_save = True
        self.db_entity.save()
        self.db_entity._no_post_post_save = False
        # Update our reference
        self.configuration = self.db_entity.feature_class_configuration

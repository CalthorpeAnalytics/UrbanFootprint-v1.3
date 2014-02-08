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
from django.contrib.gis.db import models
from django.db.models.fields import Field
from footprint.main.lib.functions import map_dict_to_dict, map_to_dict, merge, remove_keys, unique, get_single_value_or_none, flat_map, filter_keys, filter_dict
from footprint.main.models.geospatial.feature import Feature
from footprint.main.utils.dynamic_subclassing import get_dynamic_model_class_name, dynamic_model_class
from footprint.main.utils.inline_inspectdb import InlineInspectDb
from footprint.main.utils.utils import resolve_module_attr, get_property_path, full_module_path, resolve_model
from footprint.main.models.config.config_entity import ConfigEntity

logger = logging.getLogger(__name__)

class FeatureClassCreator(object):
    def __init__(self, config_entity, db_entity=None):
        """
            Creates a FeatureClassCreator for the given ConfigEntity, and optionally specific to a DbEntity of the ConfigEntity
        """

        self.config_entity = config_entity.subclassed_config_entity
        self.db_entity = db_entity

    def db_entity_to_feature_class_lookup(self):
        """
            Returns the db_entity to feature_classes of the config_entity.computed_db_entities()
        :return:
        """
        return map_to_dict(lambda db_entity: [db_entity, FeatureClassCreator(self.config_entity, db_entity).dynamic_feature_class()],
                           filter(lambda db_entity: db_entity.feature_class_configuration, self.config_entity.computed_db_entities()))

    @staticmethod
    def db_entity_key_to_feature_class_lookup(config_entity, db_entity_configurations=None):
        """
            Returns all db_entity_configuration keys mapped to a dynamic Feature subclass or None if no Feature
            class is configured for the db_entity_configuration
        :param config_entity: Used to scope the Feature classes. If no then abstract classes are returned
        :param db_entity_configurations: Optional specific set of configurations. If omitted, the db_entity.computed_db_enties()
        will be used. You must specify this before the db_entities have been created on the config_entity, for the case
        where the config_entity is null.
        :return: A dict keyed by db_entity key and valued by a dynamic Feature subclass or None
        """
        if not config_entity:
            return FeatureClassCreator.db_entity_key_to_abstract_feature_class_lookup(db_entity_configurations)

        # Get the config_entity from the first self.db_entity_configuration with a feature_class_configuration
        # Get the corresponding db_entities from the config_entity
        db_entities = map(
            lambda db_entity_configuration: config_entity.computed_db_entities(key=db_entity_configuration['key'])[0],
            db_entity_configurations)
        return map_to_dict(lambda db_entity: [db_entity.key, FeatureClassCreator(config_entity, db_entity).dynamic_feature_class()],
                           db_entities)

    @staticmethod
    def db_entity_key_to_abstract_feature_class_lookup(db_entity_configurations):
        """
            Like self.db_entity_key_to_feature_class_lookup, but used when no ConfigEntity is in scope.
            This returns the abstract version of the Feature subclasses by self.db_entity_key
        :param db_entity_configurations:
        :return:
        """
        return map_to_dict(lambda db_entity_configuration: [db_entity_configuration['key'],
                                                            resolve_module_attr(get_property_path(db_entity_configuration, 'feature_class_configuration.abstract_class'))],
                           db_entity_configurations)

    def ensure_dynamic_models(self):
        """
            For a given run of the application, make sure that all the dynamic model classes of the config_entity have been created.
            We only want to create model classes once per application run, and once they are created below we shouldn't have to check
            to see if they exist. If need models are created by layer import, etc, that process is responsible for creating the classes,
            and then they will be created here on the subsequent application runs
        """
        if self.config_entity._dynamic_models_created:
            return

        # Create all feature classes, both the base version and the rel version
        # TODO the filter_dict is here to filter out null values due to DbEntity corruption. This should go away as things stablize
        db_entity_to_feature_class = filter_dict(lambda key, value: value, self.db_entity_to_feature_class_lookup())
        # Ensure that the dynamic geography class of each uniquely represented self.db_entity-owning config_entity
        for db_entity in unique(db_entity_to_feature_class.keys(), lambda db_entity: db_entity.feature_class_configuration['geography_scope']):
            FeatureClassCreator(self.config_entity, db_entity).dynamic_geography_class()

    def dynamic_geography_class_name(self):
        return get_dynamic_model_class_name(resolve_module_attr('footprint.main.models.geographies.geography.Geography'),
                                            self.db_entity.feature_class_configuration['geography_scope'])

    def dynamic_geography_class(self):
        """
            Return the geography class based on the db_entity or config_entity
        """
        scope = ConfigEntity._subclassed_config_entity_by_id(self.db_entity.feature_class_configuration['geography_scope'] if self.db_entity else self.config_entity)
        return dynamic_model_class(
            resolve_module_attr('footprint.main.models.geographies.geography.Geography'),
            scope.schema(),
            'geography',
            self.dynamic_geography_class_name(),
            scope=scope
        )

    @property
    def feature_class_is_ready(self):
        """
            Returns True is enough configuration exists to create the dynamic feature class.
        """
        feature_class_configuration = self.db_entity.feature_class_configuration
        # This is a bit of a hack, but it's assumed the feature_class_configuration is ready when it has
        # an abstract_class, since this is the way that imported feature classes work.
        return feature_class_configuration and feature_class_configuration.get('abstract_class', False)

    def dynamic_feature_class(self, base_only=False):
        """
            Gets or creates a DbEntity Feature subclass based on the given configuration.
            There are two classes get or created. The base models the imported table.
            The child subclasses the base and adds relations. This way the imported table is not manipulated.
            The child class is returned unless base_only=True is specified
        :params base_only: Default False, indicates that only the base feature class is desired, not the subclass
            that contains the relationships
        :return: The dynamic subclass of the subclass given in feature_class_configuration or None
        """
        feature_class_configuration = self.db_entity.feature_class_configuration
        if not feature_class_configuration:
            return None

        # Create the base class to represent the "raw" table
        try:
            abstract_feature_class = resolve_module_attr(feature_class_configuration['abstract_class'])
        except Exception, e:
            # TODO. This shouldn't ever happen once DbEntity/Layer saving is stable
            logger.error("Corrupt DbEntity %s." % self.db_entity.name)
            return

        existing_field_names = map(lambda field: field.name,
                                   filter(lambda field: isinstance(field, Field), abstract_feature_class._meta.fields))
        fields = filter(lambda field: isinstance(field, Field) and field.name not in existing_field_names+['id'], feature_class_configuration.get('fields', []))

        base_feature_class = dynamic_model_class(
            abstract_feature_class,
            feature_class_configuration['schema'],
            feature_class_configuration['table'],
            class_name="{0}{1}".format(abstract_feature_class.__name__, self.db_entity.id),
            fields=map_to_dict(lambda field: [field.name, field], fields),
            # (no extra fields defined here in the parent)
            class_attrs=feature_class_configuration.get('class_attrs', {}),
            related_class_lookup=feature_class_configuration.get('related_class_lookup', {})
        )

        if base_only:
            # If the child class isn't needed, return the base
            return base_feature_class

        # Create the child class that subclasses the base and has the related fields
        return dynamic_model_class(
            base_feature_class,
            feature_class_configuration['schema'],
            '{0}rel'.format(feature_class_configuration['table']),
            class_name="{0}{1}Rel".format(abstract_feature_class.__name__, self.db_entity.id),
            fields=merge(
                # Create all related fields. These are ForeignKey fields for single values and ManyToMany for many values
                self.create_related_fields(),
                # Create the ManyToMany geographies association that associates the feature to the primary geographies that it intersects.
                # Even if this feature contains primary geographies remains a many property in case there are multiple primary geography tables
                dict(geographies=models.ManyToManyField(self.dynamic_geography_class_name(),
                                                        db_table='"{schema}"."{table}_geography"'.format(
                                                            schema=feature_class_configuration['schema'],
                                                            table=feature_class_configuration['table'])))
            ),
            class_attrs=feature_class_configuration.get('class_attrs', {}),
            related_class_lookup=feature_class_configuration.get('related_class_lookup', {})
        )

    def create_related_fields(self):
        """
            Create ForeignKey and ManyFields for each db_entity.feature_class_configuration.related_fields
        :return:
        """
        return map_dict_to_dict(
            lambda field_name, related_field_configuration: self.create_related_field(
                field_name,
                related_field_configuration),
            self.db_entity.feature_class_configuration.get('related_fields', {}))

    def related_descriptors(self):
        """
            Returns the existing related field descriptors that were created by create_related_fields and assigned
            to the dynamic feature class
        :return: A dict keyed by field name, valued by the ManyToMany field or equivalent
        """

        feature_class = self.config_entity.feature_class_of_db_entity_key(self.db_entity.key)
        return map_dict_to_dict(
            lambda field_name, related_field_configuration: [field_name, getattr(feature_class, field_name)],
            self.db_entity.feature_class_configuration.get('related_fields', {}))


    def feature_class_configuration_from_introspection(self):
        """
            Creates a dynamic Feature class configuration by introspecting the db_entity's Feature table.
        :return: The Feature class configuration
        """
        fields = InlineInspectDb.get_fields(self.db_entity.full_table_name)
        return self.create_feature_class_configuration(fields.values())

    def feature_class_configuration_from_geojson_introspection(self, data):
        """
            Creates a dynamic Feature class configuration by introspecting the db_entity's Feature table.
        :return: The Feature class configuration
        """
        properties = unique(flat_map(lambda feature: feature.properties.keys(), data.features))
        fields = map(lambda property: models.CharField(property), properties)
        return self.create_feature_class_configuration(fields)

    FEATURE_CLASS_CONFIGURATION_KEYS = [
            'abstract_class',
            'schema',
            'table',
            'class_name',
            'class_attrs',
            'related_class_lookup',
            'scope',
            'geography_scope',
            'db_entity_key',
            'fields',
            'source_id_column',
            'source_from_origin_layer_selection',
            'intersection',
            'generated',
            'data_importer'
    ]
    @classmethod
    def feature_class_configuration_keys(cls):
        """
            These are all the possible keys in the feature_class_configuration.
            This is used for cloning
        """
        return cls.FEATURE_CLASS_CONFIGURATION_KEYS

    def resolve_geography_scope(self):
        """
            The config_entity id ancestor whose geography table is used by this ConfigEntity depends on its class.
            If it is a Scenario it uses that of the Project, otherwise it uses the one in its own schema.
            The reason for this is that Scenario feature tables needed to be joined
            to Project primary geographies for querying. Really the way this is should work is that geography association tables
            are created at the Project and Region scopes, but for now we just do one.
        """
        return self.config_entity.project.id if isinstance(self.config_entity, resolve_model('main.Scenario')) else self.config_entity.id

    def create_feature_class_configuration(self, fields=[]):
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

        return dict(
            abstract_class=full_module_path(Feature),
            schema=self.config_entity.schema(),
            table=self.db_entity.key,
            class_name=None,
            class_attrs={'config_entity__id': self.config_entity.id, 'override_db': self.config_entity.db, 'db_entity_key': self.db_entity.key},
            related_class_lookup=dict(config_entity='footprint.main.models.config.config_entity.ConfigEntity'),
            scope=self.config_entity.id,
            # The scope of the Geography table. Scenarios always scope to the Project geography table, for now
            geography_scope=self.resolve_geography_scope(),
            db_entity_key=self.db_entity.key,
            fields=fields,
            source_id_column=source_id_column,
            # Indicates that the features should be created from the db_entity's LayerSelection features.
            # The LayerSelection is based on the user who last updated the db_entity (db_entity.updater)
            source_from_origin_layer_selection=False,
            # Default to centroid-centroid intersection.
            # TODO this should be specified during the import process
            intersection=dict(type='polygon'),
            # Generated tells us that the feature_class_configuration wasn't pre-configured in code
            generated=True,
            # This will be set to a custom importer class path, such as the ShapeFileProcessor,
            # depending on how the feature data is imported.
            data_importer=None
        )

    def get_feature_class_configuration(self, **kwargs):
        """
            Creates a full Feature_class_configuration based on the kwargs
        """

        from footprint.main.publishing import data_import_publishing
        return dict(
            abstract_class=full_module_path(kwargs.get('base_class', Feature)),
            schema=self.config_entity.schema(),
            table=kwargs['key'],
            class_name=None,
            class_attrs={'config_entity__id': self.config_entity.id, 'override_db': self.config_entity.db, 'db_entity_key': kwargs['key']},
            related_class_lookup=dict(config_entity='footprint.main.models.config.config_entity.ConfigEntity'),
            scope=self.config_entity.id,
            # The scope of the Geography table. Scenarios always scope to the Project geography table, for now
            geography_scope=self.resolve_geography_scope(),
            db_entity_key=kwargs['key'],
            # Indicates that the configuration was generated by introspecting a table, rather than by deliberate configuration
            generated=False,
            # Indicates that the features should be created from the db_entity's LayerSelection features.
            # The LayerSelection is based on the user who last updated the db_entity (db_entity.updater)
            source_from_origin_layer_selection=False,
            # The default data_importer for features
            # The default imports based on the url of the db_entity--usually a special database url
            data_importer=full_module_path(data_import_publishing.DefaultImportProcessor),
            # Pass the remaining keys straight through from the db_entity configuration
            **remove_keys(kwargs, ['key', 'base_class'])
        )

    def feature_class_configuration_for_config_entity(self, feature_class_configuration):
        """
            Used when cloning the db_entity of a config_entity. This takes the feature_class_configuration
            of the source config_entity and updates it scope to that of this config_entity
        """
        return merge(feature_class_configuration, dict(
            scope=self.config_entity.id,
            # The scope of the Geography table. Scenarios always scope to the Project geography table, for now
            geography_scope=self.resolve_geography_scope(),
            schema=self.config_entity.schema()
        ))

    def create_related_field(self, field_name, related_field_configuration):
        """
            Creates a ForeignKey or ManyToMany field based on related_field_configuration
        :param field_name:
        :param related_field_configuration: A dict containing related_db_entity_key or related_class_name
            related_db_entity_key: the db_entity_key of the config_entity whose feature_class is the relation type
            related_class_name: any model class, such as BuiltForm, to relate to.
            single: if True this is a ForeignKey (toOne) relationship. Otherwise a ManyToMany is created
        :return: A tuple. First item is the field name and the value is the field.
        """
    
        config_entity = ConfigEntity._subclassed_config_entity_by_id(self.db_entity.feature_class_configuration['scope'])
        if related_field_configuration.get('related_db_entity_key', None):
            # field name matches name of peer self.db_entity_key--get it's feature class name
            related_db_entity = get_single_value_or_none(config_entity.computed_db_entities(key=related_field_configuration['related_db_entity_key']))
            related_class_name_or_model = FeatureClassCreator(self.config_entity, related_db_entity).dynamic_feature_class()
        elif related_field_configuration.get('related_class_name', None):
            # A model class such as BuiltForm
            related_class_name_or_model = resolve_module_attr(related_field_configuration['related_class_name'])
        else:
            raise Exception("No related_db_entity_key or related_class_name found on feature_class_configuration for self.db_entity %s" % self.db_entity.key)

        if related_field_configuration.get('single', None):
            return [field_name,
                    models.ForeignKey(related_class_name_or_model, null=True)]
        else:
            return [field_name,
                    models.ManyToManyField(related_class_name_or_model,
                            # Pass a custom, readable table name for the through class for ManyToMany relations
                            db_table='"{schema}"."{table}_{field_name}"'.format(
                                schema=self.db_entity.feature_class_configuration['schema'],
                                table=self.db_entity.feature_class_configuration['table'],
                                field_name=field_name))]

    def merge_feature_class_configuration_into_db_entity(self, feature_class_configuration):
        # Update our DbEntity so we have the configuration available for future operations
        # Note that we always want to generate the feature_class_configuration here if its generated in case
        # the table schema is updated and we need to modify the configuration
        self.db_entity.feature_class_configuration = merge(
            self.db_entity.feature_class_configuration,
            feature_class_configuration)
        # Disable signals and update the DbEntity
        self.db_entity._no_post_post_save = True
        self.db_entity.save()
        self.db_entity._no_post_post_save = False

# coding=utf-8
# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System. #
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
from __builtin__ import classmethod
import logging
from django.contrib.auth.models import User

from django.contrib.gis.db import models
import guppy
from footprint.main.lib.functions import flat_map, unique
from footprint.main.mixins.categories import Categories
from footprint.main.mixins.config_entity_related_collection_adoption import ConfigEntityRelatedCollectionAdoption
from footprint.main.mixins.config_entity_selection import ConfigEntitySelection
from footprint.main.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.main.mixins.db_entities import DbEntities
from footprint.main.mixins.deletable import Deletable
from footprint.main.mixins.related_collection_adoption import RelatedCollectionAdoption
from footprint.main.mixins.scoped_key import ScopedKey
from footprint.main.mixins.built_form_sets import BuiltFormSets
from footprint.main.mixins.geographic_bounds import GeographicBounds
from footprint.main.mixins.name import Name
from footprint.main.mixins.policy_sets import PolicySets
from footprint.main.models.config.model_pickled_object_field import SelectionModelsPickledObjectField
from footprint.main.utils.utils import resolve_module_attr

__author__ = 'calthorpe_associates'
logger = logging.getLogger(__name__)

class ConfigEntity(
        ConfigEntityRelatedCollectionAdoption,
        ConfigEntitySelection,
        RelatedCollectionAdoption,
        GeographicBounds,
        PolicySets,
        BuiltFormSets,
        DbEntities,
        Name,
        ScopedKey,
        Categories,
        Deletable):
    """
        The base abstract class defining and UrbanFootprint object that is configurable
    """

    def __init__(self, *args, **kwargs):
        super(ConfigEntity, self).__init__(*args, **kwargs)
        if hasattr(self, 'parent_config_entity') and self.parent_config_entity and not self.bounds:
            self.bounds = self.parent_config_entity.bounds

    objects = GeoInheritanceManager()

    # TODO this should be set to null=False and required
    # The user who created the config_entity
    creator = models.ForeignKey(User, null=True, related_name='config_entity_creator')
    # The user who last updated the db_entity
    updater = models.ForeignKey(User, null=True, related_name='config_entity_updater')

    media = models.ManyToManyField('Medium', null=True)

    # Use parent_config_entity_subclassed() to get the actual subclass, not a generic config_entity instance
    parent_config_entity = models.ForeignKey('ConfigEntity', null=True, related_name='parent_set')
    def parent_config_entity_subclassed(self):
        return ConfigEntity.objects.get_subclass(id=self.parent_config_entity.id) if self.parent_config_entity else None

    # The optional config_entity whence this instance was cloned.
    origin_config_entity = models.ForeignKey('ConfigEntity', null=True, related_name='clone_set')
    def origin_config_entity_subclassed(self):
        return ConfigEntity.objects.get_subclass(id=self.parent_config_entity.id) if self.parent_config_entity else None

    db = 'default'

    # The selected policy_set, built_form_set, and anything else that could conceivably be selected
    # Currently selected sets are stored in a dictionary of the 'sets' key and selected DbEntities (when multiple DbEntities of the same key are present) are stored in a dictionary of the 'db_entities' key
    selections = SelectionModelsPickledObjectField(default=lambda: {'sets': {}, 'db_entities': {}})

    # Temporary state during post_save to disable recursing on post_save publishers
    _no_post_save_publishing = False
    # Temporary state during post_save to disable invoking the publishers upon db_entity_interest save
    _no_post_save_db_entity_interest_publishing = False

    def donor(self):
        """
            Used by the RelatedCollectionAdoption mixin
        :return:
        """
        return self.parent_config_entity_subclassed()

    # The collections listed here (defined in the various mixins) behave similarly. They are many-to-many collections. When computed_COLLECTION_NAME() is called, the returned values are either 1) if this instance has no items in its own collection, the values of the first ancestor via parent which has items set in its collection of the same name 2) if this instance has added items to its collection via add_COLLECTION_NAME(*items), then the parent's computed_COLLECTION_NAME() items are first inherited to this instance's collection (references, not clones), and then the items given are added. The end result is if no items exist for the instance, computed_COLLECTION_NAME returns the combined values of the ancestors. If items were added for the instance, computed_COLLECTION_NAME() returns the combined values of the ancestors followed by the instances own unique items. Duplicate items, as identified by the items' pk, are ignored by add_COLLECTION_NAME(*items)
    # This pattern of collection inheritance is common enough that the functionality could be added to the Django model framework by extending certain classes, but I haven't invested the time in doing this. The logic resides in ConfigEntitySets for now
    INHERITABLE_COLLECTIONS = ['db_entities', 'built_form_sets', 'policy_sets']
    # Because DbEntityInterest uses a through class (and others might in the future), this dict should be used to resolve the add and remove functions

    def __unicode__(self):
        return '{0} ({1})'.format(self.name, self.__class__.__name__)

    class Meta(object):
        abstract = False # False to allow multi-table-inheritance with many-to-many relationship
        app_label = 'main'

    def children(self):
        """
            Executes a query to return all children of this ConfigEntity. It's up to the caller to call the InheritanceManager.subclasses to 'cast' to the classes that they expect
        :return:
        """
        return ConfigEntity.objects.filter(parent_config_entity=self, deleted=False)

    def deleted_children(self):
        return ConfigEntity.objects.filter(parent_config_entity=self, deleted=True)

    def parent_config_entity_saved(self):
        """
            Called whenever the parent_config_entity's attributes are updated
        :return:
        """
        pass

    def config_keys(self):
        return self.parent_config_entity.config_keys() + [self.key] if self.parent_config_entity else [self.key]

    def schema(self):
        """
            The database schema name, created by concatinating this instance's key and its parents with underscores, where the top-most region is the first key, followed by sub-regions, project, and finally scenario
        :return: underscore concatinated schema name
        """
        return "__".join(self.config_keys()[1:]) if self.parent_config_entity else self.config_keys()[0]


    def get_selected_db_entity(self, key):
        """
            Returns the DbEntity with the given key that has been selected using _select_db_entity
        :param key:
        :return:
        """
        db_entities = self.get_db_entities_by_key(key)
        selection = self.selections['db_entities'].get(key, None)
        if selection:
            return selection
        if len(db_entities) == 1:
            return db_entities[0]
        raise Exception(
            "Instance {0} has no selected DbEntity for key {1} and there is not exactly one DbEntity with that key, rather {2}. Existing DbEntity keys: {3}".format(
                self,
                key,
                len(db_entities),
                map(lambda db_entity_interest: db_entity_interest.db_entity, self.computed_db_entity_interests())))

    def get_db_entities_by_key(self, key):
        """
            Gets the DbEntities of the instance with the given key. More than one DbEntity may have the same key in
            the case that several alternate tables are available for a given function. Use get_selected_db_entity
            to guarantee only one DbEntity is returned

        :param key: The key attribute of the DbEntity
        :return: The mat            return db_entities[0]ching DbEntities
        """
        return self.computed_db_entities(key=key)

    def resolve_db_entity(self, table, schema=None):
        """
            Search for a entity with the given table (and schema).
        :param table: the name of the table
        :param schema: the optional name of the DbEntity's schema.
        :return: a DbEntity instance matching the table and schema belonging to the instance or the first ancestor that has it
        """
        self._get('db_entities', table=table, schema=schema)


    def resolve_db(self):
        # This could be used to configure horizontal databases if needed
        return 'default'

    def full_name(self):
        """
            Concatinates all ancestor names except for that of the GlobalConfig. Thus a full name might be region_name subregion_name project_name scenario_name
        """
        return ' '.join(self.parent_config_entity.full_name().extend([self.key])[1:])

    def feature_class_of_base_class(self, base_class):
        """
            Finds the feature_class of this config_entity that is derived from the given base class
        :param base_class:
        :return:
        """
        db_entities = filter(lambda db_entity: issubclass(
                                # Get the configured abstract class
                                # The class_key is a hack to prevent Result db_entities from being chosen
                                resolve_module_attr(db_entity.feature_class_configuration.get('abstract_class', object)),
                                base_class) and not db_entity.class_key,
                             self.computed_db_entities())
        if len(db_entities) != 1:
            raise Exception(
                "Expected exactly one db_entity matching the base_class {0} but got {1}".format(base_class,
                                                                                                db_entities if len(db_entities) > 0 else 'none'))
        return self.feature_class_of_db_entity_key(db_entities[0].key)

    def db_entity_feature_class(self, key, abstract_class=False, base_class=False):
        """
            Resolves the Feature class subclass of this config_entity for the given key, or the base class version
            if base_class-True
        :param key:
        :param abstract_class, Default False, if True returns the abstract base class instead of the subclass
        :param base_class, Default False, if True returns the base class instead of the default rel class
        :return:
        """
        db_entity = self.computed_db_entities().get(key=key)
        class_key = db_entity.class_key if db_entity.class_key else key
        # Resolve the class_key of the DbEntity or just use key
        from footprint.main.models.geospatial.feature_class_creator import FeatureClassCreator
        if abstract_class:
            subclass = resolve_module_attr(db_entity.feature_class_configuration['abstract_class'])
        elif base_class:
            subclass = FeatureClassCreator(self, db_entity).dynamic_feature_class(base_only=True)
        else:
            subclass = FeatureClassCreator(self, db_entity).dynamic_feature_class()
        if not subclass:
            raise Exception(
                "For config_entity {0} no class associated with db_entity_key {1}{2}. Register a table in default_db_entity_configurations() of the owning config_entity.".
                format(unicode(self), key, ", even after resolving class_key to {0}".format(class_key) if class_key != key else ''))
        return subclass

    def clone_db_entities(self):
        """
            If this ConfigEntity has an origin_config_entity, update or create the former's db_entity by copying the
            latter's, if they are not already present.
        :return:
        """
        if not self.origin_config_entity:
            raise Exception("Cannot clone a config_entity's db_entities which lacks an origin_config_entity")
        origin_db_entity_interests = self.origin_config_entity_subclassed.computed_db_entity_interests

        # Sync the db_entities, instructing the method to clone from the origin
        # TODO figure this out
        #sync_db_entities()

    def feature_class_of_db_entity_key(self, key):
        """
            If a db_entity maps to a base model class, this method will create a subclass to map the db_entry's table.
            This is needed since tables of the same base type occur multiple times in the database and are created
            dynamically in the scope of a ConfigEntity
            The created class can then be used as a normal model class to query for instances and persist instances
            The class is always given a reference to the config_entity instance in case queries need to join with it.
            Returns the dynamic subclass associated with a given DbEntity table
            Important: For DbEntities adopted from the parent_config_entity, the generated table and subclass are in
            the context of the parent_config_entity or whatever ancestor defined the DbEntity.
            The adopting config_entity (self) doesn't get its own table and class unless it specifically clones the
            table (which isn't supported yet but easily could be.)
        :param key: The key and table name of the DbEntity instance
        :return: the dynamically created subclass
        """
        return self.db_entity_feature_class(key)

    def has_feature_class(self, db_entity_key):
        try:
            self.feature_class_of_db_entity_key(db_entity_key)
            return True
        except Exception:
            return False

    def abstract_class_of_db_entity(self, key):
        """
            Like feature_class_of_db_entity, but returns the base abstract Feature class instead of the subclass
        :param key:
        :return:
        """
        return self.db_entity_feature_class(key, abstract_class=True)


    @classmethod
    def lineage(cls, discovered=[]):
        """
            Returns the hierarchy of parent classes of this class. Duplicates are ignored. Order is from this class up
            until GlobalConfig
        :param cls:
        :return:
        """
        return unique([cls] + flat_map(lambda parent_class: parent_class.lineage(discovered + cls.parent_classes()),
                                       filter(lambda parent_class: parent_class not in discovered,
                                              cls.parent_classes())))

    def db_entity_owner(self, db_entity):
        """
            Returns the ConfigEntity that owns the db_entity, either self or one of its ancestors
        :param db_entity:
        :return:
        """
        return self if self.schema() == db_entity.schema else self.parent_config_entity_subclassed().db_entity_owner(
            db_entity)

    def owned_db_entities(self, **query_kwargs):
        """
            Returns non-adopted DbEntity instances
        """
        return map(lambda db_entity_interest: db_entity_interest.db_entity,
                   self.owned_db_entity_interests(**query_kwargs))

    def owned_db_entity_interests(self, **query_kwargs):
        """
            Returns non-adopted DbEntityInterest instances
        """
        return filter(lambda db_entity_interest: db_entity_interest.db_entity.schema == self.schema(), self._computed('db_entities', **query_kwargs))

    def expect_parent_config_entity(self):
        if not self.parent_config_entity:
            raise Exception("{0} requires a parent_config_entity of types(s)".format(
                self.__class__.__name__,
                ', '.join(self.__class__.parent_classes())))

    @property
    def subclassed_config_entity(self):
        """
            Resolves the config_entity to its subclass version. This garbage should all be done elegantly by Django,
            maybe in the newest version. Otherwise refactor to generalize
        :return:
        """
        return ConfigEntity._subclassed_config_entity(self)

    _subclassed_config_entity_lookup = {}

    @classmethod
    def _subclassed_config_entity(cls, config_entity):
        """
            Cache subclassed config_entities to compensate for Djangos apparent inability to store these on models with ConfigEntity ForeignKeys
        :param id:
        :return:
        """
        id = config_entity.id
        return cls._subclassed_config_entity_by_id(id)

    @classmethod
    def _subclassed_config_entity_by_id(cls, id):
        subclassed_config_entity = cls._subclassed_config_entity_lookup.get(id, None)
        if not subclassed_config_entity:
            cls._subclassed_config_entity_lookup[id] = cls.resolve_scenario(
                ConfigEntity.objects.get_subclass(id=id))
        return cls._subclassed_config_entity_lookup[id]

    # Cache for the instance's dynamically  models
    _dynamic_models_created = False

    @staticmethod
    def resolve_scenario(config_entity):
        for scenario_type in ['basescenario', 'futurescenario']:
            if hasattr(config_entity, scenario_type):
                return getattr(config_entity, scenario_type)
        return config_entity

    # System memory usage (nothing to do with ConfigEntity)
    _heapy = None
    @classmethod
    def init_heapy(cls):
        ConfigEntity._heapy = guppy.hpy()

    @classmethod
    def dump_heapy(cls):
        # Print memory statistics
        print cls._heapy.heap()
        # Print relative memory consumption w/heap traversing
        print cls._heapy.heap().get_rp(40)

    @classmethod
    def start_heapy_diagnosis(cls):
        cls._heapy.setrelheap()

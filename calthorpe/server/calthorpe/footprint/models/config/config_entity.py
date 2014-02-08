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
from picklefield import PickledObjectField
from footprint.lib.functions import merge, flat_map, unique, first
from footprint.mixins.categories import Categories
from footprint.mixins.config_entity_related_collection_adoption import ConfigEntityRelatedCollectionAdoption
from footprint.mixins.config_entity_selection import ConfigEntitySelection
from footprint.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.mixins.db_entities import DbEntities
from footprint.mixins.related_collection_adoption import RelatedCollectionAdoption
from footprint.mixins.scoped_key import ScopedKey
from footprint.models.config.config_entity_db_entity_setup import ConfigEntityDbEntitySetup
from footprint.models.database.information_schema import PGNamespace
from footprint.models.config.db_entity_interest import DbEntityInterest
from footprint.models.config.interest import Interest
from footprint.mixins.built_form_sets import BuiltFormSets
from footprint.mixins.geographic_bounds import GeographicBounds
from footprint.mixins.name import Name
from footprint.mixins.policy_sets import PolicySets
from footprint.models.keys.keys import Keys

__author__ = 'calthorpe'
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
        ConfigEntityDbEntitySetup):
    """
        The base abstract class defining and UrbanFootprint object that is configurable
    """

    def __init__(self, *args, **kwargs):
        super(ConfigEntity, self).__init__(*args, **kwargs)
        if hasattr(self, 'parent_config_entity') and self.parent_config_entity and not self.bounds:
            self.bounds = self.parent_config_entity.bounds

    objects = GeoInheritanceManager()

    creator = models.ForeignKey(User, null=True);
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
    selections = PickledObjectField(default=lambda: {'sets': {}, 'db_entities': {}})

    # Temporary state during post_save
    _no_post_post_save = False

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
        app_label = 'footprint'

    def children(self):
        """
            Executes a query to return all children of this ConfigEntity. It's up to the caller to call the InheritanceManager.subclasses to 'cast' to the classes that they expect
        :return:
        """
        return ConfigEntity.objects.filter(parent_config_entity=self)

    def parent_config_entity_saved(self):
        """
            Called whenever the parent_config_entity's attributes are updated
        :return:
        """
        pass

    def __setattr__(self, attrname, val):
        super(ConfigEntity, self).__setattr__(attrname, val)

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

    def full_name_of_db_entity_table(self, table):
        """
        :param table: the table name of the table that the DbEntity represents
        :return: The combined schema and table name of the given db_entity. This is used to name the dynamic class that is created to represent the table
        """
        return '"{0}"."{1}"'.format(self.schema(), table)

    def class_name_of_db_entity(self, clazz):
        """
            Returns the subclass name of the subclass generated for the table of this DbEntity. The name is the base class plus the ConfigEntity id
        :param table_name: the table name of the table that the DbEntity represents
        :param clazz:
        :return:
        """
        return '{0}__{1}'.format(clazz.__name__, self.id)


    def create_table_of_db_entity(self, db_entity, clazz):
        """
            Databaase tables of ConfigEntity instances, such as the base, canvas, etc. need to be created based on the given clazz definition. Although clazz is always a subclass of an abstract class, the table should not be constructed to use table inheritance, since there is no sense in having a base table whose subtables span schemas and have no id collision potential
        :param db_entity:
        :param clazz:
        :return:
        """
        pass


    def default_db_entity_setups(self):
        """
            Defines the relationship between DbEntities and the model base classes that represent them. The format
            of the returned structure [{db_entity:DbEntity instance, feature_class:dynamic subclass}, ...]. The feature
            class is optional since the table doesn't necessarily need to be modeled in Django.
        :return:
        """
        return []

    def accumulated_default_db_entities_and_classes(self):
        return self.default_db_entity_setups() + self.parent_config_entity_subclassed().accumulated_default_db_entities_and_classes() if self.parent_config_entity else []

    def feature_class_of_base_class(self, base_class):
        """
            Finds the feature_class of this config_entity that is derived from the given base class
        :param base_class:
        :return:
        """
        db_entity_setups = filter(lambda db_entity_setup:
                                  issubclass(db_entity_setup.get('feature_class', object),
                                             base_class),
                                  self.accumulated_default_db_entities_and_classes())
        if len(db_entity_setups) != 1:
            raise Exception(
                "Expected exactly one db_entity_setup matching the base_class {0} but got {1}".format(base_class,
                                                                                                      db_entity_setups if len(
                                                                                                          db_entity_setups) > 0 else 'none'))
        return db_entity_setups[0]['feature_class']

    def _db_entity_feature_class(self, key, base_class=False):
        """
            Resolves the Feature class subclass of this config_entity for the given key, or the base class version
            if base_class-True
        :param key:
        :param base_class, Default False, if True returns the abstract base class instead of the subclass
        :return:
        """
        db_entity = self.get_selected_db_entity(key)
        # Resolve the owning config_entity of the db_entity
        try:
            owning_config_entity = self.db_entity_owner(db_entity)
        except Exception, e:
            raise Exception(
                "No DbEntity owner. DbEntity schema: {0}. ConfigEntity schema: {1}. Original exception: {2}".format(
                    db_entity.schema, self.schema(), e.message))
            # Resolve the class_key of the DbEntity or just use key
        class_key = db_entity.class_key if db_entity.class_key else key
        # Find the registration matching the DbEntity.class_key or else the given ke
        # class_key is used by cloned DbEntities, like Result DbEntities, to resolve the class of the source DbEntity
        db_entity_setup = self.get_db_entity_setup(owning_config_entity.accumulated_default_db_entities_and_classes(),
                                                   class_key)
        subclass = db_entity_setup.get('base_class' if base_class else 'feature_class',
                                       None) if db_entity_setup else None
        if not subclass:
            raise Exception(
                "For config_entity {0} no class associated with db_entity_key {1}{2}. Register a table in default_db_entity_setups() of the owning config_entity.".
                format(unicode(self), key, ", even after resolving class_key to {0}".format(class_key) if class_key != key else ''))
        return subclass

    def sync_default_db_entities(self):
        """
            Update or create the default DbEntities for this config_entity and also create the subclass database table if the
            DbEntity is associated with a base model class. Association with a base model class implies that this
            ConfigEntity needs a dynamic subclass of the base model class and that class needs a corresponding table in
            the database.
        :return:
        """
        self.sync_db_entities(*self.default_db_entity_setups())

    def clone_db_entities(self):
        """
            If this ConfigEntity has an origin_config_entity, update or create the former's db_entity by copying the
            latter's, if they are not already present.
        :return:
        """
        if not self.origin_config_entity:
            raise Exception("Cannot clone a config_entity's db_entities which lacks an origin_config_entity")
        origin_db_entity_setups = self.origin_config_entity_subclassed.default_db_entity_setups()
        # Find or create all db_entity_setups of the origin by iterating through its db_entity_interests
        db_entity_setups = map(
            # Match the db_entity to a default db_entity_setup or if not a default simply make a db_entity_setup
            lambda db_entity_interest: self.__class__.get_db_entity_setup(
                origin_db_entity_setups,
                db_entity_interest.db_entity.key) or
            dict(db_entity=db_entity_interest.db_entity))

        # Sync the db_entities, instructing the method to clone from the origin
        self.sync_db_entities(*db_entity_setups, clone=True)


    @staticmethod
    def get_db_entity_setup(db_entity_setups, db_entity_key):
        """
            Return thd db_entity_setup matching the given key
        :param db_entity_setups:
        :param db_entity_key:

        :return:
        """
        return first(lambda default: default['key'] == db_entity_key, db_entity_setups)

    def feature_class_of_db_entity(self, key):
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
        return self._db_entity_feature_class(key)

    def has_feature_class(self, db_entity_key):
        try:
            self.feature_class_of_db_entity(db_entity_key)
            return True
        except Exception:
            return False

    def base_class_of_db_entity(self, key):
        """
            Like feature_class_of_db_entity, but returns the base abstract Feature class instead of the subclass
        :param key:
        :return:
        """
        return self._db_entity_feature_class(key, base_class=True)

    def clone_db_entity_and_interest(self, reference_db_entity_key, **kwargs):
        """
            Clone the selected db_entity of key reference_db_entity and replace any of its attributes with those
            specified in **kwargs. Normally **kwargs will contain a unique key, unless another version of the table
            with the same key is desired, such a version that filters values by query, but that is probably a bad
            practice. **kwargs must contain at least one a name to distinguish it from the source DbEntity
        :param reference_db_entity_key: key of the DbEntity to clone
        :param kwargs: replacement values containing at the very least 'key'
        :return: The DbEntityInterest which references the cloned db_entity
        """
        db_entity = self.get_selected_db_entity(reference_db_entity_key)

        # Prefer the kwargs values over those of the db_entity
        # _update_or_create_db_entity will ignore keys like id, so we don't have to remove them
        db_entity_config = merge(
            db_entity.__dict__,
            kwargs,
            dict(class_key=reference_db_entity_key)
        )
        # Persist the db_entity. The result of this should be passed to config_db_entities to setup the DbEntityInterest
        self.db_entities.filter(key=db_entity_config['key']).delete()
        db_entity = self._update_or_create_db_entity(**db_entity_config)
        interest = Interest.objects.get(key=Keys.INTEREST_OWNER)
        return DbEntityInterest.objects.update_or_create(
            config_entity=self,
            db_entity=db_entity,
            interest=interest)[0]

    @classmethod
    def parent_classes(cls):
        """
            Returns all classes that can be a parent of the class
        :return:
        """
        raise Exception("Abstract method reached")

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

    def expect_parent_config_entity(self):
        if not self.parent_config_entity:
            raise Exception("{0} requires a parent_config_entity of types(s)".format(
                self.__class__.__name__,
                ', '.join(self.parent_classes())))

    def post_create(self):
        # Create the database schema for this ConfigEntity's feature table data
        PGNamespace.objects.create_schema(self.schema())
        # If the ConfigEntity is being created by cloning
        self.sync_default_db_entities()
        #if self.origin_config_entity:
            # Create the default DbEntities
        #    self.clone_db_entities()
        #else:
            # Create the default DbEntities
        #    self.sync_default_db_entities()

        # Disable the post_post_save signal while saving to prevent an infinite loop
        self._no_post_post_save = True
        # Save post_create changes.
        self.save()
        self._no_post_post_save = False


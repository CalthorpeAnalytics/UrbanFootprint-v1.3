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
from footprint.main.lib.functions import flat_map, unique
from footprint.main.mixins.analysis_modules import AnalysisModules
from footprint.main.mixins.categories import Categories
from footprint.main.mixins.cloneable import Cloneable
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
        AnalysisModules,
        Name,
        ScopedKey,
        Categories,
        Deletable,
        Cloneable):
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

    # Designates the key prefix for database imports
    import_key = models.CharField(max_length=64, null=True)

    def parent_config_entity_subclassed(self):
        return self.parent_config_entity.subclassed_config_entity if self.parent_config_entity else None

    # The optional config_entity whence this instance was cloned.
    def origin_instance_subclassed(self):
        return self.origin_instance.subclassed_config_entity if self.origin_instance else None

    db = 'default'

    # The selected policy_set, built_form_set, and anything else that could conceivably be selected
    # Currently selected sets are stored in a dictionary of the 'sets' key and selected DbEntities (when multiple DbEntities of the same key are present) are stored in a dictionary of the 'db_entities' key
    selections = SelectionModelsPickledObjectField(default=lambda: {'sets': {}, 'db_entities': {}})

    # Temporary state during post_save to disable recursing on post_save publishers
    _no_post_save_publishing = False

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

    def expect_parent_config_entity(self):
        if not self.parent_config_entity:
            raise Exception("{0} requires a parent_config_entity of types(s)".format(
                self.__class__.__name__,
                ', '.join(self.__class__.parent_classes())))

    def resolve_db(self):
        # This could be used to configure horizontal databases if needed
        return 'default'

    @property
    def full_name(self):
        """
            Concatinates all ancestor names except for that of the GlobalConfig. Thus a full name might be region_name subregion_name project_name scenario_name
        """
        return ' '.join(self.parent_config_entity.full_name.extend([self.key])[1:])

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

    @staticmethod
    def resolve_scenario(config_entity):
        for scenario_type in ['basescenario', 'futurescenario']:
            if hasattr(config_entity, scenario_type):
                return getattr(config_entity, scenario_type)
        return config_entity

    # Cache for the instance's dynamically  models
    _feature_classes_created = False
    _analysis_modules_created = False

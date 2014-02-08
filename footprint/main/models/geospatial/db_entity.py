# coding=utf-8
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
import re
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from inflection import titleize
from picklefield import PickledObjectField
import sys
from footprint.main.lib.functions import map_dict, accumulate, map_to_dict
from footprint.main.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.main.mixins.deletable import Deletable
from footprint.main.mixins.name import Name
from footprint.main.mixins.shared_key import SharedKey
from footprint.main.mixins.tags import Tags
from footprint.main.models.geospatial.feature_class_creator import FeatureClassCreator
from footprint.main.utils.utils import database_connection_string_for_pys, resolve_module_attr
from footprint.main.utils.uf_toolbox import report_sql_values_as_dict

__author__ = 'calthorpe_associates'
logger = logging.getLogger(__name__)

class DbEntity(SharedKey, Name, Tags, Deletable):
    """
        Represents a database-derived entity, such as a table, view, or query result. Entities may have tags to help entity_configs that may be interested in them. The relationships between db_entities and entity_configs are registered by the DbEntityInterest class, which also defines the type of interest. Some db_entities are "owned" by one entity_config, while others might simply have an "observe" or "edit" or "dependency" relationship. These roles will be figured out later. The key indicates a specific function of the db_entity, such as "base" to indicate a table used for base data. Tags are broader descriptors, such as "university", used for categorization or queries. DbEntities use the SharedKey mixin to permit multiple DbEntities in the same context (e.g. those of a particular ConfigEntity interest) to share a key. This permits the user to assign multiple tables of the same key (e.g. 'base') to a ConfigEntity instance. The ConfigEntity instance tracks which DbEntity is the default in this situation (see ConfigEntity.selections['db_entities'] and defaults if only one DbEntity with a particular key is present)
    """
    objects = GeoInheritanceManager()

    # The optional schema and table or view name from which to base the layer. This will result in a query that selects all
    # rows from the table, and the table will be used to configure TileStache or Geoserver.
    # These might also identify the query as operating on the specified table and thus be useful for organization
    schema = models.CharField(max_length=100, null=True)
    table = models.CharField(max_length=100, null=True)
    srid = models.CharField(max_length=100, null=True)

    # The origin of this DbEntiy if cloned from a peer
    origin_instance = models.ForeignKey('DbEntity', null=True)

    # TODO these should be set to null=False and required
    # The user who created the db_entity
    creator = models.ForeignKey(User, null=True, related_name='db_entity_creator')
    # The user who last updated the db_entity
    updater = models.ForeignKey(User, null=True, related_name='db_entity_updater')

    # Describes how to configure the features of the table
    feature_class_configuration = PickledObjectField(null=True)

    @property
    def full_table_name(self):
        """
            Return the schema in table in the syntax usable by Django model classes '"schema"."table"'
        :return:
        """
        return '"{0}"."{1}"'.format(self.schema, self.table)

    @property
    def full_name(self):
        """
            Returns the name of the DbEntity with the titleized schema to distinguish it
        """
        return "{0} for {1}".format(self.name, titleize(self.schema) if self.schema else 'Global Config')

    def resolve_abstract_feature_class(self):
        """
            Extracts the abstract Feature class from the DbEntity configuration
            :return The abstract class or None if not configured
        """
        abstract_class_path = self.feature_class_config.get('abstract_class', None)
        return resolve_module_attr(abstract_class_path) if abstract_class_path else None

    extent_authority = models.BooleanField(default=False)

    # Remote data, such as background layers, use a url instead of schema and table or as an import source
    url = models.CharField(max_length=1000, null=True)
    # An array of host url prefixes for url based db_entities
    hosts = PickledObjectField(null=True)

    # Flag to prevent signal recursion during a save
    _no_post_post_save = False

    # TODO replace format with SC token format
    # Pickle the Django QuerySet configuration. The manager used is always the manager of the ad hoc class that represents
    # the DbEntity via its table argument. There might be a way to have a manager not associated with a table, but that isn't
    # yet supported. configuration is an array of queryset items to chain together to form the queryset
    # [
    #   (values, ['name', 'year']),
    #   (annotate, dict(average_rating=dict(Avg='book__rating'))),
    #   (filter, dict(name__like='Bob%')).
    #   (order_by, ['name', 'year'])
    # ]
    # means:
    #  ad_hoc_class.objects.values('name').annotate(average_rating=Avg('book__rating')).order_by('name','year')
    # Every tuple has a command and args. The former represents a function such as values, annotate aggregate, order_by
    # The latter are either a column/alias path, array of such, or a dictionary for kwargs
    # Every kwarg key at the second level is column/alias path and the value is a primitive or dict
    # These innermost dicts represent functions where the key is the function name and the value is a primitive or
    # column/alias path
    # The values snd annotate clause above causes a group_by, which should actually be specified by the same format in group_by
    # so that it can be overridden by alternative an group_by or values
    query = PickledObjectField(null=True)

    # Holds key that points to dynamic class info for this DbEntity. This key is normally None or the key of another
    # DbEntity, the latter if this DbEntity was cloned from another
    class_key = models.CharField(max_length=50, null=True)

    @property
    def is_clone(self):
        return self.class_key and self.class_key != self.key


    # The same format, but only one dict is expected instead of an array
    # If the group_by dict is present, it will be preprended to the query dicts to form the QuerySet definition
    group_by = PickledObjectField(null=True)

    def run_query(self, config_entity, **kwargs):
        """
            Prepends the given or default group_by (if any) and/or optional values to the query, runs the query, and returns results
            TODO Since ordering of query parts makes a big difference, we might have to let kwargs specify positions in the query
        :param kwargs['group_by']: use this group_by or the else self.group_by or else no group_by
        :param kwargs['values']: use this values to force the query to only return certain fields,
        and to return dicts instead of instances. Only pass values if not already defined in the query or group_by field
        :return:
        """

        full_query = self._add_to_query(**kwargs) if len(kwargs.keys()) > 0 else None
        return self.parse_query(config_entity, full_query)

    def _add_to_query(self, **kwargs):
        return kwargs.get('values', []) + kwargs.get('group_by', self.group_by or []) + self.query

    # TODO this is all used only for results and will be replaced by the Sproutcore style stuff in query_parsing
    def parse_query(self, config_entity, query=None):
        """
            Parses the stored QuerySet components of the DbEntity to create an actual QuerySet
            :param query: pass in a query instead of using self.query. Used by run_grouped_query to add the group_by
        :return:
        """
        query = query or self.query
        if not query:
            logger.error("Trying to run query for db_entity %s, which has no query defined or passed in" % self.full_name)
            return {}

        # Use the base table of the Feature class for now. We'll need to use the rel table soon.
        manager = config_entity.feature_class_of_db_entity_key(self.key).__base__.objects
        if isinstance(query, basestring):
            # String query
            # Join the query with the base tables of the feature classes that match the db_entity_keys listed
            # as named wildcards in the query string They are in the form %(db_entity_key)
            db_entity_keys = re.findall(r'%\((.+?)\)', query)
            return report_sql_values_as_dict(
                query % map_to_dict(
                    lambda db_entity_key: [db_entity_key, config_entity.feature_class_of_db_entity_key(db_entity_key).__base__._meta.db_table],
                    db_entity_keys),
                database_connection_string_for_pys(config_entity.db))[0] # assume aggregate
        else:
            # Combine the query parts
            return accumulate(lambda manager, queryset_command: self.parse_and_exec_queryset_command(manager, queryset_command), manager, query)

    def parse_and_exec_queryset_command(self, manager, queryset_command):
        """
            A queryset command is a two item tuple of a command and args, the command is e.g. values, annotate, or order_by, and
            args are as described in the DbEntity.query docs--a single column/alias path, array of such or kwargs.
        :param queryset_command:
        :return:
        """
        if len(queryset_command) != 2:
            raise Exception("Expected queryset_command to be a two item tuple, but got %s".format(queryset_command))
        command, arguments = queryset_command
        # Fetch the command from the manager by name and call it with the parsed arguments
        return getattr(manager, command)(*self.parse_queryset_command_arguments(arguments))

    def parse_queryset_command_arguments(self, queryset_command_arguments):
        """
            Handles the argument whether a single item, list, or dict, and returns the parsed item(s) in the same
            form. For dicts, keys are passed through and the values are parsed
        :param queryset_command_arguments:
        :return:
        """
        return map(
            lambda argument: self.parse_queryset_inner_argument(argument),
            queryset_command_arguments)

    def parse_queryset_inner_argument(self, argument):
        """
            The inner arguments of the queryset command are either a simple column/alias path or a dict in the
            case of aggregate functions, e.g. dict(Avg='book__rating') to indicate Avg('book__rating')
        :param argument:
        :return:
        """
        if isinstance(argument, dict):
            return map_dict(lambda key, value: self.resolve_models_class(key)(value), argument)[0]
        return argument

    def resolve_models_class(self, class_name):
        """
            Lookups up classes by string name for aggregate classes like Avg
            This could be extended to support other aggregate classes defined elsewhere
        :param class_name: unpackaged class name like 'Avg' stored in the query definition
        :return: The class
        """
        return getattr(sys.modules['django.db.models'], class_name)

    @property
    def has_db_url(self):
        """
            Indicates whether or not the DbEntity url is configured to point to a postgres database
        :return:
        """
        return self.url and self.url.startswith('postgres://')

    @property
    def has_file_url(self):
        """
            Indicates whether or not the DbEntity url is configured to point to a file location
        :return:
        """
        return self.url and self.url.startswith('file://')

    @property
    def importable(self):
        """
            Indicates if the DbEntity has the right characteristics for importing feature data.
        """
        return self.has_db_url or self.has_file_url or (self.origin_instance and self.origin_instance.importable)

    def __unicode__(self):
        return self.name

    class Meta(object):
        abstract = False # False to allow multi-table inheritance many-to-many relationship
        app_label = 'main'


# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
#
# Copyright (C) 2013 Calthorpe Associates
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
import re
import string
from south.db import db
from django.db import models
from django.db.models.signals import class_prepared
from tastypie.resources import ModelDeclarativeMetaclass
from footprint.lib.functions import merge
from footprint.managers.geo_inheritance_manager import GeoInheritanceManager

# Creates a model based on the given abstractClass and customTable name
# This allows us to map dynamically created tables such as those in the inputs_outputs_* schemas
from footprint.utils.utils import parse_schema_and_table, resolve_model


def get_dynamic_model_class(abstract_class, schema, table, class_name=None, class_attrs={}, fields={}, scope=None):
    """
    :param abstract_class: The abstract class to subclass. This doesn't actually have to be abstract and could simply be object
    :param schema: The schema of the table.
    :param table: The table name. Used for Meta.db_table
    :param class_name: The name to use for the class. If not specified the name will be formed from the table_name
    :param class_attrs: Nonmodel attributes to add to the subclass
    :param fields: Model fields to add to the subclass, such as ForeignKey, ManyToMany, etc
    :param scope: Optional. A model instance which represents the scope of this subclass. The id is used to form the class name
    :return:
    """

    computed_name = class_name or get_dynamic_model_class_name(abstract_class, scope.id if scope else '') # TODO use something random, not ''
    try:
        # Return the model class if already created
        resolved_model = resolve_model('footprint.{0}'.format(computed_name))
        if resolved_model:
            return resolved_model
    except Exception:
        pass

    class FootprintMetaclass(models.base.ModelBase):
        """Create a metaclass that overrides the name of the class it creates based on the given table name"""
        def __new__(cls, name, bases, attrs):

            # Register any additional model fields specified in fields
            def add_field(sender, **kwargs):
                if sender.__name__ == computed_name:
                    for field_name, field in fields.items():
                        field.contribute_to_class(sender, field_name)
            class_prepared.connect(add_field)
            return models.base.ModelBase.__new__(
                cls,
                computed_name,
                (abstract_class,),
                # Merge the manager objects (if the abstract_class has one) with attrs and class_attrs
                merge(dict(objects=abstract_class.objects.__class__()) if hasattr(abstract_class, 'objects') else {},
                      attrs,
                      class_attrs))
    # This generic class definition uses the above metaclass to give it the class name given by GenericModelClass+customTableName and the parent class abstractClass
    # More importantly, it defines its db_table as customTableName as well.
    class GenericModelClass(object):
        __metaclass__ = FootprintMetaclass

        objects = GeoInheritanceManager()

        class Meta:
            # Set the table name
            db_table = '"{0}"."{1}"'.format(schema, table)
            app_label = 'footprint'

    return GenericModelClass

def get_dynamic_resource_class(super_class, model_class, **fields):
    """
        Subclass the super_class and change the queryset to the model_class's and abstract to False
    :param super_class: The Resource class to subclass
    :param model_class: The concrete subclassed model class which we want the subclassed Resource class to query
    :param fields:
    :return:
    """
    return ModelDeclarativeMetaclass(
        get_dynamic_resource_class_name(super_class, model_class),
        (super_class,),
        merge(
            fields,
            dict(
                Meta=type('Meta',(super_class.Meta,),dict(
                    queryset = model_class.objects.all(),
                    abstract = False
        )))
    ))

# From http://dynamic-models.readthedocs.org/en/latest/topics/database-migration.html#topics-database-migration
def create_table_for_dynamic_class(model_class):

    fields = [(f.name, f) for f in model_class._meta.local_fields]
    table_name = model_class._meta.db_table
    db.create_table(table_name, fields)

    # some fields (eg GeoDjango) require additional SQL to be executed
    # Because of the poor Django/GeoDjango support for schemas, we have to manipulate the GeoDjango sql here so that the table is resolved to the correct schema, sigh
    if len(table_name.split('.'))==2:
        schema, table = parse_schema_and_table(table_name)
        for i, sql in enumerate(db.deferred_sql):
            # Replace the POSTGIS single argument with two arguments
            # TODO this stupidly assumes that all deferred sql is POSTGIS
            # Substitution for '"schema"."table"' to 'schema','table'. This is for AddGeometryColumn
            db.deferred_sql[i] = re.sub("'{0}'".format(table_name), "'{0}','{1}'".format(schema, table), sql)
            # Substitution for "schema"."table" to schema.table. This is for CREATE INDEX
            db.deferred_sql[i] = re.sub("{0}".format(table_name), "{0}.{1}".format(schema, table), db.deferred_sql[i])
            # Substitution for "schema"."tableHEX". Some indexes add random hex to the table name inside the double quotes. They may also truncate the table name, so just capture everything between "s
            # Also truncate to 64 characters the schema name minus the length of the table name, favoring the end of the schema which is most unique
            db.deferred_sql[i] = re.sub(r'"(".*)"\."(.*") ON', r'\1.\2 ON'.format(schema, table), db.deferred_sql[i])
            if string.find(db.deferred_sql[i], 'CREATE INDEX') == 0:
                subs = db.deferred_sql[i]
                # Truncate the index name. This could be done more elegantly
                db.deferred_sql[i] = subs[0:14] + subs[14:string.index(subs, '" ON')][-64:] + subs[string.index(subs, '" ON'):]

    db.execute_deferred_sql()

def drop_table_for_dynamic_class(model_class):
    table_name = model_class._meta.db_table
    db.delete_table(table_name)

def get_dynamic_resource_class_name(super_class, model_class):
    # Form the name from the model class's name schema portion
    return "{0}{1}".format(model_class.__name__, super_class.__name__)

def get_dynamic_model_class_name(abstract_class, scope_id):
    """
        Returns the naming used for a dynamic model class, which is always based on the table name
    :param abstract_class: The table name in the form "'schema'.'table'"
    :param scope_id: The id of the scope of the dynamic subclass, such as a ConfigEntity id
    :return:
    """
    return "{0}{1}".format(abstract_class.__name__, scope_id)


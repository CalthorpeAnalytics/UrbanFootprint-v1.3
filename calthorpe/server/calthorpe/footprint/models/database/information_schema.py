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

from footprint.managers.database.managers import InformationSchemaManager, PGNamespaceManager
from django.db import models
from footprint.lib.functions import merge
from uf_tools import executeSQL_now

__author__ = 'calthorpe'

class InformationSchema(models.Model):

    table_catalog = models.CharField(max_length = 100)
    table_schema = models.CharField(max_length = 100)
    table_name = models.CharField(max_length = 100)
    # Pretend this is the primary key since the table doesn't have a single column primary key
    column_name = models.CharField(max_length = 100, null=False, primary_key=True)
    data_type = models.CharField(max_length = 100)
    udt_name =  models.CharField(max_length = 100, null=False, primary_key=True)

    objects = InformationSchemaManager()

    def __unicode__(self):
        return "Catalog: {0}, Schema: {1}, Table: {2}, Column: {3}, Type: {4}".format(self.table_catalog, self.table_schema, self.table_name, self.column_name, self.data_type)

    def full_table_name(self):
        return "{0}.{1}".format(self.table_schema, self.table_name)

    class Meta(object):
        db_table = '"information_schema"."columns"'

class PGNamespace(models.Model):
    """
     This class is just needed to list schemas and see if they exist if they have no tables
    """
    # Pretend this is the primary key since the table doesn't have a single column primary key
    nspname = models.CharField(max_length = 100, null=False, primary_key=True)
    objects = PGNamespaceManager()

    class Meta(object):
        db_table = 'pg_namespace'


class SouthMigrationHistory(models.Model):
    """
     This class is just needed to list schemas and see if they exist if they have no tables
    """
    # Pretend this is the primary key since the table doesn't have a single column primary key
    id = models.IntegerField(null=False, primary_key=True)
    app_name = models.CharField(max_length=100)
    migration = models.CharField(max_length=100)
    applied = models.DateTimeField()

    class Meta(object):
        db_table = 'south_migrationhistory'


class GeometryColumns(models.Model):

    f_table_catalog = models.CharField(max_length = 256, null=False)
    f_table_schema = models.CharField(max_length = 256, null=False, primary_key=True)
    f_table_name = models.CharField(max_length = 256, null=False, primary_key=True)
    f_geometry_column = models.CharField(max_length = 256, null=False, primary_key=True)
    coord_dimension = models.IntegerField(null=False)
    srid = models.IntegerField(null=False)
    type = models.CharField(max_length = 30, null=False)

    class Meta(object):
        db_table = 'geometry_columns'

def register_geometry_columns(server, schema=None):
    tables_with_geometry = InformationSchema.objects.tables_with_geometry(schema=schema)
    for information_scheme in tables_with_geometry:

        sql =  "select ST_CoordDim({2}), ST_SRID({2}), ST_GeometryType({2}) from {1}.{0}".format(information_scheme.table_name, information_scheme.table_schema, information_scheme.column_name)
        ret = executeSQL_now(None, [sql])[0]
        if len(ret)>0:
            coord, srid, geom_type = ret[0]
        else:
            coord, srid, geom_type = (2, 4326, 'GEOMETRY')
        GeometryColumns.objects.get_or_create(
            **merge(dict(
                f_table_name = information_scheme.table_name,
                f_geometry_column = information_scheme.column_name,
                f_table_schema=information_scheme.table_schema),
                dict(defaults=dict(
                    # f_table_catalog=information_scheme.table_catalog,
                    coord_dimension=coord,
                    srid=srid,
                    type=geom_type
                ))))
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
from django.db import models, transaction
from django.db import connection
from footprint.lib.functions import merge

__author__ = 'calthorpe'

class InformationSchemaManager(models.Manager):
    def tables_of_schema(self, schema, **kwargs):
        return self.values('table_name').annotate().filter(table_schema=schema, **kwargs)

    def tables_of_schema_with_column(self, schema, column):
        return self.values('table_name').annotate().filter(table_schema=schema, column_name=column)

    def columns_of_table(self, schema, table):
        return self.filter(table_schema=schema, table_name=table)

    def table_exists(self, schema, table):
        return len(self.filter(table_schema=schema, table_name=table)) > 0

    def tables_with_geometry(self, schema=None):
        return self.filter(**merge(dict(udt_name='geometry'), dict(schema=schema) if schema else {}))

class PGNamespaceManager(models.Manager):
    def schema_exists(self, schema):
        return len(self.filter(nspname=schema)) > 0

    def create_schema(self, schema, connection=connection):
        if not self.schema_exists(schema):
            cursor = connection.cursor()
            cursor.execute('create schema {0}'.format(schema))
            transaction.commit_unless_managed()

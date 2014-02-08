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
from django.db import models, transaction
from django.db import connection
import psycopg2
from footprint import settings
from footprint.common.utils.postgres_utils import build_postgres_conn_string, pg_connection_parameters
from footprint.main.lib.functions import merge, compact_dict

logger = logging.getLogger(__name__)

__author__ = 'calthorpe_associates'

class InformationSchemaManager(models.Manager):
    def tables_of_schema(self, schema, **kwargs):
        return self.values('table_name').annotate().filter(table_schema=schema, **kwargs)

    def tables_of_schema_with_column(self, schema, column):
        return self.values('table_name').annotate().filter(table_schema=schema, column_name=column)

    def columns_of_table(self, schema, table, column_name=None):
        """
            Returns the columns matching the given schema, table, and column_name
        :param schema:
        :param table:
        :param column_name: Optionally limit the result to a single value
        :return: The matching InformationSchema instances
        """
        return self.filter(**compact_dict(dict(table_schema=schema, table_name=table, column_name=column_name)))

    def has_column(self, schema, table, column_name):
        """
            Returns true if the give column exists for the given schema and table, otherwise false
        :param schema:
        :param table:
        :param column_name:
        :return:
        """
        return len(self.columns_of_table(schema, table, column_name)) == 1

    def table_exists(self, schema, table):
        return len(self.filter(table_schema=schema, table_name=table)) > 0

    def tables_with_geometry(self, schema=None, table=None):
        """
            Returns tables with a column data type of 'geometry'
        :param schema: Optional schema to search
        :param table: Optional table to which to limit search. This guarantees 0 or 1 result
        :return:
        """
        return self.filter(**merge(dict(udt_name='geometry'),
                                   compact_dict(dict(table_schema=schema, table_name=table))))

class PGNamespaceManager(models.Manager):
    def schema_exists(self, schema):
        return len(self.filter(nspname=schema)) > 0

    def create_schema(self, schema, connection=connection):
        if not self.schema_exists(schema):
            logger.debug("Creating schema %s" % schema)


            conn = psycopg2.connect(**pg_connection_parameters(settings.DATABASES['default']))
            conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = connection.cursor()
            cursor.execute('create schema {0}'.format(schema))
            logger.debug("Schema %s created" % schema)

    def drop_schema(self, schema, connection=connection):
        if self.schema_exists(schema):
            logger.debug("Dropping schema %s" % schema)

            conn = psycopg2.connect(**pg_connection_parameters(settings.DATABASES['default']))
            conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = connection.cursor()
            cursor.execute('drop schema {0} cascade'.format(schema))
            logger.debug("Schema %s dropped" % schema)

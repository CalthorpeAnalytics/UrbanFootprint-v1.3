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

import datetime
import logging
from os import path
import re
import stat
import os
from celery.utils.functional import uniq
from django.db import connections, connection, transaction

import psycopg2
from django.conf import settings
from footprint.common.utils.postgres_utils import pg_connection_parameters, build_postgres_conn_string

from footprint.main.lib.functions import if_cond_raise, map_dict, filter_dict
from footprint.main.models.database.information_schema import InformationSchema, sync_geometry_columns, verify_srid

# from calthorpe.main.publishing.geoserver import validate_geoserver_configuration
from footprint.main.utils.uf_toolbox import drop_table
from footprint.main.utils.utils import database_settings, execute_piped_with_stdin, execute_with_stdin, chop_geom, postgres_url_to_connection_dict, file_url_to_path, os_user
from django.conf import settings

GEOMETRY_COLUMN = 'wkb_geometry'

logger = logging.getLogger(__name__)

# See Footprimporter manager command for options
class ImportData(object):

    def create_target_db_string(self):
        self.target_database_connection = "-h {0} -p {1} --user {2} {3}".format(
            self.target_database['HOST'],
            self.target_database['PORT'] or 5432,
            self.target_database['USER'],
            self.target_database['NAME'])
        logger.info("Using target database connection: {0}".format(self.target_database_connection))

    def __init__(self, **arguments):

        self.arguments = arguments
        self.dump_only = self.arguments.get('dump_only', None)
        self.region_key = self.arguments.get('schema', None)
        self.target_database = database_settings('default')
        # The config_entity whose feature tables should be imported
        self.config_entity = self.arguments.get('config_entity', None)
        if self.config_entity:
            logger.info("Importing config_entity {0}".format(self.config_entity))
        # The optional db_entity_key whose Feature class table should be imported. Otherwise all DbEntity tables
        # are imported for the config_entity, including inherited ones from parent ConfigEntities
        self.db_entity_key = self.arguments.get('db_entity_key', None)
        self.db_entities = filter(lambda db_entity: not self.db_entity_key or (db_entity.key == self.db_entity_key),
                                  self.config_entity.owned_db_entities())
        self.test = self.arguments.get('test', None)

        # The psql connection to the target server, normally the django server
        self.create_target_db_string()

        self.command_execution = CommandExecution(logger)

        self.connections = ["{host}:*:*:{user}:{password}".format(**dict(
                    host=self.target_database['HOST'],
                    user=self.target_database['USER'],
                    password=self.target_database['PASSWORD']))]

        for db_entity in self.db_entities:
            # Create a password file in order to avoid dealing with stdin for passwords
            # This has been bypassed in favor of passing the password to stdin
            if not (db_entity.has_db_url or db_entity.has_file_url):
                raise Exception("This db_entity, {0}, has no database or file url".format(db_entity.key))
            if db_entity.has_db_url:
                # Setup the connection strings for the db_entity so that we can get around interactive password authentication
                # TODO someone should clean this up to do it a better way
                connection_dict = postgres_url_to_connection_dict(db_entity.url)
                self.connections.append("{host}:*:*:{user}:{password}".format(**connection_dict))

    def run(self):
        """
            Imports the data and syncs dependent system components, such as GeoServer to the imported data.
        """

        self.passwordfile = path.join('/tmp/pgpassword_%s' % os_user())
        f = open(self.passwordfile, 'w')
        for connection in uniq(self.connections):
            f.write("{0}\n".format(connection))
        os.fchmod(f.fileno(), stat.S_IRUSR | stat.S_IWUSR)

        f.close()
        # Set the ENV variable to use this file
        os.environ['PGPASSFILE'] = self.passwordfile
        logger.info("Created password file at %s" % self.passwordfile)

        logger.info("Importing data")
        self.import_data()

        os.remove(self.passwordfile)
        del os.environ['PGPASSFILE']

    def import_data(self, **kwargs):
        """
            Imports data from an external source to create the test data
            :return a two item tuple containing the region that was imported and a list of the imported projects
        """

        # Calculate a sample lat/lon box of the config_entity
        config_entity = self.config_entity
        if self.test:
            bounds = chop_geom(config_entity.bounds, 0.90)
            logger.info(u"Creating subselection with extents: {0}. This will be used to crop any table that doesn't have a sample version".format(bounds))

        for db_entity in self.db_entities:

            if db_entity.has_file_url:
                # Remove the temp public table from public if exists from a prior run
                if re.match('file://(?P<path>.+)/(?P<filename>.+).shp', db_entity.url):
                    drop_table(re.match('file://(?P<path>.+)/(?P<filename>.+).shp', db_entity.url).groupdict()['filename'])
                shape_file_path = file_url_to_path(db_entity.url)
                # Create a command that pipes shp2pgsql to psql
                logger.debug("verifying SRID {0}".format(db_entity.srid))
                srid = verify_srid(db_entity.srid)
                shp_to_psql_command = '/usr/lib/postgresql/9.1/bin/shp2pgsql -s {srid} -g wkb_geometry -I {shapefile_path}'.format(
                    shapefile_path=shape_file_path, srid=srid.srid) + ' | /usr/bin/psql {0} -q'.format(self.target_database_connection)
                results = self.command_execution.run(shp_to_psql_command,
                                                     pipe_commands=False,
                                                     stdin="{0}\n{1}".format(self.arguments.get('password', None), self.target_database.get('PASSWORD', None)))

                generated_name = os.path.splitext(os.path.basename(shape_file_path))[0]
                move_to_schema = "alter table public.{1} set schema {0};".format(db_entity.schema, generated_name)
                rename = "alter table {0}.{1} rename to {2};".format(db_entity.schema, generated_name, db_entity.key)
                spatial_index = '''create index {0}_{1}_geom_idx on {0}.{1} using GIST (wkb_geometry);'''.format(db_entity.schema, db_entity.key)
                drop_constraint = '''alter table {0}.{1} drop constraint enforce_srid_wkb_geometry'''.format(db_entity.schema, db_entity.key)
                reproject = '''update {0}.{1} set wkb_geometry = st_SetSRID(st_transform(wkb_geometry, 4326),4326)'''.format(db_entity.schema, db_entity.key)

                conn = psycopg2.connect(**pg_connection_parameters(settings.DATABASES['default']))
                conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
                cursor = conn.cursor()
                logger.debug("Moving import shapefile table to schema: %s" % move_to_schema)
                cursor.execute(move_to_schema)
                logger.debug("Renaming shapefile table: %s" % rename)
                cursor.execute(rename)
                cursor.execute(spatial_index)
                cursor.execute(drop_constraint)
                cursor.execute(reproject)

                # Remove the temp public table from public if exists after the run
                drop_table(re.match('file://(?P<path>.+)/(?P<filename>.+).shp', db_entity.url).groupdict()['filename'])
            elif db_entity.has_db_url:
                # For now we only import data for DbEntity instances with a configured database url
                connection_dict = postgres_url_to_connection_dict(db_entity.url)
                # The import database currently stores tables as public.[config_entity.key]_[feature_class._meta.db_table (with schema removed)][_sample (for samples)]
                # We always use the table name without the word sample for the target table name
                source_table = "{0}_{1}_{2}".format(config_entity.key, db_entity.table, 'sample') if settings.USE_SAMPLE_DATA_SETS or self.test else "{0}_{1}".format(config_entity.key, db_entity.table)
                table = db_entity.table
                self._dump_tables_to_target('-t %s' % source_table, source_schema='public', target_schema=db_entity.schema, source_table=source_table, target_table=table, connection_dict=connection_dict)

            if db_entity.has_file_url or db_entity.has_db_url:
                conn = psycopg2.connect(**pg_connection_parameters(settings.DATABASES['default']))
                conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
                cursor = conn.cursor()
                transform_to_4326 = '''update "{schema}"."{table}"
                set wkb_geometry = st_setSRID(st_transform(wkb_geometry, 4326), 4326);'''.format
                cursor.execute(transform_to_4326(schema=db_entity.schema, table=db_entity.table))
                # If we imported the table successfully
                if InformationSchema.objects.table_exists(db_entity.schema, db_entity.table):
                    # Tell PostGIS about the new geometry column or the table
                    sync_geometry_columns(db_entity.schema, db_entity.table)

    def _dump_tables_to_target(self, table_selector, source_schema=None, target_schema=None, source_table=None, target_table=None, connection_dict=None, predicate_table_fetcher=lambda: []):
        """
            Dumps the table indicated by the table_selector string to the target_schema on the target database. Throws an exception if the target already exists
        :param table_selector: A string used in pg_dump to specify the table, such as '-t TABLE_NAME'. Optional attributes like --schema-only may be included
        :param source_schema: The optional source_schema to use when specifying a target_schema. Both can be left null or both most be used.
        :param target_schema: The optional target schema on the target database whither to write the table. If None the schema is that of the source
        :param source_table optional table name to use when specifying a target_table. Both can be left null or both most be used.
        :param target_table optional table name to write the table. If None the table is that of the host
        :param connection_dict: The optional database configuration. A dict of user, password, host, port, and database. Defaults to self.pg_dump_connection
        :param predicate_table_fetcher: A lambda that returns multiple results to indicate the target already exists, and an exception should be raised.
        :return: True if the table was created.
        """
        def sed_format(str, required_variables, **kwargs):
            str = str.replace(' ', '\ ')
            str = "sed " + str
            return str.format(source_table=source_table,
                              source_schema=source_schema,
                              target_table=target_table,
                              target_schema=target_schema) if all(required_variables) else None

        # We optionally use sed to change the name of the schema and or table
        sed_table = sed_format('s/{source_table}/{target_table}/g', [source_table, target_table])
        # We include the table here so public is only changed where associated with the table
        sed_schema = sed_format('s/{source_schema}\.{target_table}/{target_schema}\.{target_table}/g', [source_schema, target_schema])
        # Also add the schema to the create table statement
        sed_schema_table_create = sed_format("s/CREATE TABLE {target_table}/CREATE TABLE {target_schema}.{target_table}/g", [source_schema, target_schema])
        sed_schema_table_copy = sed_format("s/COPY {target_table}/COPY {target_schema}.{target_table}/g", [source_schema, target_schema])
        sed_schema_table_alter = sed_format("s/ALTER TABLE ONLY {target_table}/ALTER TABLE ONLY {target_schema}.{target_table}/g", [source_schema, target_schema])

        pg_dump_connection = "--host={host} --port={port} --user={user} {database}".format(**connection_dict)
        dump_to_psql_command = ' | '.join(filter(lambda str: str, [
            '/usr/bin/pg_dump {0} {1}'.format(pg_dump_connection, table_selector),
            sed_table,
            sed_schema,
            sed_schema_table_create,
            sed_schema_table_copy,
            sed_schema_table_alter,
            '/usr/bin/psql {0}'.format(self.target_database_connection)
        ]))
        target_table_already_exists = len(predicate_table_fetcher()) > 0
        results = self.command_execution.run(dump_to_psql_command,
            predicate=lambda: not target_table_already_exists,
            validator=Validator(
                predicate_table_fetcher(),
                lambda results: len(results) > 0,
                lambda results: Exception('{0} tables already exist: {1}'.format(
                    len(results),
                    map(lambda result: result.table_name, results)))),
            stdin="{0}\n{1}".format(self.arguments.get('password', None), self.target_database.get('PASSWORD', None))
        )
        return not target_table_already_exists

class CommandExecution:

    def __init__(self, logger):
        logger = logger

    def _exec_piped(self, commands, stdin):
        logger.info("Running %s", ' | ' .join(map(lambda command: ' '.join(command), commands)))
        out_and_err_tuple = execute_piped_with_stdin(commands, stdin)
        if out_and_err_tuple[0]:
            logger.info(out_and_err_tuple[0])
        if out_and_err_tuple[1]:
            logger.warn(out_and_err_tuple[1])
        return out_and_err_tuple

    def _exec(self, command, stdin):
        logger.info("Running %s" % command)
        out_and_err_tuple = execute_with_stdin(command, stdin)
        # Just log errors, since the output seems to include the output of the piped command too
        if out_and_err_tuple.stdout:
            logger.info(out_and_err_tuple.stdout.bytes)
        if out_and_err_tuple.stderr:
            logger.warn(out_and_err_tuple.stderr.bytes)
        return out_and_err_tuple

    def run(self, commands, **kwargs):
        predicate = kwargs.get('predicate', lambda: True)
        validator = kwargs.get('validator', None)
        stdin = kwargs.get('stdin', None)
        pipe_commands = kwargs.get('pipe_commands',  False)
        if predicate():
            if validator:
                validator()
            if pipe_commands:
                return self._exec_piped(commands, stdin)
            else:
                return self._exec(commands, stdin)
        else:
            if pipe_commands:
                logger.info("Not Run: ")
                logger.info(' | ' .join(map(lambda command: ' '.join(command), commands)))
            else:
                for command in commands:
                    logger.info("Not Run: %s", ' '.join(command))
            return None

class Validator:
    def __init__(self, value, predicate, exception):
        self.value = value
        self.predicate = predicate
        self.exception = exception

    def __call__(self):
        if_cond_raise(self.value, self.predicate, self.exception)


def formatted_timestamp():
    return datetime.datetime.now().strftime("%d%b%Y%H%M%S%f")


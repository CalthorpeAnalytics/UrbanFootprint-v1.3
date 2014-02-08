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
import stat
import os

import psycopg2
from django.conf import settings

from footprint.lib.functions import if_cond_raise, map_dict, filter_dict
from footprint.models.database.information_schema import InformationSchema

# from footprint.publishing.geoserver import validate_geoserver_configuration
from footprint.utils.utils import database_settings, execute_piped_with_stdin, execute_with_stdin, chop_geom

GEOMETRY_COLUMN = 'wkb_geometry'

# See Footprimporter manager command for options
class ImportData(object):

    logger = None

    def __init__(self, **arguments):
        if not self.__class__.logger:
            self.init_logger()

        self.arguments = arguments
        self.dump_only = self.arguments.get('dump_only', None)
        self.region_key = self.arguments.get('schema', None)
        self.target_database = database_settings('default')
        # The config_entity whose feature tables should be imported
        self.config_entity = self.arguments.get('config_entity', None)
        if self.config_entity:
            self.__class__.logger.info("Importing config_entity {0}".format(self.config_entity))
        # The optional db_entity_key whose Feature class table should be imported. Otherwise all DbEntity tables
        # are imported for the config_entity, including inherited ones from parent ConfigEntities
        self.db_entity_key = self.arguments.get('db_entity_key', None)
        self.db_entities = map(lambda db_entity_setup: db_entity_setup['db_entity'],
                                   filter(lambda db_entity_setup:
                                       not self.db_entity_key or (db_entity_setup['key'] == self.db_entity_key),
                                       self.config_entity.accumulated_default_db_entities_and_classes()))

        self.test = self.arguments.get('test', None)
        source_database = database_settings(self.arguments['db']) if self.arguments.get('db', None) else None
        if source_database:
            # TODO overriding host for unit tests
            host = source_database['HOST']
            port = source_database['PORT'] or 5432
            user = source_database['USER']
            password = source_database['PASSWORD']
            # TODO overriding name for unit tests
            name = source_database['NAME'].replace('test_', '') # Make sure the real source database is used for unit tests
        else:
            host = self.arguments.get('host', None)
            port = self.arguments.get('port', None) or 5432
            user = self.arguments.get('user', None)
            password = self.arguments.get('password', None)
            name = self.arguments.get('database', None)

        # The pg_dump connection string to the source server
        self.pg_dump_connection = "--host={0} --port={1} --user={2} {3}".format(
            host,
            port,
            user,
            name
        )
        self.__class__.logger.info("Using source pg_dump connection: %s", self.pg_dump_connection)

        self.source_connect_string =  'host={0} port={1} user={2} dbname={3} password={4}'.format(
            host,
            port,
            user,
            name,
            password
        )
        self.__class__.logger.info("Using source connect string: %s", self.pg_dump_connection)

        # The db_link connection string to the source server
        self.db_link_connection = "hostaddr={0} port={1} user={2} dbname={3} password={4}".format(
            host,
            port,
            user,
            name,
            password
        )
        self.__class__.logger.info("Using source db_link database connection: %s", self.db_link_connection)

        # The psql connection to the target server, normally the django server
        self.target_database_connection = "-h {0} -p {1} --user {2} {3}".format(
            self.target_database['HOST'],
            self.target_database['PORT'] or 5432,
            self.target_database['USER'],
            self.target_database['NAME'])
        self.__class__.logger.info("Using target database connection: %s", self.target_database_connection)

        self.target_connect_string =  'host={0} port={1} user={2} dbname={3} password={4}'.format(
            self.target_database['HOST'],
            self.target_database['PORT'] or 5432,
            self.target_database['USER'],
            self.target_database['NAME'],
            self.target_database['PASSWORD']
        )
        self.__class__.logger.info("Using target connect string: %s", self.target_database_connection)

        self.command_execution = CommandExecution(self.__class__.logger)

        # Create a password file in order to avoid dealing with stdin for passwords
        # This has been bypassed in favor of passing the password to stdin
        source_database_password = "{0}:*:*:{1}:{2}".format(
            host,
            user,
            password)
        target_database_password =  "{0}:*:*:{1}:{2}".format(
            self.target_database['HOST'],
            self.target_database['USER'],
            self.target_database['PASSWORD'])
        self.passwordfile = path.join(settings.ROOT_PATH, 'pgpassword')
        f=open(self.passwordfile, 'w')
        f.write("{0}\n{1}\n".format(source_database_password, target_database_password))
        os.fchmod(f.fileno(), stat.S_IRUSR | stat.S_IWUSR)
        f.close()
        os.environ['PGPASSFILE'] = self.passwordfile
        self.__class__.logger.info("Created password file at %s", self.passwordfile)

    @classmethod
    def init_logger(cls):
        cls.logger = logging.getLogger(__name__)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        fileHandler = logging.FileHandler('/var/tmp/{0}.log'.format(__name__))
        streamHandler = logging.StreamHandler()
        fileHandler.setFormatter(formatter)
        streamHandler.setFormatter(formatter)
        cls.logger.addHandler(fileHandler)
        cls.logger.addHandler(streamHandler)
        cls.logger.setLevel(logging.INFO)

    def run(self):
        """
            Imports the data and syncs dependent system components, such as GeoServer to the imported data.
        """

        self.__class__.logger.info("Importing data")
        self.import_data()

        os.remove(self.passwordfile)
        del os.environ['PGPASSFILE']


    def import_data(self):
        """
            Imports data from an external source to create the test data
            :return a two item tuple containing the region that was imported and a list of the imported projects
        """

        # Calculate a sample lat/lon box of the config_entity
        config_entity = self.config_entity
        if self.test:
            bounds = chop_geom(config_entity.bounds, 0.90)
            self.__class__.logger.info(u"Creating subselection with extents: {0}. This will be used to crop any table that doesn't have a sample version".format(bounds))

        for db_entity in self.db_entities:
            # The import database currently stores tables as public.[config_entity.key]_[feature_class._meta.db_table (with schema removed)][_sample (for samples)]
            if settings.USE_SAMPLE_DATA_SETS or self.test:
                table = "{0}_{1}_{2}".format(config_entity.key, db_entity.table, 'sample')
            else:
                table = "{0}_{1}".format(config_entity.key, db_entity.table)
            self._dump_tables_to_target('-t %s' % table)

    def _copy_geometry_table_rows(self, information_schema_table, target_schema, geom_bounds, geom_join_table=None, geom_join_column=None):
        """
        Copy the table from the source to the destination, creating the table definition and then copying
        the rows within the lat_range and lon_range
        """

        if self._source_table_exists(information_schema_table):
            # TODO Replace this lookup with a lookup for the geometry_columns table
            column_srid = self._source_query("select ST_SRID({0}) from {1} limit 1".format(
                GEOMETRY_COLUMN,
                information_schema_table.full_table_name() if not geom_join_table else geom_join_table))[0][0]
            # This smashes the polygons of the bounds into a text expression to recreate the object in PostGIS. There should be some way to move between GeoJango and PostGIS objects but it's not obvious
            geom_sql = "'MULTIPOLYGON(({0}))'".format(
                ','.join(map(lambda polygon:
                ','.join(
                    map(lambda linear_ring:
                        '({0})'.format(
                            ','.join(map(lambda point: "{0} {1}".format(*point),
                                    linear_ring))),
                        polygon)),
                    geom_bounds)))
            create_bounds = "ST_MPolyFromText({0}, {1})".format(geom_sql, settings.DEFAULT_SRID)
            query_filter = 'ST_Contains({0}, ST_Transform({1}, {2}))'.format(create_bounds, GEOMETRY_COLUMN, settings.DEFAULT_SRID)
            # Copy the rows from the source database only if the table is nonexistant on the target
            self._copy_rows_from_source_database(
                information_schema_table,
                target_schema=target_schema,
                query_filter=query_filter,
                proceed_if_table_empty=True,
                geom_join_table=geom_join_table,
                geom_join_column=geom_join_column)
                #raise_on_exists=lambda: Exception("The table {0} already exists and is not empty. Delete from the target database prior to running the import".format(information_schema_table.full_table_name())))
        else:
            self.__class__.logger.warn("Expected source table %s was not found. Skipping import of this table", information_schema_table.full_table_name())

    def _copy_rows_from_source_database(self, information_schema_table, **kwargs):

        """
            Copies rows from the source database to the target. The table is created if it doesn't exist on the target.
            The copy aborts without an error if the table already exists, unless option proceed_if_table_exists is True.

            information_schema_table is an InformationSchema to indicate the table
            Optional args:
                target_schema - the schema to which to copy the table on the target database. It must already exist. Defaults to the schema of the source database table
                query_filter - sql that is used for the where clause of the source table row selection
                table_counter_lambda - a lambda that returns the InformationSchema objects for each table that matches the the target table. If this returns more than zero results, the table is considered to already exist on the target. By default this lambda is composed to select the InformationSchema objects based on the given information_schema_table
                proceed_if_table_exists - insert rows regardless of the whether the target table already exists or not. This is useful when rows are being added to a table that may or may not exist. Only rows with ids that don't exist on the target will be inserted, rows that do exist will be update to reflect the source row.
                proceed_if_table_empty - insert rows as long as the table is empty, even if it already existed.
                raise_on_exists - a lambda that returns an exception to raise if the table already exists. This will not be called if proceed_if_table_exists is True or proceed_if_table_empty is True and the table is in fact empty. By default no exception is raised.
                geom_join_table is an optional fully qualified table named used to join the main table to a geometry column in the geom_join_table using the specified geom_join_column, which is expected to be the matching column name of both tables
                geom_join_column is an optional column name used with geom_join_table
        """
        if self.dump_only :
            raise Exception("Attempting select rows from the source database when dump_only is true")

        query_filter = kwargs.get('query_filter', None)
        target_schema = kwargs.get('target_schema', information_schema_table.table_schema)
        table_counter_lambda = kwargs.get('table_counter_lambda',
            lambda: InformationSchema.objects.tables_of_schema(target_schema, table_name=information_schema_table.table_name)
        )
        proceed_if_table_exists = kwargs.get('proceed_if_table_exists', False)
        proceed_if_table_empty = kwargs.get('proceed_if_table_empty', False)
        raise_on_exists = kwargs.get('raise_on_exists', None)
        geom_join_table = kwargs.get('geom_join_table', None)
        geom_join_column = kwargs.get('geom_join_column', None)

        target_table_created = len(InformationSchema.objects.tables_of_schema(information_schema_table.table_schema, table_name=information_schema_table.table_name)) == 0
        self._dump_tables_to_target(
            '--schema-only -t {0}'.format(information_schema_table.full_table_name()),
            information_schema_table.table_schema,
            target_schema,
            table_counter_lambda)
        self.__class__.logger.info("Target table %s created", "was" if target_table_created else "was not")

        may_proceed_if_exists = proceed_if_table_exists or (
            proceed_if_table_empty and
            (target_table_created or len(self._target_query('select * from {0}.{1} limit 1'.format(target_schema, information_schema_table.table_name))) == 0))

        if may_proceed_if_exists or target_table_created:
            column_info_schemas = InformationSchema.objects.columns_of_table(target_schema, information_schema_table.table_name)

            # Some columns nonsensically have " " in their names which breaks the insert/update queries.
            corrector = {
                'ResEnrgyNewConst':'"ResEnrgyNewConst"',
                'ResEnrgyRetro':'"ResEnrgyRetro"',
                'ResEnrgyReplcmt':'"ResEnrgyReplcmt"',
                'ComEnrgyNewConst':'"ComEnrgyNewConst"',
                'ComEnrgyRetro':'"ComEnrgyRetro"',
                'ComEnrgyReplcmt':'"ComEnrgyReplcmt"',
                'ResWatrNewConst':'"ResWatrNewConst"',
                'ResWatrRetro':'"ResWatrRetro"',
                'ResWatrReplcmt':'"ResWatrReplcmt"',
                'ComIndWatrNewConst':'"ComIndWatrNewConst"',
                'ComIndWatrRetro':'"ComIndWatrRetro"',
                'ComIndWatrReplcmt':'"ComIndWatrReplcmt"',
                'Water_GPCD_SF':'"Water_GPCD_SF"',
                'Water_GPCD_MF':'"Water_GPCD_MF"',
                'Water_GPED_Retail':'"Water_GPED_Retail"',
                'Water_GPED_Office':'"Water_GPED_Office"',
                'Water_GPED_Industrial':'"Water_GPED_Industrial"',
                'Water_GPED_School': '"Water_GPED_School"'}

            # Determine the primary key of the table
            try:
                id_column = self._source_query("SELECT pg_attribute.attname FROM pg_class, pg_attribute, pg_index WHERE pg_class.oid = pg_attribute.attrelid AND pg_class.oid = pg_index.indrelid AND pg_index.indkey[0] = pg_attribute.attnum AND pg_index.indisprimary = 't' AND pg_class.relname='{0}'".format(information_schema_table.table_name))[0][0]
            except:
                id_column = geom_join_column
                if not id_column:
                    raise Exception("Table has no primary key and no geom_join_column is defined")

            columns = map(lambda x: corrector.get(x.column_name, x.column_name), column_info_schemas)
            columns_string = ','.join(columns)
#            columns_with_type = ','.join(map(
#                lambda x: "{0} {1}".format(corrector.get(x.column_name, x.column_name), 'geometry' if x.data_type == 'USER-DEFINED' else x.data_type),
#                column_info_schemas))

            where_clause = 'where {0}'.format(query_filter) if query_filter else ''
#            db_link = "dblink('{0}', 'select {1} from {2} {3}') as t1({4})".format(
#                self.db_link_connection,
#                columns,
#                information_schema_table.full_table_name(),
#                where_clause,
#                columns_with_type)
            # Create a tmp table on the source with rows limited by geometry
            # It can't use the 'temp' keyword since it needs to survive the session to be used by pg_dump. We'll delete it after
            # postgres limits the table name length to 63 characters
            tmp_table_prefix = "{0}_{1}".format(information_schema_table.table_schema, information_schema_table.table_name)[:55]
            tmp_table_name = "{0}_temp".format(tmp_table_prefix)
            join_geometry_table = 'join {0} geom_table on geom_table.{1} = main.{1}'.format(geom_join_table, geom_join_column) if geom_join_table else ''
            try:
                create_tmp_table = 'select {0} into table {1} from {2} main {3} {4}'.format(
                    ','.join(map(lambda column: "main.{0}".format(column), columns)),
                    tmp_table_name,
                    information_schema_table.full_table_name(),
                    join_geometry_table,
                    where_clause)
                # Delete the same named tmp table on the target and dump the source table
                self._target_database_drop_table(tmp_table_name)
                self._source_create(create_tmp_table)
                self._dump_tables_to_target('-t {0}'.format(tmp_table_name), None, None, lambda: [])
            finally:
                # Delete the 'tmp' table explicitly
                try:
                    self._source_drop_tmp_table(tmp_table_name)
                except:
                    pass

            if not target_table_created:
                # The target table exists. Update existing rows and insert new ones.
                # Retrieve the primary key column
                where_not_in_clause = "{0} not in (select {0} from {1})".format(
                    id_column,
                    information_schema_table.full_table_name())
                insert_sql = "insert into {0}.{1} ({2}) select * from {3} where {4}".format(
                    target_schema,
                    information_schema_table.table_name,
                    columns_string,
                    tmp_table_name,
                    #db_link,
                    where_not_in_clause)
                self._target_database_write(insert_sql)
                where_in_clause = "target.{0} in (select {0} from {1})".format(
                    id_column,
                    information_schema_table.full_table_name())
                column_setters = ','.join(map(lambda x: "{0}=t1.{0}".format(corrector.get(x.column_name, x.column_name)), filter(lambda x: x.column_name != id_column, column_info_schemas)))
                if len(column_info_schemas) > 1:
                    # Only update if there are more columns than just the primary key
                    update_sql = "update {0} as target set {1} from {2} t1 where target.{3}=t1.{3} and {4}".format(
                        information_schema_table.full_table_name(),
                        column_setters,
                        tmp_table_name,
                        #db_link,
                        id_column,
                        where_in_clause)
                    self._target_database_write(update_sql)
            else:
                # The target table is new. Insert rows
                sql = "insert into {0}.{1} ({2}) select * from {3}".format(
                    target_schema,
                    information_schema_table.table_name,
                    columns_string,
                    tmp_table_name)
                    #db_link)
                self._target_database_write(sql)
            self._target_database_drop_table(tmp_table_name)

        elif raise_on_exists:
            raise raise_on_exists()

        return target_table_created

    def _source_table_exists(self, information_schema_table):
        return len(self._source_query("select table_name from information_schema.columns where table_schema = '{0}' and table_name like '{1}' group by table_name".format(information_schema_table.table_schema, information_schema_table.table_name))) > 0

    def _source_query(self, sql):
        self.__class__.logger.info("Database query on source: %s", sql)
        db = psycopg2.connect(self.source_connect_string)
        cursor= db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def _source_create(self, sql):
        if (not 'create' in sql and not 'into' in sql):
            raise Exception("Only create statements allowed: {0}".format(sql))

        self.__class__.logger.info("Database create table on source: %s", sql)
        db = psycopg2.connect(self.source_connect_string)
        cursor= db.cursor()
        cursor.execute(sql)
        db.commit()

    def _source_drop_tmp_table(self, tmp_table):
        if (not 'temp' in tmp_table):
            raise Exception("Only tables with 'tmp' in their name may be dropped: {0}".format(tmp_table))
        sql = 'drop table {0}'.format(tmp_table)
        self.__class__.logger.info("Database dropping tmp table on source: %s", sql)
        db = psycopg2.connect(self.source_connect_string)
        cursor= db.cursor()
        cursor.execute(sql)
        db.commit()

    def _target_query(self, sql):
        self.__class__.logger.info("Database query on target: %s", sql)
        db = psycopg2.connect(self.target_connect_string)
        cursor= db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def _target_database_drop_table(self, table):
        sql =  'drop table if exists {0}'.format(table)
        self.__class__.logger.info("Database drop on target: %s", sql)
        db = psycopg2.connect(self.target_connect_string)
        cursor= db.cursor()
        cursor.execute(sql)
        db.commit()

    def _target_database_write(self, sql):
        self.__class__.logger.info("Database write to target: %s", sql)
        db = psycopg2.connect(self.target_connect_string)
        cursor= db.cursor()
        cursor.execute(sql)
        db.commit()


    def _dump_tables_to_target(self, table_selector, source_schema=None, target_schema=None, predicate_table_fetcher=lambda: []):
        """
            Dumps the table indicated by the table_selector string to the target_schema on the target database. Throws an exception if the target already exists
        :param table_selector: A string used in pg_dump to specify the table, such as '-t TABLE_NAME'. Optional attributes like --schema-only may be included
        :param source_schema: The optional source_schema to use when specifying a target_schema. Both can be left null or both most be used.
        :param target_schema: The optional target schema on the target database whither to write the table. If None the schema is that of the source
        :param predicate_table_fetcher: A lambda that returns multiple results to indicate the target already exists, and an exception should be raised.
        :return: True if the table was created.
        """

        # We optionally use sed to change the name of the schea if the source_schema and target_schema are specified, meaning they are different
        sed = ['sed s/{0}/{1}/g'.format(source_schema, target_schema).split(' ')] if source_schema and target_schema else []
        dump_to_psql_command = ['pg_dump {0} {1}'.format(self.pg_dump_connection, table_selector).split(' ')] + sed +\
                               ['psql {0}'.format(self.target_database_connection).split(' ')]
        target_table_already_exists = len(predicate_table_fetcher()) > 0
        self.command_execution.run(dump_to_psql_command,
            pipe_commands=True,
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
        self.__class__.logger = logger

    def _exec_piped(self, commands, stdin):
        self.__class__.logger.info("Running %s", ' | ' .join(map(lambda command: ' '.join(command), commands)))
        out_and_err_tuple = execute_piped_with_stdin(commands, stdin)
        if out_and_err_tuple[0]:
            self.__class__.logger.info(out_and_err_tuple[0])
        if out_and_err_tuple[1]:
            self.__class__.logger.warn(out_and_err_tuple[1])
        return out_and_err_tuple

    def _exec(self, command, stdin):
        self.__class__.logger.info("Running %s", ' '.join(command))
        out_and_err_tuple = execute_with_stdin(command, stdin)
        # Just log errors, since the output seems to include the output of the piped command too
        if out_and_err_tuple[0]:
            self.__class__.logger.info(out_and_err_tuple[0])
        if out_and_err_tuple[1]:
            self.__class__.logger.warn(out_and_err_tuple[1])
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
                return map(lambda command:
                    self._exec(command, stdin),
                    commands)
        else:
            if pipe_commands:
                self.__class__.logger.info("Not Run: ")
                self.__class__.logger.info(' | ' .join(map(lambda command: ' '.join(command), commands)))
            else:
                for command in commands:
                    self.__class__.logger.info("Not Run: %s", ' '.join(command))
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


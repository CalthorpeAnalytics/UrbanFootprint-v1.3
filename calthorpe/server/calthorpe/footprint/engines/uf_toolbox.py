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
import subprocess, threading, Queue
#from footprint.lib.functions import merge
import psycopg2
#from footprint.utils.utils import database_settings


##-----------------------------------------------
class Multithread_process(threading.Thread):
    """Threaded Unit of work"""

    def __init__(self, queue, tQueuedJobStr, connection_string):
        threading.Thread.__init__(self)
        self.queue = queue
        self.tQueuedJobStr = tQueuedJobStr
        self.connection_string = connection_string

    def run(self):
        while True:
            #grabs host from queue
            jobD = self.queue.get()
            Task = self.tQueuedJobStr.format(jobD['start_id'], jobD['end_id'])
            execute_sql(Task, self.connection_string)
            self.queue.task_done()
            return


def queue_process():
    queue = Queue.Queue()
    return queue


def execute_sql(pSQL, connection):
    try:
        conn = psycopg2.connect(connection)
    except Exception, E:
        print str(E)
    curs = conn.cursor()

    try:
        curs.execute(pSQL)
    except Exception, E:
        print str(E)
        # raise Exception('SQL: {0}. Original Message: {1}'.format(pSQL, E.message))
    finally:
        conn.commit()
        conn.close


def copy_from_text_to_db(text_file, table_name, connection):
    try:
        conn = psycopg2.connect(connection)
    except Exception, E:
        print str(E)
    curs = conn.cursor()

    try:
        curs.copy_from(text_file, table_name)
    except Exception, E:
        print str(E)
        raise Exception('Original Message: {0}'.format(E.message))
    finally:
        conn.commit()
        conn.close


def report_sql_values(pSQL, connection, fetch_type):
    try:
        conn = psycopg2.connect(connection)
        curs = conn.cursor()
    except Exception, E:
        print str(E)

    try:
        curs.execute(pSQL)
    except Exception, E:
        print str(E)

    Sql_Values = getattr(curs, fetch_type)()
    conn.close
    return Sql_Values


def report_sql_values_as_dict(query, connection_string):
    try:
        conn = psycopg2.connect(connection_string)
    except Exception, E:
        print str(E)
    curs = conn.cursor()

    try:
        curs.execute(query)
    except Exception, E:
        print str(E)

    r = [dict((curs.description[i][0], value) for i, value in enumerate(row)) for row in curs.fetchall()]
    curs.connection.close()
    return r if r else None


def copy_to_psql(output_tmp, cDSN, working_schema, tmp_table_name):
    try:
        conn = psycopg2.connect(cDSN)
    except Exception, E:
        print str(E)
    curs = conn.cursor()

    curs.copy_from(output_tmp, working_schema + "." + tmp_table_name)
    conn.commit()


def connect(conn_string):
    '''given a connection string, connects to the database and returns a cursor '''
    try:
        gDB = psycopg2.connect(conn_string)
    except Exception, E:
        print str(E)
        raise
    return gDB


def get_conn_string(db_name):
    d = database_settings(db_name)
    return 'dbname=' + d['NAME'] + ' host=' + d['HOST'] + ' user=' + d['USER'] + ' password=' + d['PASSWORD']


def db_table_exists(table, cursor=None):
    try:
        if not cursor:
            from django.db import connection

            cursor = connection.cursor()
        if not cursor:
            raise Exception
        try:
            selection = """SELECT tablename FROM pg_tables"""
            cursor.execute("SELECT tablename FROM pg_tables")
        except:
            raise
        table_names = cursor.fetchall()
        tables = []
        for t in table_names:
            tables.append(t[0])
            # table_names = connection.introspection.get_table_list(cursor)
    except:
        raise Exception("unable to determine if the table '%s' exists" % table)
    else:
        return table in tables


def executeSQL_now(conn_string, sqls, db=None, **kwargs):
    resultset = []
    for sql in sqls:
        try:
            db = connect(conn_string)
            gCurs = db.cursor()

            try:
                gCurs.execute(sql)
            except Exception, E:
                print str(E)
                raise

            try:
                result = gCurs.fetchall()
            except:
                result = ()

            db.commit()

            results = []
            for n in result: results.append(n)
            resultset.append(results)

        except Exception, E:
            resultset.append(E)

    return resultset


def get_geom_reg(conn_string, schema, table):
    #TODO: update this to use the views.geometry columns
    query = "select srid, type, coord_dimension from views.geometry_columns " \
            "where f_table_schema = '{0}' and f_table_name = '{1}'".format(schema, table)
    return executeSQL_now(conn_string, [query])[0][0]


def list_all_geom_tables(conn_string):
    query = "select table_schema, table_name from information_schema.columns where column_name = 'wkb_geometry';"
    return executeSQL_now(conn_string, [query])


def get_constraints(conn_string, schema, table):
    query = """select constraint_name from information_schema.constraint_column_usage
    where table_schema = '{0}' and table_name = '{1}'""".format(schema, table)
    return executeSQL_now(conn_string, [query])

# return qualities of the geometry field

def get_geom_type(conn_string, schema, table):
    query = "select distinct(geometrytype(wkb_geometry)) from {0}.{1}".format(schema, table)
    return executeSQL_now(conn_string, [query])


def get_geom_SRID(conn_string, schema, table):
    query = "select distinct(st_srid(wkb_geometry)) from {0}.{1}".format(schema, table)
    return executeSQL_now(conn_string, [query])


def get_geom_dims(conn_string, schema, table):
    query = "select distinct(ST_CoordDim(wkb_geometry)) from {0}.{1}".format(schema, table)
    return executeSQL_now(conn_string, [query])

# add constraints functions

def add_constraint_geom_type(conn_string, schema, table, geom_type):
    add_constraint = "ALTER TABLE {0}.{1} ADD CONSTRAINT enforce_geotype_wkb_geometry check(geometrytype(wkb_geometry) = '{2}');".format(
        schema, table, geom_type)
    executeSQL_now(conn_string, [add_constraint])


def add_constraint_SRID(conn_string, schema, table, srid):
    add_constraint = "ALTER TABLE {0}.{1} ADD CONSTRAINT enforce_srid_wkb_geometry check (st_srid(wkb_geometry) = '{2}');".format(
        schema, table, srid)
    executeSQL_now(conn_string, [add_constraint])


def add_constraint_geom_dims(conn_string, schema, table, geom_dims):
    add_constraint = "ALTER TABLE {0}.{1} ADD CONSTRAINT enforce_dims_wkb_geometry check (ST_CoordDim(wkb_geometry) = {2});".format(
        schema, table, geom_dims)
    executeSQL_now(conn_string, [add_constraint])

# drop a constraint
def drop_spatial_constraint(conn_string, schema, table, type, column):
    query = 'ALTER TABLE {0}.{1} DROP CONSTRAINT enforce_{2}_{3};'.format(schema, table, type, column)
    executeSQL_now(conn_string, [query])

# add geometric index
def add_geom_idx(conn_string, schema, table, column="wkb_geometry"):
    query = 'CREATE INDEX {0}_geom_idx on {1}.{0} using GIST ({2});'.format(table, schema, column)
    executeSQL_now(conn_string, [query])


def drop_geom_idx(conn_string, schema, table):
    query = 'DROP INDEX {1}.{0}_geom_idx;'.format(table, schema)
    executeSQL_now(conn_string, [query])


def add_attribute_idx(conn_string, schema, table, field):
    query = 'create index {1}_{2}_idx on {0}.{1} ({2});'.format(schema, table, field)
    executeSQL_now(conn_string, [query])


def add_primary_key(conn_string, schema, table, field):
    query = 'alter table {0}.{1} add constraint {1}_pk primary key ({2});'.format(schema, table, field)
    executeSQL_now(conn_string, [query])


def drop_table(table_name, conn_string):
    pSql = '''drop table if exists {0} cascade;'''.format(table_name)
    execute_sql(pSql, conn_string)

#----------------------------------------------------------------------------------------
def create_sql_calculations(table_fields, sql_format):
    sql_calculations = ''
    for field in table_fields:
        sql_calculations += sql_format.format(field)

    return sql_calculations


def create_sql_calculations_two_variables(table_fields, sql_query):
    sql_calculations = ''
    for field in table_fields:
        sql_calculations += sql_query.format(field[0], field[1])
    return sql_calculations


def create_sql_calculations_four_variables(table_fields, sql_query):
    sql_calculations = ''
    for field in table_fields:
        sql_calculations += sql_query.format(field[0], field[1], field[2], field[3], field[4])
    return sql_calculations


# make sure all spatial tables in db have proper constraints
# this will ensure that they are registered in the geometry_columns view
def validate_constraints_whole_db(conn_string):
    geom_tables = list_all_geom_tables(conn_string)
    for t in geom_tables[0]:
        schema, table = t[0], t[1]
        validate_constraints(conn_string, schema, table)


def validate_constraints(conn_string, schema, table):
    info = schema + '.' + table
    constraints = get_constraints(conn_string, schema, table)[0]

    # make sure the SRID has a constraint, and if not, create one
    if ("enforce_srid_wkb_geometry",) not in constraints:
        try:
            srid = get_geom_SRID(conn_string, schema, table)[0][0]
            # TODO: better error handling here -- can we try fixing the problem before rejecting it?
            if len(srid) > 1:
                print "there are multiple SRID's for this table, cannot add constraint"
                raise
            elif len(srid) == 0:
                print "there is no SRID for the geometry in this table. cannot add constraint"
                raise
            else:
                add_constraint_SRID(conn_string, schema, table, srid[0])
                info += ': added SRID constraint, '
        except Exception, E:
            print E
            raise
    else:
        info += ': SRID OK, '

    # make sure the geometry type has a constraint, and if not, create one
    if ("enforce_geotype_wkb_geometry",) not in constraints:
        try:
            geom_type = get_geom_type(conn_string, schema, table)[0][0]
            # TODO: better error handling here -- can we try fixing the problem before rejecting it?
            if len(geom_type) > 1:
                print "there are multiple geometry types for this table. cannot add constraint"
                raise
            elif len(geom_type) == 0:
                print "there is no geometry type for the geometry in this table. cannot add constraint"
                raise
            else:
                add_constraint_geom_type(conn_string, schema, table, geom_type[0])
                info += ' added geom_type constraint, '
        except Exception, E:
            print E;
            raise

    else:
        info += ' geom_type OK, '

    # make sure the number of dimensions has a constraint, and if not, create one
    if ("enforce_dims_wkb_geometry",) not in constraints:
        try:
            dims = get_geom_dims(conn_string, schema, table)[0][0]
            # TODO: better error handling here -- can we try fixing the problem before rejecting it?
            if len(dims) > 1:
                print "there are inconsistent coordinate dimensions for this table. cannot add constraint"
                raise
            elif len(dims) == 0:
                print "there are no coordinate dimensions for the geometry in this table. cannot add constraint"
                raise
            else:
                add_constraint_geom_dims(conn_string, schema, table, dims[0])
                info += ' added coord_dims constraint'
        except Exception, E:
            print E
            raise

    else:
        info += ' coord_dims OK '

    print info


def reproject_table(conn_string, schema, table, srid):
#    old_srid, type, coords = get_geom_reg(conn_string, schema, table)
#    drop_spatial_constraint(conn_string,schema,table,type,'wkb_geometry')
#    if old_srid <> 0:
#        # TODO column doesn't exist
#        #drop_spatial_constraint(conn_string, schema, table, 'srid', column)
#        pass
    drop_geom_idx(conn_string, schema, table)
    reproject = 'UPDATE {0}.{1} set wkb_geometry = ST_setSRID(ST_transform(wkb_geometry, {2}),{2});' \
        .format(schema, table, srid)
    executeSQL_now(conn_string, [reproject])
    add_geom_idx(conn_string, schema, table)

#    add_constraint_SRID(conn_string, schema, table, srid)

def ogr_to_gdb(conn_string, schema, table, output_gdb):
    reproject_table(conn_string, schema, table, '4326')
    ogr_command = 'ogr2ogr -overwrite -skipfailures -f "FileGDB" "{1}" PG:"{0}" "{2}.{3}" ' \
        .format(conn_string, output_gdb, schema, table)
    print ogr_command
    subprocess.call(ogr_command, shell=True)


def register_geometry_columns(server, schema=None):
    select_tables = "Truncate geometry_columns cascade; \n" \
                    "select table_name, table_schema from information_schema.columns " \
                    "where column_name = 'wkb_geometry' " \
                    "and table_schema = '{0}';".format(schema)
    if not schema:
        select_tables = "Truncate geometry_columns cascade; \n" \
                        "select table_name, table_schema from information_schema.columns " \
                        "where column_name = 'wkb_geometry';"

    try:
        gDB = psycopg2.connect(server)
    except Exception, E:
        print str(E)
        raise
    gCurs = gDB.cursor()

    try:
        print select_tables
        gCurs.execute(select_tables)
    except Exception, E:
        print str(E)
        raise
    tables_to_fix = gCurs.fetchall()
    print tables_to_fix
    if not schema:
        print "assigning schema"

    for t in tables_to_fix:
        print t
        update = '''

        INSERT INTO geometry_columns(f_table_catalog, f_table_schema, f_table_name, f_geometry_column, coord_dimension,
        srid, "type")
        SELECT '', '{0}', '{1}', 'wkb_geometry', ST_CoordDim(wkb_geometry), ST_SRID(wkb_geometry),
        ST_GeometryType(wkb_geometry)
        FROM {0}.{1} LIMIT 1;'''.format(t[1], t[0])
        try:
            print update
            r = gCurs.execute(update)
            gDB.commit()
        except Exception, E:
            print str(E)
            gDB.close()
            gDB = psycopg2.connect(server)
            gCurs = gDB.cursor()



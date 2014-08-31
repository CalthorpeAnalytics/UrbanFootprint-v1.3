from footprint.common.utils.websockets import send_message_to_client
from footprint.main.models.config.scenario import FutureScenario
from footprint.main.models.geospatial.db_entity_keys import DbEntityKey
from footprint.main.models.keys.keys import Keys
from footprint.main.publishing.data_import_publishing import create_and_populate_relations
from footprint.main.utils.uf_toolbox import queue_process, report_sql_values, execute_sql, drop_table, \
    add_primary_key, count_cores, add_geom_idx, MultithreadProcess, reproject_table, add_constraint_SRID, truncate_table
from footprint.main.utils.utils import parse_schema_and_table

__author__ = 'calthorpe'


def run_one_mile_buffers(config_entity):
    #for the vmt model, this function calculates the sum of each field within a quarter mile of each input geometry
    #and produces an output join table

    thread_count = count_cores()

    vmt_one_mile_class = config_entity.db_entity_feature_class(DbEntityKey.VMT_ONE_MILE_BUFFER)

    if isinstance(config_entity.subclassed_config_entity, FutureScenario):
        scenario_class = config_entity.db_entity_feature_class(DbEntityKey.END_STATE)

    else:
        scenario_class = config_entity.db_entity_feature_class(DbEntityKey.BASE)

    input_table = scenario_class.db_entity_key
    input_schema = parse_schema_and_table(scenario_class._meta.db_table)[0]

    vmt_table = vmt_one_mile_class.db_entity_key
    vmt_schema = parse_schema_and_table(vmt_one_mile_class._meta.db_table)[0]
    vmt_rel_table = parse_schema_and_table(vmt_one_mile_class._meta.db_table)[1]
    vmt_rel_column = vmt_one_mile_class._meta.parents.values()[0].column

    queue = queue_process()

    gQry = '''select pg_typeof(id) from {0}.{1} limit 1;'''.format(input_schema, input_table)
    geometry_id_type = report_sql_values(gQry, 'fetchone')[0]

    pSql = '''drop function if exists one_mile_buffer(
      in_id {0},
      in_wkb_geometry geometry,
      OUT id {0},
      OUT emp numeric(14,4),
      OUT wkb_geometry geometry
      );'''.format(geometry_id_type)

    execute_sql(pSql)
    
    print 'Multithread running'

    gQry1 = '''
    CREATE OR REPLACE FUNCTION one_mile_buffer(
      in_id {2},
      in_wkb_geometry geometry,
      OUT id {2},
      OUT emp numeric(14,4),
      OUT wkb_geometry geometry
      ) 
    AS
    $$
      select $1 as id,
        sum(round(cast(r.emp as numeric(14,4)), 4)) as emp,
        st_transform($2, 4326) as wkb_geometry
      FROM {0}.{1}_geom_tmp a
       inner join {0}.{1} r on a.id = r.id WHERE st_dwithin( $2, a.wkb_geometry, 1608)
    $$ 
    COST 10000
    language SQL STABLE strict;
    '''.format(input_schema, input_table, geometry_id_type)

    execute_sql(gQry1)

    truncate_table(vmt_schema + '.'+ vmt_table)

    #pass a flat list of the input table ids for the multithread process to use to split the process into tasks
    id_list = scenario_class.objects.values_list('id', flat=True).order_by('id')
    ##-----------------------------------------------------------------------------
    #spawn a pool of threads, and pass them queue instance

    insert_sql = '''
    insert into {0}.{1}
      select (f).* from (select one_mile_buffer(a.id, b.wkb_geometry) as f
            from {2}.{3} a
            inner join {2}.{3}_geom_tmp b on a.id = b.id
        where a.id >= {4} and a.id <= {5} and du + emp > 0 offset 0) s;
    '''.format(vmt_schema, vmt_table, input_schema, input_table, "{0}", "{1}")

    for i in range(thread_count):
        t = MultithreadProcess(queue, insert_sql)
        t.setDaemon(True)
        t.start()

    #populate queue with data
    rows_per_thread = len(id_list) / thread_count
    offset = 0

    for i in range(thread_count):
        if i == thread_count - 1:
            ## last bucket gets any remainder, too
            last_thread = len(id_list) - 1
        else:
            last_thread = offset + rows_per_thread - 1

        rows_to_process = {
            'start_id': id_list[offset],
            'end_id': id_list[last_thread]
        }

        offset += rows_per_thread
        queue.put(rows_to_process)

    #wait on the queue until everything has been processed
    queue.join()

    truncate_table(vmt_schema + '.'+ vmt_rel_table)

    pSql = '''
    DO $$
    BEGIN
        BEGIN
            ALTER TABLE {vmt_schema}.{vmt_rel_table} ADD COLUMN {vmt_rel_column} int;
        EXCEPTION
            WHEN duplicate_column
                THEN -- do nothing;
        END;
    END;
    $$'''.format(
        vmt_schema=vmt_schema,
        vmt_rel_table=vmt_rel_table,
        vmt_rel_column=vmt_rel_column
    )
    execute_sql(pSql)

    pSql = '''
    insert into {vmt_schema}.{vmt_rel_table} ({vmt_rel_column}) select id from {vmt_schema}.{vmt_table};'''.format(
        vmt_schema=vmt_schema,
        vmt_table=vmt_table,
        vmt_rel_table=vmt_rel_table,
        vmt_rel_column=vmt_rel_column)

    execute_sql(pSql)

    create_and_populate_relations(config_entity, config_entity.computed_db_entities(key=DbEntityKey.VMT_ONE_MILE_BUFFER)[0])

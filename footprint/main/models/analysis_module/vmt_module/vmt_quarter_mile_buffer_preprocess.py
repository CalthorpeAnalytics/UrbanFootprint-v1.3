from footprint.main.models.config.scenario import FutureScenario
from footprint.main.models.keys.keys import Keys
from footprint.main.utils.uf_toolbox import queue_process, report_sql_values, execute_sql, drop_table, \
    MultithreadProcess, add_primary_key, count_cores, add_geom_idx, drop_geom_idx, drop_spatial_constraint, reproject_table, add_constraint_SRID
from footprint.main.utils.utils import parse_schema_and_table

__author__ = 'calthorpe'



def run_quarter_mile_buffers(config_entity):
    #for the vmt model, this function calculates the sum of each field within a quarter mile of each input geometry
    #and produces an output join table

    thread_count = count_cores()
    
    vmt_quarter_mile_class = config_entity.feature_class_of_db_entity_key(Keys.DB_ABSTRACT_VMT_QUARTER_MILE_BUFFER_FEATURE)
     
    if isinstance(config_entity.subclassed_config_entity, FutureScenario):
        scenario_class = config_entity.feature_class_of_db_entity_key(Keys.DB_ABSTRACT_END_STATE_FEATURE)
        
    else:
        scenario_class = config_entity.feature_class_of_db_entity_key(Keys.DB_ABSTRACT_BASE_FEATURE)


    input_table = scenario_class.db_entity_key
    input_schema = parse_schema_and_table(scenario_class._meta.db_table)[0]

    vmt_table = vmt_quarter_mile_class.db_entity_key
    vmt_schema = parse_schema_and_table(vmt_quarter_mile_class._meta.db_table)[0]

    queue = queue_process()

    gQry = '''select pg_typeof(id) from {0}.{1} limit 2;'''.format(input_schema, input_table)
    geometry_id_type = report_sql_values(gQry, 'fetchone')[0]

    pSql = '''drop function if exists quarter_mile_buffer(
      in_id {0},
      in_wkb_geometry geometry,
      OUT id {0},
      OUT acres_parcel_res numeric(14,4),
      OUT acres_parcel_emp numeric(14,4),
      OUT acres_parcel_mixed numeric(14,4),
      OUT du numeric(14,4),
      OUT pop numeric(14,4),
      OUT emp numeric(14,4),
      OUT emp_ret numeric(14,4),
      OUT wkb_geometry geometry
      );'''.format(geometry_id_type)

    execute_sql(pSql)
    
    print 'Multithread running'

    gQry1 = '''
    CREATE OR REPLACE FUNCTION quarter_mile_buffer(
      in_id {2},
      in_wkb_geometry geometry,
      OUT id {2},
      OUT acres_parcel_res numeric(14,4),
      OUT acres_parcel_emp numeric(14,4),
      OUT acres_parcel_mixed numeric(14,4),
      OUT du numeric(14,4),
      OUT pop numeric(14,4),
      OUT emp numeric(14,4),
      OUT emp_ret numeric(14,4),
      OUT wkb_geometry geometry
      ) 
    AS
    $$
      select $1 as id, 
        sum(round(cast(r.acres_parcel_res as numeric(14,4)), 4)) as acres_parcel_res,
        sum(round(cast(r.acres_parcel_emp as numeric(14,4)), 4)) as acres_parcel_emp,
        sum(round(cast(r.acres_parcel_mixed as numeric(14,4)), 4)) as acres_parcel_mixed,
        sum(round(cast(r.du  as numeric(14,4)), 4)) as du,
        sum(round(cast(r.pop as numeric(14,4)), 4)) as pop,
        sum(round(cast(r.emp as numeric(14,4)), 4)) as emp,
        sum(round(cast(r.emp_ret as numeric(14,4)), 4)) as emp_ret,
        $2 as wkb_geometry
      FROM {0}.{1} r WHERE st_dwithin( $2, st_transform(r.wkb_geometry, 3310), 402)
    $$ 
    COST 10000
    language SQL STABLE strict;
    '''.format(input_schema, input_table, geometry_id_type)

    execute_sql(gQry1)

    drop_table('''{0}.{1}'''.format(vmt_schema, vmt_table))

    pSql = '''
    create table {0}.{1}
        (
            id serial NOT NULL,
            acres_parcel_res numeric(14,4) NOT NULL,
            acres_parcel_emp numeric(14,4) NOT NULL,
            acres_parcel_mixed numeric(14,4) NOT NULL,
            du numeric(14,4) NOT NULL,
            pop numeric(14,4) NOT NULL,
            emp numeric(14,4) NOT NULL,
            emp_ret numeric(14,4) NOT NULL,
            wkb_geometry geometry
        );'''.format(vmt_schema, vmt_table)

    execute_sql(pSql)

    #=======================================================================================

    #pass a flat list of the input table ids for the multithread process to use to split the process into tasks
    id_list = scenario_class.objects.values_list('id', flat=True).order_by('id')
    ##-----------------------------------------------------------------------------
    #spawn a pool of threads, and pass them queue instance

    insert_sql = '''
    insert into {0}.{1}
      select (f).* from (select quarter_mile_buffer(id, st_transform(wkb_geometry,3310)) as f
            from {2}.{3}
        where id >= {4} and id <= {5} offset 0) s;
    '''.format(vmt_schema, vmt_table, input_schema, input_table, "{0}", "{1}")

    for i in range(thread_count):
        t = MultithreadProcess(queue, insert_sql)
        t.setDaemon(True)
        t.start()

    ##---------------------------------------------------
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

    reproject_table(vmt_schema, vmt_table, '4326')
    add_primary_key(vmt_schema, vmt_table, 'id')
    add_geom_idx(vmt_schema, vmt_table)
    add_constraint_SRID(vmt_schema, vmt_table, '4326')

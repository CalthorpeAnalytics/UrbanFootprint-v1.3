from footprint.main.lib.functions import flatten
from footprint.main.models.config.scenario import FutureScenario
from footprint.main.models.keys.keys import Keys
from footprint.main.utils.uf_toolbox import queue_process, report_sql_values, execute_sql, drop_table, \
    MultithreadProcess, add_primary_key, count_cores, add_geom_idx, add_constraint_SRID
from footprint.main.utils.utils import parse_schema_and_table

__author__ = 'calthorpe'



def run_variable_buffers(config_entity):
    #for the vmt model, this function calculates the sum of each field within a variable buffer of each input geometry
    #and produces an output join table

    thread_count = count_cores()


    if isinstance(config_entity.subclassed_config_entity, FutureScenario):
        scenario_class = config_entity.feature_class_of_db_entity_key(Keys.DB_ABSTRACT_END_STATE_FEATURE)
        demographics_class = config_entity.feature_class_of_db_entity_key(Keys.DB_ABSTRACT_END_STATE_DEMOGRAPHIC_FEATURE)
        vmt_trip_lengths_class = config_entity.feature_class_of_db_entity_key(Keys.DB_ABSTRACT_VMT_FUTURE_TRIP_LENGTHS_FEATURE)

    else:
        scenario_class = config_entity.feature_class_of_db_entity_key(Keys.DB_ABSTRACT_BASE_FEATURE)
        demographics_class = config_entity.feature_class_of_db_entity_key(Keys.DB_ABSTRACT_BASE_DEMOGRAPHIC_FEATURE)
        vmt_trip_lengths_class = config_entity.feature_class_of_db_entity_key(Keys.DB_ABSTRACT_VMT_BASE_TRIP_LENGTHS_FEATURE)

    vmt_variable_class = config_entity.feature_class_of_db_entity_key(Keys.DB_ABSTRACT_VMT_VARIABLE_BUFFER_FEATURE)


    input_table = scenario_class.db_entity_key
    input_demographic_table = demographics_class.db_entity_key
    input_schema = parse_schema_and_table(scenario_class._meta.db_table)[0]


    vmt_table = vmt_variable_class.db_entity_key
    vmt_schema = parse_schema_and_table(vmt_variable_class._meta.db_table)[0]


    project_schema = parse_schema_and_table(vmt_trip_lengths_class._meta.db_table)[0]
    vmt_trips_table = vmt_trip_lengths_class.db_entity_key

    queue = queue_process()
    
    drop_table('''{0}.{1}_intersect'''.format(vmt_schema, vmt_table))
    pSql = '''
    create table {4}.{5}_intersect
        as select
            a.id as id, 
            b.id as trip_id,
            a.wkb_geometry
        from {0}.{1} a, {2}.{3} b
    where st_intersects(st_centroid(a.wkb_geometry), b.wkb_geometry);

    '''.format(input_schema, input_table, project_schema, vmt_trips_table, vmt_schema, vmt_table)

    execute_sql(pSql)


    drop_table('''{0}.{1}_grouped'''.format(vmt_schema, vmt_table))

    pSql = '''
    create table {5}.{6}_grouped
        as select
            trip_id as id, d.wkb_geometry,
            sum(round(cast(b.acres_parcel_res as numeric(14,4)), 4)) as acres_parcel_res,
            sum(round(cast(b.acres_parcel_emp as numeric(14,4)), 4)) as acres_parcel_emp,
            sum(round(cast(b.acres_parcel_mixed as numeric(14,4)), 4)) as acres_parcel_mixed,
            sum(round(cast(b.du as numeric(14,4)), 4)) as du,
            sum(round(cast(b.pop as numeric(14,4)), 4)) as pop,
            sum(round(cast(b.emp as numeric(14,4)), 4)) as emp,
            sum(round(cast(b.emp_ret as numeric(14,4)), 4)) as emp_ret,
            sum(round(cast(b.hh as numeric(14,4)), 4)) as hh,
            sum(round(cast(b.du_mf as numeric(14,4)), 4)) as du_mf,
            sum(round(cast(c.hh_inc_00_10 as numeric(14,4)), 4)) as hh_inc_00_10,
            sum(round(cast(c.hh_inc_10_20 as numeric(14,4)), 4)) as hh_inc_10_20,
            sum(round(cast(c.hh_inc_20_30 as numeric(14,4)), 4)) as hh_inc_20_30,
            sum(round(cast(c.hh_inc_30_40 as numeric(14,4)), 4)) as hh_inc_30_40,
            sum(round(cast(c.hh_inc_40_50 as numeric(14,4)), 4)) as hh_inc_40_50,
            sum(round(cast(c.hh_inc_50_60 as numeric(14,4)), 4)) as hh_inc_50_60,
            sum(round(cast(c.hh_inc_60_75 as numeric(14,4)), 4)) as hh_inc_60_75,
            sum(round(cast(c.hh_inc_75_100 as numeric(14,4)), 4)) as hh_inc_75_100,
            sum(round(cast(c.hh_inc_100_125 + c.hh_inc_125_150 + c.hh_inc_150_200 + c.hh_inc_200p as numeric(14,4)), 4)) as hh_inc_100p,
            sum(round(cast(c.pop_employed as numeric(14,4)), 4)) as pop_employed,
            sum(round(cast(c.pop_age16_up as numeric(14,4)), 4)) as pop_age16_up,
            sum(round(cast(c.pop_age65_up as numeric(14,4)), 4)) as pop_age65_up

        from {5}.{6}_intersect a
        left join {0}.{1} b on a.id = b.id
        left join {0}.{2} c on a.id = c.id
        left join {3}.{4} d on a.trip_id = d.id
        group by trip_id, d.wkb_geometry;
    '''.format(input_schema, input_table, input_demographic_table, project_schema, vmt_trips_table, vmt_schema,
               vmt_table)

    execute_sql(pSql)
    
    add_geom_idx(vmt_schema, '{0}_grouped'.format(vmt_table))
    add_primary_key(vmt_schema, '{0}_grouped'.format(vmt_table), 'id')
    
    
    gQry = '''select pg_typeof(id) from {0}.{1}_grouped limit 1;'''.format(vmt_schema, vmt_table)
    geometry_id_type = report_sql_values(gQry, 'fetchone')[0]

    pSql = '''drop function if exists variable_distance_buffers(
      in_id {0},
      in_distance numeric(14,4),
      in_geometry geometry,
      OUT id {0},
      OUT distance numeric(14,4),
      OUT acres_parcel_res numeric(14,4),
      OUT acres_parcel_emp numeric(14,4),
      OUT acres_parcel_mixed numeric(14,4),
      OUT du numeric(14,4),
      OUT pop numeric(14,4),
      OUT emp numeric(14,4),
      OUT emp_ret numeric(14,4),
      OUT hh numeric(14,4),
      OUT du_mf numeric(14,4),
      OUT hh_inc_00_10 numeric(14,4),
      OUT hh_inc_10_20 numeric(14,4),
      OUT hh_inc_20_30 numeric(14,4),
      OUT hh_inc_30_40 numeric(14,4),
      OUT hh_inc_40_50 numeric(14,4),
      OUT hh_inc_50_60 numeric(14,4),
      OUT hh_inc_60_75 numeric(14,4),
      OUT hh_inc_75_100 numeric(14,4),
      OUT hh_inc_100p numeric(14,4),
      OUT pop_employed numeric(14,4),
      OUT pop_age16_up numeric(14,4),
      OUT pop_age65_up numeric(14,4)
      );'''.format(geometry_id_type)

    execute_sql(pSql)
    
    print 'Multithread running'

    gQry1 = '''
    CREATE OR REPLACE FUNCTION variable_distance_buffers(
      in_id {0},
      in_distance numeric(14,4),
      in_geometry geometry,
      OUT id {0},
      OUT distance numeric(14,4),
      OUT acres_parcel_res numeric(14,4),
      OUT acres_parcel_emp numeric(14,4),
      OUT acres_parcel_mixed numeric(14,4),
      OUT du numeric(14,4),
      OUT pop numeric(14,4),
      OUT emp numeric(14,4),
      OUT emp_ret numeric(14,4),
      OUT hh numeric(14,4),
      OUT du_mf numeric(14,4),
      OUT hh_inc_00_10 numeric(14,4),
      OUT hh_inc_10_20 numeric(14,4),
      OUT hh_inc_20_30 numeric(14,4),
      OUT hh_inc_30_40 numeric(14,4),
      OUT hh_inc_40_50 numeric(14,4),
      OUT hh_inc_50_60 numeric(14,4),
      OUT hh_inc_60_75 numeric(14,4),
      OUT hh_inc_75_100 numeric(14,4),
      OUT hh_inc_100p numeric(14,4),
      OUT pop_employed numeric(14,4),
      OUT pop_age16_up numeric(14,4),
      OUT pop_age65_up numeric(14,4)
      ) 
    AS
    $$
      select $1 as id,
        $2 as distance,
        sum(round(cast(r.acres_parcel_res as numeric(14,4)), 4)) as acres_parcel_res,
        sum(round(cast(r.acres_parcel_emp as numeric(14,4)), 4)) as acres_parcel_emp,
        sum(round(cast(r.acres_parcel_mixed as numeric(14,4)), 4)) as acres_parcel_mixed,
        sum(round(cast(r.du as numeric(14,4)), 4)) as du,
        sum(round(cast(r.pop as numeric(14,4)), 4)) as pop,
        sum(round(cast(r.emp as numeric(14,4)), 4)) as emp,
        sum(round(cast(r.emp_ret as numeric(14,4)), 4)) as emp_ret,
        sum(round(cast(r.hh as numeric(14,4)), 4)) as hh,
        sum(round(cast(r.du_mf as numeric(14,4)), 4)) as du_mf,
        sum(round(cast(r.hh_inc_00_10 as numeric(14,4)), 4)) as hh_inc_00_10,
        sum(round(cast(r.hh_inc_10_20 as numeric(14,4)), 4)) as hh_inc_10_20,
        sum(round(cast(r.hh_inc_20_30 as numeric(14,4)), 4)) as hh_inc_20_30,
        sum(round(cast(r.hh_inc_30_40 as numeric(14,4)), 4)) as hh_inc_30_40,
        sum(round(cast(r.hh_inc_40_50 as numeric(14,4)), 4)) as hh_inc_40_50,
        sum(round(cast(r.hh_inc_50_60 as numeric(14,4)), 4)) as hh_inc_50_60,
        sum(round(cast(r.hh_inc_60_75 as numeric(14,4)), 4)) as hh_inc_60_75,
        sum(round(cast(r.hh_inc_75_100 as numeric(14,4)), 4)) as hh_inc_75_100,
        sum(round(cast(r.hh_inc_100p as numeric(14,4)), 4)) as hh_inc_100p,
        sum(round(cast(r.pop_employed as numeric(14,4)), 4)) as pop_employed,
        sum(round(cast(r.pop_age16_up as numeric(14,4)), 4)) as pop_age16_up,
        sum(round(cast(r.pop_age65_up as numeric(14,4)), 4)) as pop_age65_up
      FROM {1}.{2}_grouped r WHERE st_dwithin( $3, ST_TRANSFORM(r.wkb_geometry, 3310), $2)
    $$ 
    COST 10000
    language SQL STABLE strict;
    '''.format(geometry_id_type, vmt_schema, vmt_table)

    execute_sql(gQry1)

    drop_table('''{0}.{1}_tmp'''.format(vmt_schema, vmt_table))


    pSql = '''
    create table {0}.{1}_tmp (
        id serial NOT NULL,
        distance numeric(14,4) NOT NULL,
        acres_parcel_res numeric(14,4) NOT NULL,
        acres_parcel_emp numeric(14,4) NOT NULL,
        acres_parcel_mixed numeric(14,4) NOT NULL,
        du numeric(14,4) NOT NULL,
        pop numeric(14,4) NOT NULL,
        emp numeric(14,4) NOT NULL,
        emp_ret numeric(14,4) NOT NULL,
        hh numeric(14,4) NOT NULL,
        du_mf numeric(14,4) NOT NULL,
        hh_inc_00_10 numeric(14,4) NOT NULL,
        hh_inc_10_20 numeric(14,4) NOT NULL,
        hh_inc_20_30 numeric(14,4) NOT NULL,
        hh_inc_30_40 numeric(14,4) NOT NULL,
        hh_inc_40_50 numeric(14,4) NOT NULL,
        hh_inc_50_60 numeric(14,4) NOT NULL,
        hh_inc_60_75 numeric(14,4) NOT NULL,
        hh_inc_75_100 numeric(14,4) NOT NULL,
        hh_inc_100p numeric(14,4) NOT NULL,
        pop_employed numeric(14,4) NOT NULL,
        pop_age16_up numeric(14,4) NOT NULL,
        pop_age65_up numeric(14,4) NOT NULL
    );'''.format(vmt_schema, vmt_table)

    execute_sql(pSql)

    #=======================================================================================

    #pass a flat list of the input table ids for the multithread process to use to split the process into tasks
    pSql = 'select id from {0}.{1}_grouped order by id'''.format(vmt_schema, vmt_table)
    id_list = flatten(report_sql_values(pSql, 'fetchall'))

    if len(id_list) < 2000:
        thread_count = 1
    else:
        thread_count = count_cores()

    insert_sql = '''
    insert into {0}.{1}_tmp
      select (f).* from (select variable_distance_buffers(c.id, cast(c.attractions_hbw * 1609.0 as numeric(14,4)), ST_TRANSFORM(c.wkb_geometry, 3310)) as f
            from (select a.id, a.attractions_hbw, a.wkb_geometry from {2}.{3} a, {0}.{1}_grouped b where a.id = b.id) as c
        where c.id >= {4} and c.id <= {5}) as s;
    '''.format(vmt_schema, vmt_table, project_schema, vmt_trips_table, "{0}", "{1}")

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

    drop_table('''{0}.{1}'''.format(vmt_schema, vmt_table))
    pSql = '''
    create table {0}.{1}
    as select
       a.id, distance, acres_parcel_res, acres_parcel_emp, acres_parcel_mixed,
       du, pop, emp, emp_ret, hh, du_mf, hh_inc_00_10, hh_inc_10_20,
       hh_inc_20_30, hh_inc_30_40, hh_inc_40_50, hh_inc_50_60, hh_inc_60_75,
       hh_inc_75_100, hh_inc_100p, pop_employed, pop_age16_up, pop_age65_up, productions_hbw,
       productions_hbo, productions_nhb, attractions_hbw, attractions_hbo, attractions_nhb,
       emp_30min_transit, emp_45min_transit, a.wkb_geometry
    from {0}.{1}_intersect a
    left join {0}.{1}_tmp b on a.trip_id = b.id
    left join {2}.{3} c on a.trip_id = c.id
    '''.format(vmt_schema, vmt_table, project_schema, vmt_trips_table)
    execute_sql(pSql)

    add_primary_key(vmt_schema, vmt_table, 'id')
    add_geom_idx(vmt_schema, vmt_table)
    add_constraint_SRID(vmt_schema, vmt_table, '4326')

    drop_table('''{0}.{1}_intersect'''.format(vmt_schema, vmt_table))
    drop_table('''{0}.{1}_grouped'''.format(vmt_schema, vmt_table))
    drop_table('''{0}.{1}_tmp'''.format(vmt_schema, vmt_table))
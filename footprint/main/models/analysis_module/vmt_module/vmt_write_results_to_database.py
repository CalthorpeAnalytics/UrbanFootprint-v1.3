import os
from footprint.main.models.analysis_module.vmt_module.vmt_model_constants import vmt_output_field_list
from footprint.main.models.geospatial.db_entity_keys import DbEntityKey
from footprint.main.publishing.data_import_publishing import create_and_populate_relations
from footprint.main.utils.uf_toolbox import drop_table, execute_sql, copy_from_text_to_db, create_sql_calculations, truncate_table


__author__ = 'calthorpe'

##-----------------------------------------------------------
def write_vmt_results_to_database(options, vmt_output_list):

    drop_table('{0}.{1}'.format(options['vmt_schema'], options['vmt_result_table']))

    attribute_list = filter(lambda x: x != 'id', vmt_output_field_list)
    output_field_syntax = 'id int' + create_sql_calculations(attribute_list, ', {0} numeric(14, 4)')

    pSql = '''
    create table {0}.{1} ({2});'''.format(options['vmt_schema'], options['vmt_result_table'], output_field_syntax)
    execute_sql(pSql)

    if os.path.exists('/tmp/vmt_out_{unique_name}'.format(unique_name=options['vmt_schema'])):
        os.remove('/tmp/vmt_out_{unique_name}'.format(unique_name=options['vmt_schema']))

    vmt_output_text_file_path = open("/tmp/vmt_out_{unique_name}".format(unique_name=options['vmt_schema']), "w")

    for row in vmt_output_list:
        stringrow = []
        for item in row:
            if isinstance(item, int):
                stringrow.append(str(item))
            else:
                stringrow.append(str(round(item, 4)))
        vmt_output_text_file_path.write("\t".join(stringrow,) + "\n")

    vmt_output_text_file_path.close()

    ##---------------------------
    vmt_output_text_file_path = open("/tmp/vmt_out_{unique_name}".format(unique_name=options['vmt_schema']), 'r')

    copy_from_text_to_db(vmt_output_text_file_path, '{0}.{1}'.format(options['vmt_schema'],
                                                                     options['vmt_result_table']))
    ##---------------------------
    pSql = '''alter table {0}.{1} add column wkb_geometry geometry;
    '''.format(options['vmt_schema'], options['vmt_result_table'])
    execute_sql(pSql)

    pSql = '''update {0}.{1} b set
                wkb_geometry = a.wkb_geometry
                from (select id, wkb_geometry from {2}.{3}) a
                where cast(a.id as int) = cast(b.id as int);
    '''.format(options['vmt_schema'], options['vmt_result_table'], options['input_schema'], options['input_table'])

    execute_sql(pSql)


    truncate_table(options['vmt_schema'] + '.'+ options['vmt_rel_table'])

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
        vmt_schema=options['vmt_schema'],
        vmt_rel_table=options['vmt_rel_table'],
        vmt_rel_column=options['vmt_rel_column']
    )
    execute_sql(pSql)

    pSql = '''
    insert into {vmt_schema}.{vmt_rel_table} ({vmt_rel_column}) select id from {vmt_schema}.{vmt_table};'''.format(
        vmt_schema=options['vmt_schema'],
        vmt_table=options['vmt_result_table'],
        vmt_rel_table=options['vmt_rel_table'],
        vmt_rel_column=options['vmt_rel_column'])

    execute_sql(pSql)

    create_and_populate_relations(options['config_entity'], options['config_entity'].computed_db_entities(key=DbEntityKey.VMT)[0])






import os
from footprint.main.models.analysis_module.vmt_module.vmt_model_constants import vmt_output_field_list
from footprint.main.utils.uf_toolbox import drop_table, execute_sql, copy_from_text_to_db, create_sql_calculations


__author__ = 'calthorpe'

##-----------------------------------------------------------
def write_vmt_results_to_database(options, vmt_output_list):

    drop_table('{0}.{1}'.format(options['vmt_schema'], options['vmt_result_table']))

    attribute_list = filter(lambda x: x != 'id', vmt_output_field_list)
    output_field_syntax = 'id int' + create_sql_calculations(attribute_list, ', {0} numeric(14, 4)')

    pSql = '''
    create table {0}.{1} ({2});'''.format(options['vmt_schema'], options['vmt_result_table'], output_field_syntax)
    execute_sql(pSql)

    if os.path.exists('/tmp/vmt_out_tmp'):
        os.remove('/tmp/vmt_out_tmp')

    vmt_output_text_file_path = open("/tmp/vmt_out_tmp", "w")

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
    vmt_output_text_file_path = open("/tmp/vmt_out_tmp", 'r')

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






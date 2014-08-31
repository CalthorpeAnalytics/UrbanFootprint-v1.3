import os
from footprint.main.models.analysis_module.water_module.water_keys import WATER_OUTPUT_FIELDS
from footprint.main.utils.uf_toolbox import drop_table, execute_sql, copy_from_text_to_db, create_sql_calculations


__author__ = 'calthorpe'

##-----------------------------------------------------------
def write_water_results_to_database(options, water_output_list):

    drop_table('{0}.{1}'.format(options['water_schema'], options['water_result_table']))

    attribute_list = filter(lambda x: x != 'id', WATER_OUTPUT_FIELDS)
    attribute_list1 = filter(lambda x: x != 'evapotranspiration_zone', attribute_list)
    output_field_syntax = 'id int' + ', evapotranspiration_zone int' + create_sql_calculations(attribute_list1, ', {0} numeric(14, 4)')

    pSql = '''
    create table {0}.{1} ({2});'''.format(options['water_schema'], options['water_result_table'], output_field_syntax)
    execute_sql(pSql)

    if os.path.exists('/tmp/water_out_{unique_name}'.format(unique_name=options['water_schema'])):
        os.remove('/tmp/water_out_{unique_name}'.format(unique_name=options['water_schema']))

    water_output_text_file_path = open("/tmp/water_out_{unique_name}".format(unique_name=options['water_schema']), "w")

    for row in water_output_list:
        stringrow = []
        for item in row:
            if isinstance(item, int):
                stringrow.append(str(item))
            else:
                stringrow.append(str(round(item, 4)))
        water_output_text_file_path.write("\t".join(stringrow,) + "\n")

    water_output_text_file_path.close()

    ##---------------------------('/tmp/water_out_{unique_name}'))
    water_output_text_file_path = open("/tmp/water_out_{unique_name}".format(unique_name=options['water_schema']), 'r')

    copy_from_text_to_db(water_output_text_file_path, '{0}.{1}'.format(options['water_schema'],
                                                                     options['water_result_table']))
    ##---------------------------
    pSql = '''alter table {0}.{1} add column wkb_geometry geometry;
    '''.format(options['water_schema'], options['water_result_table'])
    execute_sql(pSql)

    pSql = '''update {0}.{1} b set
                wkb_geometry = a.wkb_geometry
                from (select id, wkb_geometry from {2}.{3}) a
                where cast(a.id as int) = cast(b.id as int);
    '''.format(options['water_schema'], options['water_result_table'], options['base_schema'], options['base_table'])

    execute_sql(pSql)






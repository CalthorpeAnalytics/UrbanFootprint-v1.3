import os
from footprint.main.models.analysis_module.energy_module.energy_keys import ENERGY_OUTPUT_FIELDS
from footprint.main.utils.uf_toolbox import drop_table, execute_sql, copy_from_text_to_db, create_sql_calculations


__author__ = 'calthorpe'

##-----------------------------------------------------------
def write_energy_results_to_database(options, energy_output_list):

    drop_table('{0}.{1}'.format(options['energy_schema'], options['energy_result_table']))

    attribute_list = filter(lambda x: x != 'id', ENERGY_OUTPUT_FIELDS)
    attribute_list1 = filter(lambda x: x != 'title24_zone', attribute_list)
    attribute_list2 = filter(lambda x: x != 'fcz_zone', attribute_list1)
    output_field_syntax = 'id int' + ', title24_zone int' + ', fcz_zone int' + create_sql_calculations(attribute_list2, ', {0} numeric(14, 4)')

    pSql = '''
    create table {0}.{1} ({2});'''.format(options['energy_schema'], options['energy_result_table'], output_field_syntax)
    execute_sql(pSql)

    if os.path.exists('/tmp/energy_out_{unique_name}'.format(unique_name=options['energy_schema'])):
        os.remove('/tmp/energy_out_{unique_name}'.format(unique_name=options['energy_schema']))

    energy_output_text_file_path = open("/tmp/energy_out_{unique_name}".format(unique_name=options['energy_schema']), "w")

    for row in energy_output_list:
        stringrow = []
        for item in row:
            if isinstance(item, int):
                stringrow.append(str(item))
            else:
                stringrow.append(str(round(item, 4)))
        energy_output_text_file_path.write("\t".join(stringrow,) + "\n")

    energy_output_text_file_path.close()

    ##---------------------------
    energy_output_text_file_path = open("/tmp/energy_out_{unique_name}".format(unique_name=options['energy_schema']), 'r')

    copy_from_text_to_db(energy_output_text_file_path, '{0}.{1}'.format(options['energy_schema'],
                                                                     options['energy_result_table']))
    ##---------------------------
    pSql = '''alter table {0}.{1} add column wkb_geometry geometry;
    '''.format(options['energy_schema'], options['energy_result_table'])
    execute_sql(pSql)

    pSql = '''update {0}.{1} b set
                wkb_geometry = a.wkb_geometry
                from (select id, wkb_geometry from {2}.{3}) a
                where cast(a.id as int) = cast(b.id as int);
    '''.format(options['energy_schema'], options['energy_result_table'], options['base_schema'], options['base_table'])

    execute_sql(pSql)






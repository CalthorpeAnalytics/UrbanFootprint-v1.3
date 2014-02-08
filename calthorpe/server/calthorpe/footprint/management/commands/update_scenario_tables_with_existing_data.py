from footprint.engines.uf_toolbox import create_sql_calculations, execute_sql
from footprint.models.config.scenario import FutureScenario

__author__ = 'calthorpe'

options = dict(
    region_name = 'sandag',
    project_name = 'sandag',
    scenario_name = 'sandag_scenario_c',
    scenario_feature_table='core_gross_increment_scenario_c_alt1',
    end_state_table='core_end_state_scenario_c_alt1',
    net_increment_table='core_net_increment_scenario_c_alt1',
    connection_string='dbname=urbanfootprint host=10.0.0.24 user=calthorpe password=Calthorpe123'
)

# Phone: (510) 548-6800. Web: www.calthorpe.com
from optparse import make_option
from random import randrange
import logging

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from footprint.models import Placetype
from footprint.models.analysis_module.core import executeCore
from footprint.models.application_initialization import application_initialization, create_data_provider_data
from footprint.models.config.scenario import FutureScenario
from footprint.models.keys.keys import Keys


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
        This command initializes/syncs the footprint server with default and sample data. I'd like this to happen automatically in response to the post_syncdb event, but that event doesn't seem to fire (see management/__init__.py for the attempted wiring)
    """
    option_list = BaseCommand.option_list + (
        make_option('-r', '--resave', action='store_true', default=False,
                    help='Resave all the config_entities to trigger signals'),
        make_option('-s', '--skip', action='store_true', default=False,
                    help='Skip initialization and data creation (for just doing resave)'),
        make_option('--scenario', default='', help='String matching a key of or more Scenario to run'),
    )

    def handle(self, *args, **options):

        def update_future_scenario_feature(options):

            table_fields=['acres_parcel_res', 'acres_parcel_res_detsf_ll',
               'acres_parcel_res_detsf_sl', 'acres_parcel_res_attsf', 'acres_parcel_res_mf',
               'acres_parcel_emp', 'acres_parcel_emp_ret', 'acres_parcel_emp_off',
               'acres_parcel_emp_ind', 'acres_parcel_emp_ag', 'acres_parcel_emp_mixed',
               'acres_parcel_mixed', 'acres_parcel_mixed_w_off', 'acres_parcel_mixed_no_off',
               'pop', 'hh', 'du', 'du_detsf_ll', 'du_detsf_sl', 'du_attsf', 'du_mf', 'emp',
               'emp_ret', 'emp_retail_services', 'emp_restaurant', 'emp_accommodation',
               'emp_arts_entertainment', 'emp_other_services', 'emp_off', 'emp_office_services',
               'emp_education', 'emp_public_admin', 'emp_medical_services', 'emp_ind',
               'emp_wholesale', 'emp_transport_warehousing', 'emp_manufacturing',
               'emp_construction_utilities', 'emp_ag', 'emp_agriculture', 'emp_extraction',
               'emp_military', 'bldg_sqft_detsf_ll', 'bldg_sqft_detsf_sl', 'bldg_sqft_attsf',
               'bldg_sqft_mf', 'bldg_sqft_retail_services', 'bldg_sqft_restaurant',
               'bldg_sqft_accommodation', 'bldg_sqft_arts_entertainment', 'bldg_sqft_other_services',
               'bldg_sqft_office_services', 'bldg_sqft_public_admin', 'bldg_sqft_medical_services',
               'bldg_sqft_education', 'bldg_sqft_wholesale', 'bldg_sqft_transport_warehousing',
               'commercial_irrigated_sqft', 'residential_irrigated_sqft'
            ]


            sql_format = ', {0} = round(cast(b.{0} as numeric(14,4)), 4)'
            update_sql = create_sql_calculations(table_fields, sql_format)


            sql_format = ', a.{0}'
            field_select_sql = create_sql_calculations(table_fields, sql_format)


            pSql = '''
            update {region_name}__{project_name}__{scenario_name}.future_scenario_feature a set
                built_form_id = b.built_form_id,
                refill_flag = (case when b.refill_flag = 1 then true else false end),
                acres_parcel = b.acres_parcel_res + b.acres_parcel_emp + b.acres_parcel_mixed
                {update_sql}
            from
                (select
                    c.id as geography_id,
                    b.id as built_form_id,
                    refill_flag

                    {field_select_sql}

                from {scenario_feature_table} a
                left join footprint_geography c on cast('{region_name}' || '__' || '{project_name}' || '__' || 'base_feature__' || a.geography_id as varchar) = c.source_id
                left join footprint_builtform b on a.placetype_key = b.key) b
            where b.geography_id = a.geography_id;
            '''.format(region_name=options['region_name'], project_name=options['project_name'], scenario_name=options['scenario_name'], update_sql=update_sql, field_select_sql=field_select_sql, scenario_feature_table=options['scenario_feature_table'])

            execute_sql(pSql, options['connection_string'])

        def update_end_state(options):


            table_fields=['acres_parcel_res', 'acres_parcel_res_detsf_ll',
               'acres_parcel_res_detsf_sl', 'acres_parcel_res_attsf', 'acres_parcel_res_mf',
               'acres_parcel_emp', 'acres_parcel_emp_ret', 'acres_parcel_emp_off',
               'acres_parcel_emp_ind', 'acres_parcel_emp_ag', 'acres_parcel_mixed', 'acres_parcel_mixed_w_off', 'acres_parcel_mixed_no_off',
               'pop', 'hh', 'du', 'du_detsf_ll', 'du_detsf_sl', 'du_attsf', 'du_mf', 'emp',
               'emp_ret', 'emp_retail_services', 'emp_restaurant', 'emp_accommodation',
               'emp_arts_entertainment', 'emp_other_services', 'emp_off', 'emp_office_services',
               'emp_education', 'emp_public_admin', 'emp_medical_services', 'emp_ind',
               'emp_wholesale', 'emp_transport_warehousing', 'emp_manufacturing',
               'emp_ag', 'emp_agriculture', 'emp_extraction',
               'emp_military', 'bldg_sqft_detsf_ll', 'bldg_sqft_detsf_sl', 'bldg_sqft_attsf',
               'bldg_sqft_mf', 'bldg_sqft_retail_services', 'bldg_sqft_restaurant',
               'bldg_sqft_accommodation', 'bldg_sqft_arts_entertainment', 'bldg_sqft_other_services',
               'bldg_sqft_office_services', 'bldg_sqft_public_admin', 'bldg_sqft_medical_services',
               'bldg_sqft_education', 'bldg_sqft_wholesale', 'bldg_sqft_transport_warehousing',
               'commercial_irrigated_sqft', 'residential_irrigated_sqft'
            ]


            sql_format = ', {0} = round(cast(b.{0} as numeric(14,4)), 4)'
            update_sql = create_sql_calculations(table_fields, sql_format)


            sql_format = ', a.{0}'
            field_select_sql = create_sql_calculations(table_fields, sql_format)


            pSql = '''
            update {region_name}__{project_name}__{scenario_name}.end_state a set
                built_form_id = b.built_form_id,
                acres_parcel = round(cast(b.acres_parcel_res + b.acres_parcel_emp + b.acres_parcel_mixed as numeric(14,4)), 4),
                emp_construction = round(cast(b.emp_construction_utilities * 0.6 as numeric(14,4)), 4),
                emp_utilities = round(cast(b.emp_construction_utilities * 0.4 as numeric(14,4)), 4)
                {update_sql}
            from
                (select
                    c.id as geography_id,
                    b.id as built_form_id,
                    emp_construction_utilities

                    {field_select_sql}

                from {end_state_table} a
                left join footprint_geography c on cast('{region_name}' || '__' || '{project_name}' || '__' || 'base_feature__' || a.geography_id as varchar) = c.source_id
                left join footprint_builtform b on a.placetype_key = b.key) b
            where b.geography_id = a.geography_id;
            '''.format(region_name=options['region_name'], project_name=options['project_name'], scenario_name=options['scenario_name'], update_sql=update_sql, field_select_sql=field_select_sql, end_state_table=options['end_state_table'])

            execute_sql(pSql, options['connection_string'])



        def update_net_increment(options):



            table_fields=[ 'pop', 'hh', 'du', 'du_detsf_ll', 'du_detsf_sl', 'du_attsf', 'du_mf', 'emp',
               'emp_ret', 'emp_retail_services', 'emp_restaurant', 'emp_accommodation',
               'emp_arts_entertainment', 'emp_other_services', 'emp_off', 'emp_office_services',
               'emp_education', 'emp_public_admin', 'emp_medical_services', 'emp_ind',
               'emp_wholesale', 'emp_transport_warehousing', 'emp_manufacturing',
               'emp_ag', 'emp_agriculture', 'emp_extraction',
               'emp_military'
            ]


            sql_format = ', {0} = round(cast(b.{0} as numeric(14,4)), 4)'
            update_sql = create_sql_calculations(table_fields, sql_format)


            sql_format = ', a.{0}'
            field_select_sql = create_sql_calculations(table_fields, sql_format)


            pSql = '''
            update {region_name}__{project_name}__{scenario_name}.increments a set
                emp_construction = round(cast(b.emp_construction_utilities * 0.6 as numeric(14,4)), 4),
                emp_utilities = round(cast(b.emp_construction_utilities * 0.4 as numeric(14,4)), 4)
                {update_sql}
            from
                (select
                    c.id as geography_id,
                    b.id as built_form_id,
                    emp_construction_utilities

                    {field_select_sql}

                from {net_increment_table} a
                left join footprint_geography c on cast('{region_name}' || '__' || '{project_name}' || '__' || 'base_feature__' || a.geography_id as varchar) = c.source_id
                left join footprint_builtform b on a.placetype_key = b.key) b
            where b.geography_id = a.geography_id;
            '''.format(region_name=options['region_name'], project_name=options['project_name'], scenario_name=options['scenario_name'], update_sql=update_sql, field_select_sql=field_select_sql, net_increment_table=options['net_increment_table'])

            execute_sql(pSql, options['connection_string'])



    # update_future_scenario_feature(options)
    # update_end_state(options)
    update_net_increment(options)
    from footprint.models.signals import post_analytic_run
    post_analytic_run.send(sender=FutureScenario, config_entity=FutureScenario.objects.get(key='scenario_c'))
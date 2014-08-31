from footprint.main.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.main.models.analysis_module.analysis_tool import AnalysisTool
from footprint.main.models.geospatial.db_entity_keys import DbEntityKey

__author__ = 'calthorpe'

from footprint.common.utils.websockets import send_message_to_client
from footprint.main.models.config.scenario import FutureScenario
from django.db.models import Sum, Q
from footprint.main.utils.query_parsing import annotated_related_feature_class_pk_via_geographies
from footprint.main.utils.utils import parse_schema_and_table
from vmt_calculate_final_results import calculate_final_vmt_results
from vmt_calculate_log_odds import calculate_log_odds
from vmt_model_constants import vmt_output_field_list
from vmt_raw_trip_generation import generate_raw_trips
from vmt_trip_purpose_splits import calculate_trip_purpose_splits
from vmt_write_results_to_database import write_vmt_results_to_database
from footprint.main.models.analysis_module.vmt_module.vmt_variable_buffer_preprocess import run_variable_buffers
from footprint.main.models.analysis_module.vmt_module.vmt_quarter_mile_buffer_preprocess import run_quarter_mile_buffers
from footprint.main.models.analysis_module.vmt_module.vmt_one_mile_buffer_preprocess import run_one_mile_buffers
import logging

logger = logging.getLogger(__name__)

class VmtUpdaterTool(AnalysisTool):

    objects = GeoInheritanceManager()

    class Meta(object):
        app_label = 'main'
        abstract = False

    def vmt_progress(self, proportion, **kwargs):

        send_message_to_client(kwargs['user'].id, dict(
            event='postSavePublisherProportionCompleted',
            job_id=str(kwargs['job'].hashid),
            config_entity_id=self.config_entity.id,
            id=kwargs['analysis_module'].id,
            class_name='AnalysisModule',
            key=kwargs['analysis_module'].key,
            proportion=proportion)
        )
        logger.info("Progress {0}".format(proportion))


    def update(self, **kwargs):

        # Make sure all related models have been created before querying
        logger.info("Executing Vmt using {0}".format(self.config_entity))

        self.vmt_progress(0.1, **kwargs)

        try:
            run_quarter_mile_buffers(self.config_entity)
        except Exception, e:
            print e

        self.vmt_progress(0.2, **kwargs)

        try:
            run_one_mile_buffers(self.config_entity)
        except Exception, e:
            print e

        self.vmt_progress(0.4, **kwargs)

        try:
            run_variable_buffers(self.config_entity)
        except Exception, e:
            print e

        self.vmt_progress(0.2, **kwargs)
        self.execute_vmt(**kwargs)

        logger.info("Done executing Vmt")
        logger.info("Executed Vmt using {0}".format(self.config_entity))


    def execute_vmt(self, **kwargs):

        vmt_feature = {}

        one_mile_buffer_class = self.config_entity.db_entity_feature_class(DbEntityKey.VMT_ONE_MILE_BUFFER)
        quarter_mile_buffer_class = self.config_entity.db_entity_feature_class(DbEntityKey.VMT_QUARTER_MILE_BUFFER)
        variable_buffer_class = self.config_entity.db_entity_feature_class(DbEntityKey.VMT_VARIABLE_BUFFER)
        vmt_result_class = self.config_entity.db_entity_feature_class(DbEntityKey.VMT)

        if isinstance(self.config_entity.subclassed_config_entity, FutureScenario):
            scenario_class = self.config_entity.db_entity_feature_class(DbEntityKey.END_STATE)
            demographic_class = self.config_entity.db_entity_feature_class(DbEntityKey.END_STATE_DEMOGRAPHIC)

            features = scenario_class.objects.filter(Q(du__gt=0) | Q(emp__gt=0))

            annotated_features = annotated_related_feature_class_pk_via_geographies(features, self.config_entity, [
            DbEntityKey.VMT_ONE_MILE_BUFFER, DbEntityKey.VMT_QUARTER_MILE_BUFFER,
            DbEntityKey.VMT_VARIABLE_BUFFER, DbEntityKey.END_STATE_DEMOGRAPHIC])
            future = True

        else:
            scenario_class = self.config_entity.db_entity_feature_class(DbEntityKey.BASE)
            demographic_class = self.config_entity.db_entity_feature_class(DbEntityKey.BASE_DEMOGRAPHIC)

            features = scenario_class.objects.filter(Q(du__gt=0) | Q(emp__gt=0))

            annotated_features = annotated_related_feature_class_pk_via_geographies(features, self.config_entity, [
            DbEntityKey.VMT_ONE_MILE_BUFFER, DbEntityKey.VMT_QUARTER_MILE_BUFFER,
            DbEntityKey.VMT_VARIABLE_BUFFER, DbEntityKey.BASE_DEMOGRAPHIC])
            future = False


        options = dict(
            vmt_result_table=vmt_result_class.db_entity_key,
            vmt_schema=parse_schema_and_table(vmt_result_class._meta.db_table)[0],
            input_table=scenario_class.db_entity_key,
            input_schema=parse_schema_and_table(scenario_class._meta.db_table)[0],
            vmt_rel_table=parse_schema_and_table(vmt_result_class._meta.db_table)[1],
            vmt_rel_column=vmt_result_class._meta.parents.values()[0].column,
            config_entity=self.config_entity
        )

        total_employment = scenario_class.objects.aggregate(Sum('emp'))
        vmt_output_list = []

        for feature in annotated_features:
            if future:
                demographic = demographic_class.objects.get(id=feature.end_state_demographic_feature)
            else:
                demographic = demographic_class.objects.get(id=feature.base_demographic_feature)

            one_mile_buffer = one_mile_buffer_class.objects.get(id=feature.vmt_one_mile_buffer_feature)
            quarter_mile_buffer = quarter_mile_buffer_class.objects.get(id=feature.vmt_quarter_mile_buffer_feature)
            variable_buffer = variable_buffer_class.objects.get(id=feature.vmt_variable_buffer_feature)

            vmt_feature['id'] = int(feature.id)
            vmt_feature['acres_gross'] = float(feature.acres_gross)
            vmt_feature['acres_parcel'] = float(feature.acres_parcel)
            vmt_feature['acres_parcel_res'] = float(feature.acres_parcel_res)
            vmt_feature['acres_parcel_emp'] = float(feature.acres_parcel_emp)
            vmt_feature['acres_parcel_mixed'] = float(feature.acres_parcel_mixed)
            vmt_feature['intersections_qtrmi'] = float(feature.intersection_density_sqmi)
            vmt_feature['du'] = float(feature.du)
            vmt_feature['du_occupancy_rate'] = float(demographic.du_occupancy_rate)
            vmt_feature['du_detsf'] = float(feature.du_detsf)
            vmt_feature['du_attsf'] = float(feature.du_attsf)

            vmt_feature['du_mf'] = float(feature.du_mf)
            vmt_feature['du_mf2to4'] = float(feature.du_mf2to4)
            vmt_feature['du_mf5p'] = float(feature.du_mf5p)
            vmt_feature['hh'] = float(feature.hh)
            vmt_feature['hh_avg_size'] = float(demographic.hh_avg_size)
            vmt_feature['hh_avg_inc'] = float(demographic.hh_avg_inc)

            vmt_feature['hh_inc_00_10'] = float(demographic.hh_inc_00_10)
            vmt_feature['hh_inc_10_20'] = float(demographic.hh_inc_10_20)
            vmt_feature['hh_inc_20_30'] = float(demographic.hh_inc_20_30)
            vmt_feature['hh_inc_30_40'] = float(demographic.hh_inc_30_40)
            vmt_feature['hh_inc_40_50'] = float(demographic.hh_inc_40_50)
            vmt_feature['hh_inc_50_60'] = float(demographic.hh_inc_50_60)
            vmt_feature['hh_inc_60_75'] = float(demographic.hh_inc_60_75)
            vmt_feature['hh_inc_75_100'] = float(demographic.hh_inc_75_100)
            vmt_feature['hh_inc_100p'] = float(demographic.hh_inc_100_125 + demographic.hh_inc_125_150 + \
                                         demographic.hh_inc_150_200 + demographic.hh_inc_200p)

            vmt_feature['pop'] = float(feature.pop)
            vmt_feature['pop_employed'] = float(demographic.pop_employed)
            vmt_feature['pop_age16_up'] = float(demographic.pop_age16_up)
            vmt_feature['pop_age65_up'] = float(demographic.pop_age65_up)

            vmt_feature['emp'] = float(feature.emp)
            vmt_feature['emp_retail'] = float(feature.emp_retail_services + feature.emp_other_services)
            vmt_feature['emp_restaccom'] = float(feature.emp_accommodation + feature.emp_restaurant)
            vmt_feature['emp_arts_entertainment'] = float(feature.emp_arts_entertainment)
            vmt_feature['emp_office'] = float(feature.emp_off)
            vmt_feature['emp_public'] = float(feature.emp_public_admin + feature.emp_education)
            vmt_feature['emp_industry'] = float(feature.emp_ind + feature.emp_ag)

            vmt_feature['emp_within_1mile'] = float(one_mile_buffer.emp)
            vmt_feature['hh_within_quarter_mile_trans'] = float(0)

            vmt_feature['vb_acres_parcel_res_total'] = float(variable_buffer.acres_parcel_res)
            vmt_feature['vb_acres_parcel_emp_total'] = float(variable_buffer.acres_parcel_emp)
            vmt_feature['vb_acres_parcel_mixed_total'] = float(variable_buffer.acres_parcel_mixed)
            vmt_feature['vb_du_total'] = float(variable_buffer.du)
            vmt_feature['vb_pop_total'] = float(variable_buffer.pop)
            vmt_feature['vb_emp_total'] = float(variable_buffer.emp)
            vmt_feature['vb_emp_retail_total'] = float(variable_buffer.emp_ret)
            vmt_feature['vb_hh_total'] = float(variable_buffer.hh)
            vmt_feature['vb_du_mf_total'] = float(variable_buffer.du_mf)
            vmt_feature['vb_hh_inc_00_10_total'] = float(variable_buffer.hh_inc_00_10)
            vmt_feature['vb_hh_inc_10_20_total'] = float(variable_buffer.hh_inc_10_20)
            vmt_feature['vb_hh_inc_20_30_total'] = float(variable_buffer.hh_inc_20_30)
            vmt_feature['vb_hh_inc_30_40_total'] = float(variable_buffer.hh_inc_30_40)
            vmt_feature['vb_hh_inc_40_50_total'] = float(variable_buffer.hh_inc_40_50)
            vmt_feature['vb_hh_inc_50_60_total'] = float(variable_buffer.hh_inc_50_60)
            vmt_feature['vb_hh_inc_60_75_total'] = float(variable_buffer.hh_inc_60_75)
            vmt_feature['vb_hh_inc_75_100_total'] = float(variable_buffer.hh_inc_75_100)
            vmt_feature['vb_hh_inc_100p_total'] = float(variable_buffer.hh_inc_100p)

            vmt_feature['vb_pop_employed_total'] = float(variable_buffer.pop_employed)
            vmt_feature['vb_pop_age16_up_total'] = float(variable_buffer.pop_age16_up)
            vmt_feature['vb_pop_age65_up_total'] = float(variable_buffer.pop_age65_up)

            vmt_feature['emp30m_transit'] = float(variable_buffer.emp_30min_transit)
            vmt_feature['emp45m_transit'] = float(variable_buffer.emp_45min_transit)
            vmt_feature['prod_hbw'] = float(variable_buffer.productions_hbw)
            vmt_feature['prod_hbo'] = float(variable_buffer.productions_hbo)
            vmt_feature['prod_nhb'] = float(variable_buffer.productions_nhb)
            vmt_feature['attr_hbw'] = float(variable_buffer.attractions_hbw)
            vmt_feature['attr_hbo'] = float(variable_buffer.attractions_hbo)
            vmt_feature['attr_nhb'] = float(variable_buffer.attractions_nhb)

            vmt_feature['qmb_acres_parcel_res_total'] = float(quarter_mile_buffer.acres_parcel_res)
            vmt_feature['qmb_acres_parcel_emp_total'] = float(quarter_mile_buffer.acres_parcel_emp)
            vmt_feature['qmb_acres_parcel_mixed_total'] = float(quarter_mile_buffer.acres_parcel_mixed)
            vmt_feature['qmb_du_total'] = float(quarter_mile_buffer.du)
            vmt_feature['qmb_pop_total'] = float(quarter_mile_buffer.pop)
            vmt_feature['qmb_emp_total'] = float(quarter_mile_buffer.emp)
            vmt_feature['qmb_emp_retail'] = float(quarter_mile_buffer.emp_ret)
            vmt_feature['hh_avg_veh'] = float(demographic.hh_avg_vehicles)

            vmt_feature['truck_adjustment_factor'] = 0.031
            vmt_feature['total_employment'] = float(total_employment['emp__sum'])
            #----------------------------------
            #run raw trip generation
            #----------------------------------
            vmt_feature_trips = generate_raw_trips(vmt_feature)
            #----------------------------------
            #run trip purpose splits
            #----------------------------------
            vmt_feature_trip_purposes = calculate_trip_purpose_splits(vmt_feature_trips)
            #----------------------------------
            #run log odds
            #----------------------------------
            vmt_feature_log_odds = calculate_log_odds(vmt_feature_trip_purposes)
            #----------------------------------
            #run vmt equations
            #----------------------------------
            vmt_output = calculate_final_vmt_results(vmt_feature_log_odds)

            #filters the vmt feature dictionary for specific output fields for writing to the database
            output_list = map(lambda key: vmt_output[key], vmt_output_field_list)

            vmt_output_list.append(output_list)
        self.vmt_progress(0.1, **kwargs)
        #-- write result db table
        write_vmt_results_to_database(options, vmt_output_list)





import time
import math
from footprint.common.utils.websockets import send_message_to_client
from footprint.main.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.main.models.analysis_module.analysis_tool import AnalysisTool

from footprint.main.models.analysis_module.water_module.water_calculate_base import calculate_base_water
from footprint.main.models.analysis_module.water_module.water_calculate_future import calculate_future_water
from footprint.main.models.analysis_module.water_module.water_format_policy_inputs import FormatPolicyInputs
from footprint.main.models.analysis_module.water_module.water_keys import WATER_OUTPUT_FIELDS
from footprint.main.models.analysis_module.water_module.write_water_results_to_database import write_water_results_to_database
from footprint.main.models.config.scenario import FutureScenario
from footprint.main.models.geospatial.db_entity_keys import DbEntityKey

import logging
from footprint.main.utils.query_parsing import annotated_related_feature_class_pk_via_geographies
from footprint.main.utils.utils import parse_schema_and_table


__author__ = 'calthorpe'

logger = logging.getLogger(__name__)

class WaterUpdaterTool(AnalysisTool):

    objects = GeoInheritanceManager()

    class Meta(object):
        app_label = 'main'
        abstract = False

    def water_progress(self, proportion, **kwargs):

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

        logger.info("Executing Water using {0}".format(self.config_entity))

        self.run_water_calculations(**kwargs)

        logger.info("Done executing Water")
        logger.info("Executed Water using {0}".format(self.config_entity))


    def run_future_water_calculations(self):

        policy_assumptions = FormatPolicyInputs(self.config_entity)

        configuration = dict(
            time_increment=float(self.config_entity.scenario.year - self.config_entity.scenario.project.base_year),
            base_year=float(self.config_entity.scenario.project.base_year),
            future_year=float(self.config_entity.scenario.year)
        )

        water_class = self.config_entity.db_entity_feature_class(DbEntityKey.WATER)

        end_state_class = self.config_entity.db_entity_feature_class(DbEntityKey.END_STATE)
        end_state_demographic_class = self.config_entity.db_entity_feature_class(DbEntityKey.END_STATE_DEMOGRAPHIC)
        base_class = self.config_entity.db_entity_feature_class(DbEntityKey.BASE)
        base_demographic_class = self.config_entity.db_entity_feature_class(DbEntityKey.BASE_DEMOGRAPHIC)
        climate_zone_class = self.config_entity.db_entity_feature_class(DbEntityKey.CLIMATE_ZONE)

        features = end_state_class.objects.all()

        annotated_features = annotated_related_feature_class_pk_via_geographies(features, self.config_entity, [
            DbEntityKey.BASE, DbEntityKey.CLIMATE_ZONE,
            DbEntityKey.END_STATE_DEMOGRAPHIC, DbEntityKey.BASE_DEMOGRAPHIC])

        water_output_list = []

        options = dict(
            water_result_table=water_class.db_entity_key,
            water_schema=parse_schema_and_table(water_class._meta.db_table)[0],
            base_table=base_class.db_entity_key,
            base_schema=parse_schema_and_table(base_class._meta.db_table)[0],
        )

        for feature in annotated_features:

            base_feature = base_class.objects.get(id=feature.base_feature)
            climate_zone_feature = climate_zone_class.objects.filter(id=feature.climate_zones)
            if climate_zone_feature.exists():
                climate_zone_feature = climate_zone_feature[0]
            else:
                logger.warn("No Climate Zone intersection for feature id {0}".format(feature.id))
                continue

            demographic_feature = end_state_demographic_class.objects.get(id=feature.end_state_demographic_feature)
            base_demographic_feature = base_demographic_class.objects.get(id=feature.base_demographic_feature)

            water_input = dict(

                id=feature.id,

                evapotranspiration_zone=climate_zone_feature.evapotranspiration_zone.zone,
                annual_evapotranspiration=float(climate_zone_feature.evapotranspiration_zone.annual_evapotranspiration),

                pop=float(feature.pop),
                hh=float(feature.hh),
                emp=float(feature.emp),

                residential_irrigated_sqft_new=float(feature.residential_irrigated_sqft - base_feature.residential_irrigated_sqft)
                if feature.residential_irrigated_sqft - base_feature.residential_irrigated_sqft > 0 else 0,

                commercial_irrigated_sqft_new=float(feature.commercial_irrigated_sqft - base_feature.commercial_irrigated_sqft)
                if feature.commercial_irrigated_sqft - base_feature.commercial_irrigated_sqft > 0 else 0,

                du_detsf_ll_new=float((feature.du_detsf_ll - base_feature.du_detsf_ll) *
                    demographic_feature.du_occupancy_rate * demographic_feature.hh_avg_size)
                if feature.du_detsf_ll - base_feature.du_detsf_ll > 0 else 0,

                du_detsf_sl_new=float((feature.du_detsf_sl - base_feature.du_detsf_sl) *
                    demographic_feature.du_occupancy_rate * demographic_feature.hh_avg_size)
                if feature.du_detsf_sl -base_feature.du_detsf_sl > 0 else 0,

                du_attsf_new=float((feature.du_attsf - base_feature.du_attsf) * demographic_feature.du_occupancy_rate * \
                   demographic_feature.hh_avg_size) if feature.du_attsf - base_feature.du_attsf > 0 else 0,

                du_mf_new=float((feature.du_mf - base_feature.du_mf) * demographic_feature.du_occupancy_rate * \
                    demographic_feature.hh_avg_size) if feature.du_mf - base_feature.du_mf > 0 else 0,

                residential_irrigated_sqft_base=float(base_feature.residential_irrigated_sqft),

                commercial_irrigated_sqft_base=float(base_feature.commercial_irrigated_sqft),

                du_detsf_ll_base=float(base_feature.du_detsf_ll * base_demographic_feature.du_occupancy_rate * \
                                   base_demographic_feature.hh_avg_size),

                du_detsf_sl_base=float(base_feature.du_detsf_sl * base_demographic_feature.du_occupancy_rate * \
                                   base_demographic_feature.hh_avg_size),

                du_attsf_base=float(base_feature.du_attsf * base_demographic_feature.du_occupancy_rate * \
                                base_demographic_feature.hh_avg_size),

                du_mf_base=float(base_feature.du_mf * base_demographic_feature.du_occupancy_rate * \
                                base_demographic_feature.hh_avg_size),

                residential_irrigated_sqft_redev=float(math.fabs(feature.residential_irrigated_sqft - base_feature.residential_irrigated_sqft))
                if feature.residential_irrigated_sqft - base_feature.residential_irrigated_sqft < 0 else 0,

                commercial_irrigated_sqft_redev=float(math.fabs(feature.commercial_irrigated_sqft - base_feature.commercial_irrigated_sqft))
                if feature.commercial_irrigated_sqft - base_feature.commercial_irrigated_sqft < 0 else 0,

                du_detsf_ll_redev=float(math.fabs((feature.du_detsf_ll - base_feature.du_detsf_ll) *
                base_demographic_feature.du_occupancy_rate * base_demographic_feature.hh_avg_size))
                if feature.du_detsf_ll - base_feature.du_detsf_ll < 0 else 0,

                du_detsf_sl_redev=float(math.fabs((feature.du_detsf_sl - base_feature.du_detsf_sl) *
                base_demographic_feature.du_occupancy_rate * base_demographic_feature.hh_avg_size))
                if feature.du_detsf_sl - base_feature.du_detsf_sl < 0 else 0,

                du_attsf_redev=float(math.fabs((feature.du_attsf - base_feature.du_attsf) *
                base_demographic_feature.du_occupancy_rate * base_demographic_feature.hh_avg_size))
                if feature.du_attsf - base_feature.du_attsf < 0 else 0,

                du_mf_redev=float(math.fabs((feature.du_mf - base_feature.du_mf) *
                base_demographic_feature.du_occupancy_rate * base_demographic_feature.hh_avg_size))
                if feature.du_mf - base_feature.du_mf < 0 else 0,

                retail_services_new=float(feature.emp_retail_services - base_feature.emp_retail_services)
                if feature.emp_retail_services - base_feature.emp_retail_services > 0 else 0,

                restaurant_new=float(feature.emp_restaurant - base_feature.emp_restaurant)
                if feature.emp_restaurant - base_feature.emp_restaurant > 0 else 0,

                accommodation_new=float(feature.emp_accommodation - base_feature.emp_accommodation)
                if feature.emp_accommodation - base_feature.emp_accommodation > 0 else 0,

                arts_entertainment_new=float(feature.emp_arts_entertainment - base_feature.emp_arts_entertainment)
                if feature.emp_arts_entertainment - base_feature.emp_arts_entertainment > 0 else 0,

                other_services_new=float(feature.emp_other_services - base_feature.emp_other_services)
                if feature.emp_other_services - base_feature.emp_other_services > 0 else 0,

                office_services_new=float(feature.emp_office_services - base_feature.emp_office_services)
                if feature.emp_office_services - base_feature.emp_office_services > 0 else 0,

                public_admin_new=float(feature.emp_public_admin - base_feature.emp_public_admin)
                if feature.emp_public_admin - base_feature.emp_public_admin > 0 else 0,

                education_new=float(feature.emp_education - base_feature.emp_education)
                if feature.emp_education - base_feature.emp_education > 0 else 0,

                medical_services_new=float(feature.emp_medical_services - base_feature.emp_medical_services)
                if feature.emp_medical_services - base_feature.emp_medical_services > 0 else 0,

                wholesale_new=float(feature.emp_wholesale - base_feature.emp_wholesale)
                if feature.emp_wholesale - base_feature.emp_wholesale > 0 else 0,

                transport_warehousing_new=float(feature.emp_transport_warehousing - base_feature.emp_transport_warehousing)
                if feature.emp_transport_warehousing - base_feature.emp_transport_warehousing > 0 else 0,

                manufacturing_new=float(math.fabs(feature.emp_manufacturing - base_feature.emp_manufacturing))
                if feature.emp_manufacturing - base_feature.emp_manufacturing > 0 else 0,

                construction_new=float(math.fabs(feature.emp_construction - base_feature.emp_construction))
                if feature.emp_construction - base_feature.emp_construction > 0 else 0,

                utilities_new=float(math.fabs(feature.emp_utilities - base_feature.emp_utilities))
                if feature.emp_utilities - base_feature.emp_utilities > 0 else 0,

                agriculture_new=float(math.fabs(feature.emp_agriculture - base_feature.emp_agriculture))
                if feature.emp_agriculture - base_feature.emp_agriculture > 0 else 0,

                extraction_new=float(math.fabs(feature.emp_extraction - base_feature.emp_extraction))
                if feature.emp_extraction - base_feature.emp_extraction > 0 else 0,

                military_new=float(math.fabs(feature.emp_military - base_feature.emp_military))
                if feature.emp_military - base_feature.emp_military > 0 else 0,

                retail_services_base=float(base_feature.emp_retail_services),

                restaurant_base=float(base_feature.emp_restaurant),

                accommodation_base=float(base_feature.emp_accommodation),

                arts_entertainment_base=float(base_feature.emp_arts_entertainment),

                other_services_base=float(base_feature.emp_other_services),

                office_services_base=float(base_feature.emp_office_services),

                public_admin_base=float(base_feature.emp_public_admin),

                education_base=float(base_feature.emp_education),

                medical_services_base=float(base_feature.emp_medical_services),

                wholesale_base=float(base_feature.emp_wholesale),

                transport_warehousing_base=float(base_feature.emp_transport_warehousing),

                manufacturing_base=float(base_feature.emp_manufacturing),

                construction_base=float(base_feature.emp_construction),

                utilities_base=float(base_feature.emp_utilities),

                agriculture_base=float(base_feature.emp_agriculture),

                extraction_base=float(base_feature.emp_extraction),

                military_base=float(base_feature.emp_military),

                retail_services_redev=float(math.fabs(feature.emp_retail_services - base_feature.emp_retail_services))
                if feature.emp_retail_services - base_feature.emp_retail_services < 0 else 0,

                restaurant_redev=float(math.fabs(feature.emp_restaurant - base_feature.emp_restaurant))
                if feature.emp_restaurant - base_feature.emp_restaurant < 0 else 0,

                accommodation_redev=float(math.fabs(feature.emp_accommodation - base_feature.emp_accommodation))
                if feature.emp_accommodation - base_feature.emp_accommodation < 0 else 0,

                arts_entertainment_redev=float(math.fabs(feature.emp_arts_entertainment - base_feature.emp_arts_entertainment))
                if feature.emp_arts_entertainment - base_feature.emp_arts_entertainment < 0 else 0,

                other_services_redev=float(math.fabs(feature.emp_other_services - base_feature.emp_other_services))
                if feature.emp_other_services - base_feature.emp_other_services < 0 else 0,

                office_services_redev=float(math.fabs(feature.emp_office_services - base_feature.emp_office_services))
                if feature.emp_office_services - base_feature.emp_office_services < 0 else 0,

                public_admin_redev=float(math.fabs(feature.emp_public_admin - base_feature.emp_public_admin))
                if feature.emp_public_admin - base_feature.emp_public_admin < 0 else 0,

                education_redev=float(math.fabs(feature.emp_education - base_feature.emp_education))
                if feature.emp_education - base_feature.emp_education < 0 else 0,

                medical_services_redev=float(math.fabs(feature.emp_medical_services - base_feature.emp_medical_services))
                if feature.emp_medical_services - base_feature.emp_medical_services < 0 else 0,

                wholesale_redev=float(math.fabs(feature.emp_wholesale - base_feature.emp_wholesale))
                if feature.emp_wholesale - base_feature.emp_wholesale < 0 else 0,

                transport_warehousing_redev=float(math.fabs(feature.emp_transport_warehousing - base_feature.emp_transport_warehousing))
                if feature.emp_transport_warehousing - base_feature.emp_transport_warehousing < 0 else 0,

                manufacturing_redev=float(math.fabs(feature.emp_manufacturing - base_feature.emp_manufacturing))
                if feature.emp_manufacturing - base_feature.emp_manufacturing < 0 else 0,

                construction_redev=float(math.fabs(feature.emp_construction - base_feature.emp_construction))
                if feature.emp_construction - base_feature.emp_construction < 0 else 0,

                utilities_redev=float(math.fabs(feature.emp_utilities - base_feature.emp_utilities))
                if feature.emp_utilities - base_feature.emp_utilities < 0 else 0,

                agriculture_redev=float(math.fabs(feature.emp_agriculture - base_feature.emp_agriculture))
                if feature.emp_agriculture - base_feature.emp_agriculture < 0 else 0,

                extraction_redev=float(math.fabs(feature.emp_extraction - base_feature.emp_extraction))
                if feature.emp_extraction - base_feature.emp_extraction < 0 else 0,

                military_redev=float(math.fabs(feature.emp_military - base_feature.emp_military))
                if feature.emp_military - base_feature.emp_military < 0 else 0,
            )

            water_output = calculate_future_water(water_input, policy_assumptions, configuration)

            output_row = map(lambda key: water_output[key], WATER_OUTPUT_FIELDS)
            water_output_list.append(output_row)

        return water_output_list, options


    def run_base_water_calculations(self):

        policy_assumptions = FormatPolicyInputs(self.config_entity)

        water_class = self.config_entity.db_entity_feature_class(DbEntityKey.WATER)

        base_class = self.config_entity.db_entity_feature_class(DbEntityKey.BASE)
        base_demographic_class = self.config_entity.db_entity_feature_class(DbEntityKey.BASE_DEMOGRAPHIC)
        climate_zone_class = self.config_entity.db_entity_feature_class(DbEntityKey.CLIMATE_ZONE)

        features = base_class.objects.all()

        annotated_features = annotated_related_feature_class_pk_via_geographies(features, self.config_entity, [
            DbEntityKey.CLIMATE_ZONE, DbEntityKey.BASE_DEMOGRAPHIC])

        water_output_list = []

        options = dict(
            water_result_table=water_class.db_entity_key,
            water_schema=parse_schema_and_table(water_class._meta.db_table)[0],
            base_table=base_class.db_entity_key,
            base_schema=parse_schema_and_table(base_class._meta.db_table)[0],
        )

        for feature in annotated_features:
            climate_zone_feature = climate_zone_class.objects.filter(id=feature.climate_zones)

            if climate_zone_feature.exists():
                climate_zone_feature = climate_zone_feature[0]
            else:
                logger.warn("No Climate Zone intersection for feature id {0}".format(feature.id))
                continue

            base_demographic_feature = base_demographic_class.objects.get(id=feature.base_demographic_feature)

            water_input = dict(

                id=feature.id,

                evapotranspiration_zone=climate_zone_feature.evapotranspiration_zone.zone,
                annual_evapotranspiration=float(climate_zone_feature.evapotranspiration_zone.annual_evapotranspiration),

                pop=float(feature.pop),
                hh=float(feature.hh),
                emp=float(feature.emp),

                residential_irrigated_sqft=float(feature.residential_irrigated_sqft),
                commercial_irrigated_sqft=float(feature.commercial_irrigated_sqft),

                du_detsf_ll=float(feature.du_detsf_ll * base_demographic_feature.du_occupancy_rate * \
                                  base_demographic_feature.hh_avg_size),
                du_detsf_sl=float(feature.du_detsf_sl * base_demographic_feature.du_occupancy_rate * \
                                  base_demographic_feature.hh_avg_size),
                du_attsf=float(feature.du_attsf * base_demographic_feature.du_occupancy_rate * \
                               base_demographic_feature.hh_avg_size),
                du_mf=float(feature.du_mf * base_demographic_feature.du_occupancy_rate * \
                            base_demographic_feature.hh_avg_size),

                retail_services=float(feature.emp_retail_services),
                restaurant=float(feature.emp_restaurant),
                accommodation=float(feature.emp_accommodation),
                arts_entertainment=float(feature.emp_arts_entertainment),
                other_services=float(feature.emp_other_services),
                office_services=float(feature.emp_office_services),
                public_admin=float(feature.emp_public_admin),
                education=float(feature.emp_education),
                medical_services=float(feature.emp_medical_services),
                wholesale=float(feature.emp_wholesale),
                transport_warehousing=float(feature.emp_transport_warehousing),
                manufacturing=float(feature.emp_manufacturing),
                construction=float(feature.emp_construction),
                utilities=float(feature.emp_utilities),
                agriculture=float(feature.emp_agriculture),
                extraction=float(feature.emp_extraction),
                military=float(feature.emp_military)
            )

            water_output = calculate_base_water(water_input, policy_assumptions)

            output_row = map(lambda key: water_output[key], WATER_OUTPUT_FIELDS)
            water_output_list.append(output_row)

        return water_output_list, options


    def run_water_calculations(self, **kwargs):

        start_time = time.time()

        if isinstance(self.config_entity.subclassed_config_entity, FutureScenario):
            self.water_progress(0.3, **kwargs)
            water_output_list, options = self.run_future_water_calculations()
            self.water_progress(0.5, **kwargs)
        else:
            self.water_progress(0.3, **kwargs)
            water_output_list, options = self.run_base_water_calculations()
            self.water_progress(0.5, **kwargs)

        write_water_results_to_database(options, water_output_list)
        self.water_progress(0.2, **kwargs)


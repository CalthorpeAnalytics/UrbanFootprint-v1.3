import time
import math
from django.db import models
from footprint.common.utils.websockets import send_message_to_client
from footprint.main.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.main.models.analysis_module.analysis_tool import AnalysisTool
from footprint.main.models.analysis_module.energy_module.energy_calculate_base import calculate_base_energy
from footprint.main.models.analysis_module.energy_module.energy_calculate_future import calculate_future_energy
from footprint.main.models.analysis_module.energy_module.energy_format_policy_inputs import FormatPolicyInputs
from footprint.main.models.analysis_module.energy_module.energy_keys import ENERGY_OUTPUT_FIELDS
from footprint.main.models.analysis_module.energy_module.write_energy_results_to_database import write_energy_results_to_database
from footprint.main.models.config.scenario import FutureScenario
import logging
from footprint.main.models.geospatial.db_entity_keys import DbEntityKey
from footprint.main.utils.query_parsing import annotated_related_feature_class_pk_via_geographies
from footprint.main.utils.utils import parse_schema_and_table

__author__ = 'calthorpe_associates'


logger = logging.getLogger(__name__)

class EnergyUpdaterTool(AnalysisTool):

    objects = GeoInheritanceManager()

    class Meta(object):
        app_label = 'main'
        abstract = False


    def energy_progress(self, proportion, **kwargs):
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

        logger.info("Executing Energy using {0}".format(self.config_entity))

        self.run_energy_calculations(**kwargs)

        logger.info("Done executing Energy")
        logger.info("Executed Energy using {0}".format(self.config_entity))


    def run_future_energy_calculations(self):

        policy_assumptions = FormatPolicyInputs(self.config_entity)

        configuration = dict(
            time_increment=float(self.config_entity.scenario.year - self.config_entity.scenario.project.base_year),
            base_year=float(self.config_entity.scenario.project.base_year),
            future_year=float(self.config_entity.scenario.year)
        )

        energy_class = self.config_entity.db_entity_feature_class(DbEntityKey.ENERGY)

        end_state_class = self.config_entity.db_entity_feature_class(DbEntityKey.END_STATE)
        end_state_demographic_class = self.config_entity.db_entity_feature_class(DbEntityKey.END_STATE_DEMOGRAPHIC)
        base_class = self.config_entity.db_entity_feature_class(DbEntityKey.BASE)
        base_demographic_class = self.config_entity.db_entity_feature_class(DbEntityKey.BASE_DEMOGRAPHIC)
        climate_zone_class = self.config_entity.db_entity_feature_class(DbEntityKey.CLIMATE_ZONE)

        features = end_state_class.objects.all()

        annotated_features = annotated_related_feature_class_pk_via_geographies(features, self.config_entity, [
            DbEntityKey.BASE, DbEntityKey.CLIMATE_ZONE,
            DbEntityKey.END_STATE_DEMOGRAPHIC, DbEntityKey.BASE_DEMOGRAPHIC])

        energy_output_list = []

        options = dict(
            energy_result_table=energy_class.db_entity_key,
            energy_schema=parse_schema_and_table(energy_class._meta.db_table)[0],
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

            energy_input = dict(

                id=feature.id,
                du_detsf_ll_new=float((feature.du_detsf_ll - base_feature.du_detsf_ll) *
                demographic_feature.du_occupancy_rate) if feature.du_detsf_ll - base_feature.du_detsf_ll > 0 else 0,
                du_detsf_sl_new=float((feature.du_detsf_sl - base_feature.du_detsf_sl) *
                demographic_feature.du_occupancy_rate) if feature.du_detsf_sl -base_feature.du_detsf_sl > 0 else 0,
                du_attsf_new=float((feature.du_attsf - base_feature.du_attsf) * demographic_feature.du_occupancy_rate)
                if feature.du_attsf - base_feature.du_attsf > 0 else 0,
                du_mf_new=float((feature.du_mf - base_feature.du_mf) * demographic_feature.du_occupancy_rate)
                if feature.du_mf - base_feature.du_mf > 0 else 0,

                du_detsf_ll_base=float(base_feature.du_detsf_ll * base_demographic_feature.du_occupancy_rate),

                du_detsf_sl_base=float(base_feature.du_detsf_sl * base_demographic_feature.du_occupancy_rate),

                du_attsf_base=float(base_feature.du_attsf * base_demographic_feature.du_occupancy_rate),

                du_mf_base=float(base_feature.du_mf * base_demographic_feature.du_occupancy_rate),

                du_detsf_ll_redev=float(math.fabs((feature.du_detsf_ll - base_feature.du_detsf_ll) *
                base_demographic_feature.du_occupancy_rate)) if feature.du_detsf_ll - base_feature.du_detsf_ll < 0 else 0,

                du_detsf_sl_redev=float(math.fabs((feature.du_detsf_sl - base_feature.du_detsf_sl) *
                base_demographic_feature.du_occupancy_rate)) if feature.du_detsf_sl - base_feature.du_detsf_sl < 0 else 0,

                du_attsf_redev=float(math.fabs((feature.du_attsf - base_feature.du_attsf) *
                base_demographic_feature.du_occupancy_rate)) if feature.du_attsf - base_feature.du_attsf < 0 else 0,

                du_mf_redev=float(math.fabs((feature.du_mf - base_feature.du_mf) *
                base_demographic_feature.du_occupancy_rate)) if feature.du_mf - base_feature.du_mf < 0 else 0,

                hh=feature.hh,

                emp=feature.emp,

                total_commercial_sqft=float(feature.bldg_sqft_retail_services) + float(feature.bldg_sqft_restaurant) + \
                float(feature.bldg_sqft_accommodation) + float(feature.bldg_sqft_arts_entertainment) + \
                float(feature.bldg_sqft_other_services) + float(feature.bldg_sqft_office_services) + \
                float(feature.bldg_sqft_public_admin) + float(feature.bldg_sqft_education) + \
                float(feature.bldg_sqft_medical_services) + float(feature.bldg_sqft_wholesale) + \
                float(feature.bldg_sqft_transport_warehousing),

                retail_services_new=float(feature.bldg_sqft_retail_services - base_feature.bldg_sqft_retail_services)
                if feature.bldg_sqft_retail_services - base_feature.bldg_sqft_retail_services > 0 else 0,

                restaurant_new=float(feature.bldg_sqft_restaurant - base_feature.bldg_sqft_restaurant)
                if feature.bldg_sqft_restaurant - base_feature.bldg_sqft_restaurant > 0 else 0,

                accommodation_new=float(feature.bldg_sqft_accommodation - base_feature.bldg_sqft_accommodation)
                if feature.bldg_sqft_accommodation - base_feature.bldg_sqft_accommodation > 0 else 0,

                arts_entertainment_new=float(feature.bldg_sqft_arts_entertainment - base_feature.bldg_sqft_arts_entertainment)
                if feature.bldg_sqft_arts_entertainment - base_feature.bldg_sqft_arts_entertainment > 0 else 0,

                other_services_new=float(feature.bldg_sqft_other_services - base_feature.bldg_sqft_other_services)
                if feature.bldg_sqft_other_services - base_feature.bldg_sqft_other_services > 0 else 0,

                office_services_new=float(feature.bldg_sqft_office_services - base_feature.bldg_sqft_office_services)
                if feature.bldg_sqft_office_services - base_feature.bldg_sqft_office_services > 0 else 0,

                public_admin_new=float(feature.bldg_sqft_public_admin - base_feature.bldg_sqft_public_admin)
                if feature.bldg_sqft_public_admin - base_feature.bldg_sqft_public_admin > 0 else 0,

                education_new=float(feature.bldg_sqft_education - base_feature.bldg_sqft_education)
                if feature.bldg_sqft_education - base_feature.bldg_sqft_education > 0 else 0,

                medical_services_new=float(feature.bldg_sqft_medical_services - base_feature.bldg_sqft_medical_services)
                if feature.bldg_sqft_medical_services - base_feature.bldg_sqft_medical_services > 0 else 0,

                wholesale_new=float(feature.bldg_sqft_wholesale - base_feature.bldg_sqft_wholesale)
                if feature.bldg_sqft_wholesale - base_feature.bldg_sqft_wholesale > 0 else 0,

                transport_warehousing_new=float(feature.bldg_sqft_transport_warehousing - base_feature.bldg_sqft_transport_warehousing)
                if feature.bldg_sqft_transport_warehousing - base_feature.bldg_sqft_transport_warehousing > 0 else 0,

                retail_services_base=float(base_feature.bldg_sqft_retail_services),

                restaurant_base=float(base_feature.bldg_sqft_restaurant),

                accommodation_base=float(base_feature.bldg_sqft_accommodation),

                arts_entertainment_base=float(base_feature.bldg_sqft_arts_entertainment),

                other_services_base=float(base_feature.bldg_sqft_other_services),

                office_services_base=float(base_feature.bldg_sqft_office_services),

                public_admin_base=float(base_feature.bldg_sqft_public_admin),

                education_base=float(base_feature.bldg_sqft_education),

                medical_services_base=float(base_feature.bldg_sqft_medical_services),

                wholesale_base=float(base_feature.bldg_sqft_wholesale),

                transport_warehousing_base=float(base_feature.bldg_sqft_transport_warehousing),

                retail_services_redev=float(math.fabs(feature.bldg_sqft_retail_services - base_feature.bldg_sqft_retail_services))
                if feature.bldg_sqft_retail_services - base_feature.bldg_sqft_retail_services < 0 else 0,

                restaurant_redev=float(math.fabs(feature.bldg_sqft_restaurant - base_feature.bldg_sqft_restaurant))
                if feature.bldg_sqft_restaurant - base_feature.bldg_sqft_restaurant < 0 else 0,

                accommodation_redev=float(math.fabs(feature.bldg_sqft_accommodation - base_feature.bldg_sqft_accommodation))
                if feature.bldg_sqft_accommodation - base_feature.bldg_sqft_accommodation < 0 else 0,

                arts_entertainment_redev=float(math.fabs(feature.bldg_sqft_arts_entertainment - base_feature.bldg_sqft_arts_entertainment))
                if feature.bldg_sqft_arts_entertainment - base_feature.bldg_sqft_arts_entertainment < 0 else 0,

                other_services_redev=float(math.fabs(feature.bldg_sqft_other_services - base_feature.bldg_sqft_other_services))
                if feature.bldg_sqft_other_services - base_feature.bldg_sqft_other_services < 0 else 0,

                office_services_redev=float(math.fabs(feature.bldg_sqft_office_services - base_feature.bldg_sqft_office_services))
                if feature.bldg_sqft_office_services - base_feature.bldg_sqft_office_services < 0 else 0,

                public_admin_redev=float(math.fabs(feature.bldg_sqft_public_admin - base_feature.bldg_sqft_public_admin))
                if feature.bldg_sqft_public_admin - base_feature.bldg_sqft_public_admin < 0 else 0,

                education_redev=float(math.fabs(feature.bldg_sqft_education - base_feature.bldg_sqft_education))
                if feature.bldg_sqft_education - base_feature.bldg_sqft_education < 0 else 0,

                medical_services_redev=float(math.fabs(feature.bldg_sqft_medical_services - base_feature.bldg_sqft_medical_services))
                if feature.bldg_sqft_medical_services - base_feature.bldg_sqft_medical_services < 0 else 0,

                wholesale_redev=float(math.fabs(feature.bldg_sqft_wholesale - base_feature.bldg_sqft_wholesale))
                if feature.bldg_sqft_wholesale - base_feature.bldg_sqft_wholesale < 0 else 0,

                transport_warehousing_redev=float(math.fabs(feature.bldg_sqft_transport_warehousing - base_feature.bldg_sqft_transport_warehousing))
                if feature.bldg_sqft_transport_warehousing - base_feature.bldg_sqft_transport_warehousing < 0 else 0,

                title24_zone=climate_zone_feature.title_24_zone.zone,
                fcz_zone=climate_zone_feature.forecasting_climate_zone.zone,

                du_detsf_ll_gas=float(climate_zone_feature.title_24_zone.du_detsf_ll_gas),

                du_detsf_sl_gas=float(climate_zone_feature.title_24_zone.du_detsf_sl_gas),

                du_attsf_gas=float(climate_zone_feature.title_24_zone.du_attsf_gas),

                du_mf_gas=float(climate_zone_feature.title_24_zone.du_mf_gas),

                retail_services_gas=float(climate_zone_feature.forecasting_climate_zone.retail_services_gas),

                restaurant_gas=float(climate_zone_feature.forecasting_climate_zone.restaurant_gas),

                accommodation_gas=float(climate_zone_feature.forecasting_climate_zone.accommodation_gas),

                arts_entertainment_gas=float(climate_zone_feature.forecasting_climate_zone.arts_entertainment_gas),

                other_services_gas=float(climate_zone_feature.forecasting_climate_zone.other_services_gas),

                office_services_gas=float(climate_zone_feature.forecasting_climate_zone.office_services_gas),

                public_admin_gas=float(climate_zone_feature.forecasting_climate_zone.public_admin_gas),

                education_gas=float(climate_zone_feature.forecasting_climate_zone.education_gas),

                medical_services_gas=float(climate_zone_feature.forecasting_climate_zone.medical_services_gas),

                wholesale_gas=float(climate_zone_feature.forecasting_climate_zone.wholesale_gas),

                transport_warehousing_gas=float(climate_zone_feature.forecasting_climate_zone.transport_warehousing_gas),

                du_detsf_ll_electricity=float(climate_zone_feature.title_24_zone.du_detsf_ll_electricity),

                du_detsf_sl_electricity=float(climate_zone_feature.title_24_zone.du_detsf_sl_electricity),

                du_attsf_electricity=float(climate_zone_feature.title_24_zone.du_attsf_electricity),

                du_mf_electricity=float(climate_zone_feature.title_24_zone.du_mf_electricity),

                retail_services_electricity=float(climate_zone_feature.forecasting_climate_zone.retail_services_electricity),

                restaurant_electricity=float(climate_zone_feature.forecasting_climate_zone.restaurant_electricity),

                accommodation_electricity=float(climate_zone_feature.forecasting_climate_zone.accommodation_electricity),

                arts_entertainment_electricity=float(climate_zone_feature.forecasting_climate_zone.arts_entertainment_electricity),

                other_services_electricity=float(climate_zone_feature.forecasting_climate_zone.other_services_electricity),

                office_services_electricity=float(climate_zone_feature.forecasting_climate_zone.office_services_electricity),

                public_admin_electricity=float(climate_zone_feature.forecasting_climate_zone.public_admin_electricity),

                education_electricity=float(climate_zone_feature.forecasting_climate_zone.education_electricity),

                medical_services_electricity=float(climate_zone_feature.forecasting_climate_zone.medical_services_electricity),

                wholesale_electricity=float(climate_zone_feature.forecasting_climate_zone.wholesale_electricity),

                transport_warehousing_electricity=float(climate_zone_feature.forecasting_climate_zone.transport_warehousing_electricity)

            )

            energy_output = calculate_future_energy(energy_input, policy_assumptions, configuration)

            output_row = map(lambda key: energy_output[key], ENERGY_OUTPUT_FIELDS)
            energy_output_list.append(output_row)

        return energy_output_list, options



    def run_base_energy_calculations(self):

        energy_class = self.config_entity.db_entity_feature_class(DbEntityKey.ENERGY)

        base_class = self.config_entity.db_entity_feature_class(DbEntityKey.BASE)
        base_demographic_class = self.config_entity.db_entity_feature_class(DbEntityKey.BASE_DEMOGRAPHIC)
        climate_zone_class = self.config_entity.db_entity_feature_class(DbEntityKey.CLIMATE_ZONE)

        features = base_class.objects.all()

        annotated_features = annotated_related_feature_class_pk_via_geographies(features, self.config_entity, [
            DbEntityKey.CLIMATE_ZONE, DbEntityKey.BASE_DEMOGRAPHIC])

        energy_output_list = []

        options = dict(
            energy_result_table=energy_class.db_entity_key,
            energy_schema=parse_schema_and_table(energy_class._meta.db_table)[0],
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

            energy_input = dict(

                id = feature.id,

                title24_zone=climate_zone_feature.title_24_zone.zone,
                fcz_zone=climate_zone_feature.forecasting_climate_zone.zone,

                hh=feature.hh,

                emp=feature.emp,

                total_commercial_sqft=float(feature.bldg_sqft_retail_services) + float(feature.bldg_sqft_restaurant) + \
                float(feature.bldg_sqft_accommodation) + float(feature.bldg_sqft_arts_entertainment) + \
                float(feature.bldg_sqft_other_services) + float(feature.bldg_sqft_office_services) + \
                float(feature.bldg_sqft_public_admin) + float(feature.bldg_sqft_education) + \
                float(feature.bldg_sqft_medical_services) + float(feature.bldg_sqft_wholesale) + \
                float(feature.bldg_sqft_transport_warehousing),

                du_detsf_ll=float(feature.du_detsf_ll * base_demographic_feature.du_occupancy_rate),

                du_detsf_sl=float(feature.du_detsf_sl * base_demographic_feature.du_occupancy_rate),

                du_attsf=float(feature.du_attsf * base_demographic_feature.du_occupancy_rate),

                du_mf=float(feature.du_mf * base_demographic_feature.du_occupancy_rate),

                retail_services=float(feature.bldg_sqft_retail_services),

                restaurant=float(feature.bldg_sqft_restaurant),

                accommodation=float(feature.bldg_sqft_accommodation),

                arts_entertainment=float(feature.bldg_sqft_arts_entertainment),

                other_services=float(feature.bldg_sqft_other_services),

                office_services=float(feature.bldg_sqft_office_services),

                public_admin=float(feature.bldg_sqft_public_admin),

                education=float(feature.bldg_sqft_education),

                medical_services=float(feature.bldg_sqft_medical_services),

                wholesale=float(feature.bldg_sqft_wholesale),

                transport_warehousing=float(feature.bldg_sqft_transport_warehousing),

                du_detsf_ll_gas=float(climate_zone_feature.title_24_zone.du_detsf_ll_gas),

                du_detsf_sl_gas=float(climate_zone_feature.title_24_zone.du_detsf_sl_gas),

                du_attsf_gas=float(climate_zone_feature.title_24_zone.du_attsf_gas),

                du_mf_gas=float(climate_zone_feature.title_24_zone.du_mf_gas),

                retail_services_gas=float(climate_zone_feature.forecasting_climate_zone.retail_services_gas),

                restaurant_gas=float(climate_zone_feature.forecasting_climate_zone.restaurant_gas),

                accommodation_gas=float(climate_zone_feature.forecasting_climate_zone.accommodation_gas),

                arts_entertainment_gas=float(climate_zone_feature.forecasting_climate_zone.arts_entertainment_gas),

                other_services_gas=float(climate_zone_feature.forecasting_climate_zone.other_services_gas),

                office_services_gas=float(climate_zone_feature.forecasting_climate_zone.office_services_gas),

                public_admin_gas=float(climate_zone_feature.forecasting_climate_zone.public_admin_gas),

                education_gas=float(climate_zone_feature.forecasting_climate_zone.education_gas),

                medical_services_gas=float(climate_zone_feature.forecasting_climate_zone.medical_services_gas),

                wholesale_gas=float(climate_zone_feature.forecasting_climate_zone.wholesale_gas),

                transport_warehousing_gas=float(climate_zone_feature.forecasting_climate_zone.transport_warehousing_gas),

                du_detsf_ll_electricity=float(climate_zone_feature.title_24_zone.du_detsf_ll_electricity),

                du_detsf_sl_electricity=float(climate_zone_feature.title_24_zone.du_detsf_sl_electricity),

                du_attsf_electricity=float(climate_zone_feature.title_24_zone.du_attsf_electricity),

                du_mf_electricity=float(climate_zone_feature.title_24_zone.du_mf_electricity),

                retail_services_electricity=float(climate_zone_feature.forecasting_climate_zone.retail_services_electricity),

                restaurant_electricity=float(climate_zone_feature.forecasting_climate_zone.restaurant_electricity),

                accommodation_electricity=float(climate_zone_feature.forecasting_climate_zone.accommodation_electricity),

                arts_entertainment_electricity=float(climate_zone_feature.forecasting_climate_zone.arts_entertainment_electricity),

                other_services_electricity=float(climate_zone_feature.forecasting_climate_zone.other_services_electricity),

                office_services_electricity=float(climate_zone_feature.forecasting_climate_zone.office_services_electricity),

                public_admin_electricity=float(climate_zone_feature.forecasting_climate_zone.public_admin_electricity),

                education_electricity=float(climate_zone_feature.forecasting_climate_zone.education_electricity),

                medical_services_electricity=float(climate_zone_feature.forecasting_climate_zone.medical_services_electricity),

                wholesale_electricity=float(climate_zone_feature.forecasting_climate_zone.wholesale_electricity),

                transport_warehousing_electricity=float(climate_zone_feature.forecasting_climate_zone.transport_warehousing_electricity)
            )

            energy_output = calculate_base_energy(energy_input)

            output_row = map(lambda key: energy_output[key], ENERGY_OUTPUT_FIELDS)
            energy_output_list.append(output_row)

        return energy_output_list, options



    def run_energy_calculations(self, **kwargs):

        start_time = time.time()

        if isinstance(self.config_entity.subclassed_config_entity, FutureScenario):
            self.energy_progress(0.3, **kwargs)
            energy_output_list,options = self.run_future_energy_calculations()
            self.energy_progress(0.5, **kwargs)
        else:
            self.energy_progress(0.3, **kwargs)
            energy_output_list,options = self.run_base_energy_calculations()
            self.energy_progress(0.5, **kwargs)

        write_energy_results_to_database(options, energy_output_list)
        self.energy_progress(0.2, **kwargs)

        print 'Finished: ' + str(time.time() - start_time)

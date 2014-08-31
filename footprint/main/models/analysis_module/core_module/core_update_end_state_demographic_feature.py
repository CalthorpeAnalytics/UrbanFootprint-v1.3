import logging
from footprint.main.models.analysis_module.core_module.core_revert_to_base_condition import core_demographic_revert_to_base_condition
from footprint.main.models.geospatial.db_entity_keys import DbEntityKey

__author__ = 'calthorpe'

logger = logging.getLogger(__name__)

def update_end_state_demographic_feature(config_entity, annotated_features):
    end_state_demographic_class = config_entity.db_entity_feature_class(DbEntityKey.END_STATE_DEMOGRAPHIC)
    base_demographic_class = config_entity.db_entity_feature_class(DbEntityKey.BASE_DEMOGRAPHIC)
    census_block_class = config_entity.db_entity_feature_class(DbEntityKey.CENSUS_BLOCK)
   
    for feature in annotated_features:

        try:
            census_block = census_block_class.objects.get(id=feature.census_block)
        except:
            continue
        demographic = end_state_demographic_class.objects.get(id=feature.end_state_demographic_feature)
        base_demographic = base_demographic_class.objects.get(id=feature.base_demographic_feature)


        if not feature.built_form_base:
            # If the user reverted the built_form, it will be null and we need to set it to the base built_form
            core_demographic_revert_to_base_condition(demographic, base_demographic)
            continue

        demographic.du_occupancy_rate = feature.hh / feature.du if feature.du > 0 else 0
        demographic.pop_male = feature.pop * census_block.pop_male_rate
        demographic.pop_female = feature.pop * census_block.pop_female_rate

        demographic.pop_female_age20_64 = feature.pop * census_block.pop_female_age20_64_rate
        demographic.pop_male_age20_64 = feature.pop * census_block.pop_male_age20_64_rate
        demographic.pop_age16_up = feature.pop * census_block.pop_age16_up_rate
        demographic.pop_age25_up = feature.pop * census_block.pop_age25_up_rate
        demographic.pop_age65_up = feature.pop * census_block.pop_age65_up_rate
        
        demographic.pop_age20_64 = feature.pop * (census_block.pop_female_age20_64_rate +
                                                  census_block.pop_female_age20_64_rate)
        
        demographic.pop_hs_not_comp = feature.pop * census_block.pop_hs_not_comp_rate
        demographic.pop_hs_diploma = feature.pop * census_block.pop_hs_diploma_rate
        demographic.pop_some_college = feature.pop * census_block.pop_assoc_some_coll_rate
        demographic.pop_college_degree = feature.pop * census_block.pop_coll_degree_rate
        demographic.pop_graduate_degree = feature.pop * census_block.pop_grad_degree_rate
        demographic.pop_employed = feature.pop * census_block.pop_employed_rate
        demographic.hh_inc_00_10 = feature.hh * census_block.hh_inc_00_10_rate
        demographic.hh_inc_10_20 = feature.hh * census_block.hh_inc_10_20_rate
        demographic.hh_inc_20_30 = feature.hh * census_block.hh_inc_20_30_rate
        demographic.hh_inc_30_40 = feature.hh * census_block.hh_inc_30_40_rate
        demographic.hh_inc_40_50 = feature.hh * census_block.hh_inc_40_50_rate
        demographic.hh_inc_50_60 = feature.hh * census_block.hh_inc_50_60_rate
        demographic.hh_inc_60_75 = feature.hh * census_block.hh_inc_60_75_rate
        demographic.hh_inc_75_100 = feature.hh * census_block.hh_inc_75_100_rate
        demographic.hh_inc_100_125 = feature.hh * census_block.hh_inc_100_125_rate
        demographic.hh_inc_125_150 = feature.hh * census_block.hh_inc_125_150_rate
        demographic.hh_inc_150_200 = feature.hh * census_block.hh_inc_150_200_rate
        demographic.hh_inc_200p = feature.hh * census_block.hh_inc_200p_rate
        demographic.hh_avg_vehicles = census_block.hh_agg_veh_rate

        demographic.hh_avg_size = feature.pop / feature.hh if feature.hh > 0 else 0
        demographic.hh_agg_inc = feature.hh * census_block.hh_agg_inc_rate
        demographic.hh_avg_inc = census_block.hh_agg_inc_rate
        demographic.hh_owner_occ = feature.hh * census_block.hh_own_occ_rate
        demographic.hh_rental_occ = feature.hh * census_block.hh_rent_occ_rate

        demographic.save()

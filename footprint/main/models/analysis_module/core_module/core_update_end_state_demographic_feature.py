from footprint.main.models.keys.keys import Keys
from footprint.main.utils.query_parsing import annotated_related_feature_class_pk_via_geographies

__author__ = 'calthorpe'


def update_end_state_demographic_feature(config_entity):
    end_state_class = config_entity.feature_class_of_db_entity_key(Keys.DB_ABSTRACT_END_STATE_FEATURE)
    end_state_demographic_class = config_entity.feature_class_of_db_entity_key(Keys.DB_ABSTRACT_END_STATE_DEMOGRAPHIC_FEATURE)
    census_block_class = config_entity.feature_class_of_db_entity_key(Keys.DB_ABSTRACT_CENSUS_BLOCK)
   
    future_scenario_class = config_entity.feature_class_of_db_entity_key(Keys.DB_ABSTRACT_FUTURE_SCENARIO_FEATURE)

    feature = future_scenario_class.objects.filter(dirty_flag=True)

    annotated_features = annotated_related_feature_class_pk_via_geographies(feature, config_entity, [Keys.DB_ABSTRACT_END_STATE_DEMOGRAPHIC_FEATURE, Keys.DB_ABSTRACT_CENSUS_BLOCK, Keys.DB_ABSTRACT_END_STATE_FEATURE])

    for feature in annotated_features:

        demographic = end_state_demographic_class.objects.get(id=feature.end_state_demographic_feature)
        census_block = census_block_class.objects.get(id=feature.census_block)
        end_state = end_state_class.objects.get(id=feature.end_state)

        demographic.du_occupancy_rate = end_state.hh / end_state.du if end_state.du > 0 else 0
        demographic.pop_male = end_state.pop * census_block.pop_male_rate
        demographic.pop_female = end_state.pop * census_block.pop_female_rate

        demographic.pop_female_age20_64 = end_state.pop * census_block.pop_female_age20_64_rate
        demographic.pop_male_age20_64 = end_state.pop * census_block.pop_male_age20_64_rate
        demographic.pop_age16_up = end_state.pop * census_block.pop_age16_up_rate
        demographic.pop_age25_up = end_state.pop * census_block.pop_age25_up_rate
        demographic.pop_age65_up = end_state.pop * census_block.pop_age65_up_rate
        
        demographic.pop_age20_64 = end_state.pop * (census_block.pop_female_age20_64_rate + 
                                                  census_block.pop_female_age20_64_rate)
        
        demographic.pop_hs_not_comp = end_state.pop * census_block.pop_hs_not_comp_rate
        demographic.pop_hs_diploma = end_state.pop * census_block.pop_hs_diploma_rate
        demographic.pop_some_college = end_state.pop * census_block.pop_assoc_some_coll_rate
        demographic.pop_college_degree = end_state.pop * census_block.pop_coll_degree_rate
        demographic.pop_graduate_degree = end_state.pop * census_block.pop_grad_degree_rate
        demographic.pop_employed = end_state.pop * census_block.pop_employed_rate
        demographic.hh_inc_00_10 = end_state.hh * census_block.hh_inc_00_10_rate
        demographic.hh_inc_10_20 = end_state.hh * census_block.hh_inc_10_20_rate
        demographic.hh_inc_20_30 = end_state.hh * census_block.hh_inc_20_30_rate
        demographic.hh_inc_30_40 = end_state.hh * census_block.hh_inc_30_40_rate
        demographic.hh_inc_40_50 = end_state.hh * census_block.hh_inc_40_50_rate
        demographic.hh_inc_50_60 = end_state.hh * census_block.hh_inc_50_60_rate
        demographic.hh_inc_60_75 = end_state.hh * census_block.hh_inc_60_75_rate
        demographic.hh_inc_75_100 = end_state.hh * census_block.hh_inc_75_100_rate
        demographic.hh_inc_100_125 = end_state.hh * census_block.hh_inc_100_125_rate
        demographic.hh_inc_125_150 = end_state.hh * census_block.hh_inc_125_150_rate
        demographic.hh_inc_150_200 = end_state.hh * census_block.hh_inc_150_200_rate
        demographic.hh_inc_200p = end_state.hh * census_block.hh_inc_200p_rate
        demographic.hh_avg_vehicles = census_block.hh_agg_veh_rate
        demographic.hh_avg_size = end_state.hh * census_block.hh_inc_200p_rate
        demographic.hh_agg_inc = end_state.hh * census_block.hh_agg_inc_rate
        demographic.hh_avg_inc = census_block.hh_agg_inc_rate
        demographic.hh_owner_occ = end_state.hh * census_block.hh_own_occ_rate
        demographic.hh_rental_occ = end_state.hh * census_block.hh_rent_occ_rate

        demographic.save()

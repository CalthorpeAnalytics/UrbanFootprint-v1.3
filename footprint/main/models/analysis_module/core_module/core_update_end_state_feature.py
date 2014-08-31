from footprint.main.models.analysis_module.core_module.core_revert_to_base_condition import core_end_state_revert_to_base_condition
from footprint.main.models.geospatial.db_entity_keys import DbEntityKey
__author__ = 'calthorpe'


def update_end_state_feature(config_entity, annotated_features):
    future_scenario_class = config_entity.db_entity_feature_class(DbEntityKey.FUTURE_SCENARIO)
    developable_class = config_entity.db_entity_feature_class(DbEntityKey.DEVELOPABLE)
    base_class = config_entity.db_entity_feature_class(DbEntityKey.BASE)

    for feature in annotated_features:
        future_scenario_feature = future_scenario_class.objects.get(id=feature.future_scenario_feature)
        developable = developable_class.objects.get(id=feature.developable)
        base = base_class.objects.get(id=feature.base_feature)

        if not feature.built_form_id:
            # If the user reverted the built_form, it will be null and we need to set it to the base built_form
            core_end_state_revert_to_base_condition(feature, base)
            continue

        feature.built_form_key = future_scenario_feature.built_form_key
        feature.built_form_base = base.built_form_key
        feature.refill_flag = future_scenario_feature.refill_flag
        

        feature.intersection_density_sqmi = future_scenario_feature.intersection_density_sqmi if feature.clear_base_flag is True else \
            future_scenario_feature.intersection_density_sqmi + future_scenario_feature.dev_pct * base.intersection_density_sqmi

        feature.acres_parcel = base.acres_parcel

        feature.acres_parcel_res = future_scenario_feature.acres_parcel_res if feature.clear_base_flag \
            is True else future_scenario_feature.acres_parcel_res - (future_scenario_feature.dev_pct * developable.acres_parcel_res) + \
                         base.acres_parcel_res

        feature.acres_parcel_res_detsf_ll = future_scenario_feature.acres_parcel_res_detsf_ll if \
            feature.clear_base_flag is True else future_scenario_feature.acres_parcel_res_detsf_ll \
                                             - (future_scenario_feature.dev_pct * developable.acres_parcel_res_detsf_ll) + \
                                             base.acres_parcel_res_detsf_ll

        feature.acres_parcel_res_detsf_sl = future_scenario_feature.acres_parcel_res_detsf_sl if \
            feature.clear_base_flag is True else future_scenario_feature.acres_parcel_res_detsf_sl \
                                             - (future_scenario_feature.dev_pct * developable.acres_parcel_res_detsf_sl) + \
                                             base.acres_parcel_res_detsf_sl

        feature.acres_parcel_res_detsf = feature.acres_parcel_res_detsf_ll + feature.acres_parcel_res_detsf_sl

        feature.acres_parcel_res_attsf = future_scenario_feature.acres_parcel_res_attsf if \
            feature.clear_base_flag is True else future_scenario_feature.acres_parcel_res_attsf - \
                                             (future_scenario_feature.dev_pct * developable.acres_parcel_res_attsf) + \
                                             base.acres_parcel_res_attsf

        feature.acres_parcel_res_mf = future_scenario_feature.acres_parcel_res_mf if feature.clear_base_flag \
            is True else future_scenario_feature.acres_parcel_res_mf - (future_scenario_feature.dev_pct * developable.acres_parcel_res_mf) + \
                         base.acres_parcel_res_mf

        feature.acres_parcel_emp = future_scenario_feature.acres_parcel_emp if feature.clear_base_flag \
            is True else future_scenario_feature.acres_parcel_emp - (future_scenario_feature.dev_pct * developable.acres_parcel_emp) + \
                         base.acres_parcel_emp

        feature.acres_parcel_emp_ret = future_scenario_feature.acres_parcel_emp_ret if feature.clear_base_flag is True else \
            future_scenario_feature.acres_parcel_emp_ret - (future_scenario_feature.dev_pct * developable.acres_parcel_emp_ret) + base.acres_parcel_emp_ret

        feature.acres_parcel_emp_off = future_scenario_feature.acres_parcel_emp_off if feature.clear_base_flag is True else \
            future_scenario_feature.acres_parcel_emp_off - (future_scenario_feature.dev_pct * developable.acres_parcel_emp_off) + base.acres_parcel_emp_off

        feature.acres_parcel_emp_ind = future_scenario_feature.acres_parcel_emp_ind if feature.clear_base_flag is True else \
            future_scenario_feature.acres_parcel_emp_ind - (future_scenario_feature.dev_pct * developable.acres_parcel_emp_ind) + base.acres_parcel_emp_ind

        feature.acres_parcel_emp_ag = future_scenario_feature.acres_parcel_emp_ag if feature.clear_base_flag is True else \
            future_scenario_feature.acres_parcel_emp_ag - (future_scenario_feature.dev_pct * developable.acres_parcel_emp_ag) + base.acres_parcel_emp_ag

        feature.acres_parcel_emp_mixed = future_scenario_feature.acres_parcel_emp_mixed if feature.clear_base_flag is True else \
            future_scenario_feature.acres_parcel_emp_mixed - (future_scenario_feature.dev_pct * developable.acres_parcel_emp_mixed) + base.acres_parcel_emp_mixed

        feature.acres_parcel_mixed = future_scenario_feature.acres_parcel_mixed if feature.clear_base_flag is True else \
            future_scenario_feature.acres_parcel_mixed - (future_scenario_feature.dev_pct * developable.acres_parcel_mixed) + base.acres_parcel_mixed

        feature.acres_parcel_mixed_w_off = future_scenario_feature.acres_parcel_mixed_w_off if feature.clear_base_flag is True else \
            future_scenario_feature.acres_parcel_mixed_w_off - (future_scenario_feature.dev_pct * developable.acres_parcel_mixed_w_off) + base.acres_parcel_mixed_w_off

        feature.acres_parcel_mixed_no_off = future_scenario_feature.acres_parcel_mixed_no_off if feature.clear_base_flag is True else \
            future_scenario_feature.acres_parcel_mixed_no_off - (future_scenario_feature.dev_pct * developable.acres_parcel_mixed_no_off) + base.acres_parcel_mixed_no_off

        feature.acres_parcel_no_use = future_scenario_feature.acres_parcel_no_use if feature.clear_base_flag is True else \
            future_scenario_feature.acres_parcel_no_use - (future_scenario_feature.dev_pct * developable.acres_parcel_no_use) + base.acres_parcel_no_use

        feature.pop = future_scenario_feature.pop if feature.clear_base_flag is True else \
            future_scenario_feature.pop - (future_scenario_feature.dev_pct * developable.pop) + base.pop

        feature.hh = future_scenario_feature.hh if feature.clear_base_flag is True else \
            future_scenario_feature.hh - (future_scenario_feature.dev_pct * developable.hh) + base.hh

        feature.du = future_scenario_feature.du if feature.clear_base_flag is True else \
            future_scenario_feature.du - (future_scenario_feature.dev_pct * developable.du) + base.du

        feature.du_detsf_ll = future_scenario_feature.du_detsf_ll if feature.clear_base_flag is True else \
            future_scenario_feature.du_detsf_ll - (future_scenario_feature.dev_pct * developable.du_detsf_ll) + base.du_detsf_ll

        feature.du_detsf_sl = future_scenario_feature.du_detsf_sl if feature.clear_base_flag is True else \
            future_scenario_feature.du_detsf_sl - (future_scenario_feature.dev_pct * developable.du_detsf_sl) + base.du_detsf_sl

        feature.du_detsf = feature.du_detsf_ll + feature.du_detsf_sl

        feature.du_attsf = future_scenario_feature.du_attsf if feature.clear_base_flag is True else \
            future_scenario_feature.du_attsf - (future_scenario_feature.dev_pct * developable.du_attsf) + base.du_attsf

        feature.du_mf = future_scenario_feature.du_mf if feature.clear_base_flag is True else \
            future_scenario_feature.du_mf - (future_scenario_feature.dev_pct * developable.du_mf) + base.du_mf

        feature.du_mf2to4 = future_scenario_feature.du_mf2to4 if feature.clear_base_flag is True else \
            future_scenario_feature.du_mf2to4 - (future_scenario_feature.dev_pct * developable.du_mf2to4) + base.du_mf2to4

        feature.du_mf5p = future_scenario_feature.du_mf5p if feature.clear_base_flag is True else \
            future_scenario_feature.du_mf5p - (future_scenario_feature.dev_pct * developable.du_mf5p) + base.du_mf5p

        feature.emp = future_scenario_feature.emp if feature.clear_base_flag is True else \
            future_scenario_feature.emp - (future_scenario_feature.dev_pct * developable.emp) + base.emp

        feature.emp_ret = future_scenario_feature.emp_ret if feature.clear_base_flag is True else \
            future_scenario_feature.emp_ret - (future_scenario_feature.dev_pct * developable.emp_ret) + base.emp_ret

        feature.emp_retail_services = future_scenario_feature.emp_retail_services if feature.clear_base_flag is True else \
            future_scenario_feature.emp_retail_services - (future_scenario_feature.dev_pct * developable.emp_retail_services) + base.emp_retail_services

        feature.emp_restaurant = future_scenario_feature.emp_restaurant if feature.clear_base_flag is True else \
            future_scenario_feature.emp_restaurant - (future_scenario_feature.dev_pct * developable.emp_restaurant) + base.emp_restaurant

        feature.emp_accommodation = future_scenario_feature.emp_accommodation if feature.clear_base_flag is True else \
            future_scenario_feature.emp_accommodation - (future_scenario_feature.dev_pct * developable.emp_accommodation) + base.emp_accommodation

        feature.emp_arts_entertainment = future_scenario_feature.emp_arts_entertainment if feature.clear_base_flag is True else \
            future_scenario_feature.emp_arts_entertainment - (future_scenario_feature.dev_pct * developable.emp_arts_entertainment) + base.emp_arts_entertainment

        feature.emp_other_services = future_scenario_feature.emp_other_services if feature.clear_base_flag is True else \
            future_scenario_feature.emp_other_services - (future_scenario_feature.dev_pct * developable.emp_other_services) + base.emp_other_services

        feature.emp_off = future_scenario_feature.emp_off if feature.clear_base_flag is True else \
            future_scenario_feature.emp_off - (future_scenario_feature.dev_pct * developable.emp_off) + base.emp_off
        
        feature.emp_pub = future_scenario_feature.emp_pub if feature.clear_base_flag is True else \
            future_scenario_feature.emp_pub - (future_scenario_feature.dev_pct * developable.emp_pub) + base.emp_pub

        feature.emp_office_services = future_scenario_feature.emp_office_services if feature.clear_base_flag is True else \
            future_scenario_feature.emp_office_services - (future_scenario_feature.dev_pct * developable.emp_office_services) + base.emp_office_services

        feature.emp_education = future_scenario_feature.emp_education if feature.clear_base_flag is True else \
            future_scenario_feature.emp_education - (future_scenario_feature.dev_pct * developable.emp_education) + base.emp_education

        feature.emp_public_admin = future_scenario_feature.emp_public_admin if feature.clear_base_flag is True else \
            future_scenario_feature.emp_public_admin - (future_scenario_feature.dev_pct * developable.emp_public_admin) + base.emp_public_admin

        feature.emp_medical_services = future_scenario_feature.emp_medical_services if feature.clear_base_flag is True else \
            future_scenario_feature.emp_medical_services - (future_scenario_feature.dev_pct * developable.emp_medical_services) + base.emp_medical_services

        feature.emp_ind = future_scenario_feature.emp_ind if feature.clear_base_flag is True else \
            future_scenario_feature.emp_ind - (future_scenario_feature.dev_pct * developable.emp_ind) + base.emp_ind

        feature.emp_wholesale = future_scenario_feature.emp_wholesale if feature.clear_base_flag is True else \
            future_scenario_feature.emp_wholesale - (future_scenario_feature.dev_pct * developable.emp_wholesale) + base.emp_wholesale

        feature.emp_transport_warehousing = future_scenario_feature.emp_transport_warehousing if feature.clear_base_flag is True else \
            future_scenario_feature.emp_transport_warehousing - (future_scenario_feature.dev_pct * developable.emp_transport_warehousing) + base.emp_transport_warehousing

        feature.emp_manufacturing = future_scenario_feature.emp_manufacturing if feature.clear_base_flag is True else \
            future_scenario_feature.emp_manufacturing - (future_scenario_feature.dev_pct * developable.emp_manufacturing) + base.emp_manufacturing

        feature.emp_construction_utilities = future_scenario_feature.emp_construction_utilities if feature.clear_base_flag is True else \
            future_scenario_feature.emp_construction_utilities - (
                (future_scenario_feature.dev_pct * (developable.emp_construction + developable.emp_utilities))) + \
            (base.emp_construction + base.emp_utilities)

        feature.emp_ag = future_scenario_feature.emp_ag if feature.clear_base_flag is True else \
            future_scenario_feature.emp_ag - (future_scenario_feature.dev_pct * developable.emp_ag) + base.emp_ag

        feature.emp_agriculture = future_scenario_feature.emp_agriculture if feature.clear_base_flag is True else \
            future_scenario_feature.emp_agriculture - (future_scenario_feature.dev_pct * developable.emp_agriculture) + base.emp_agriculture

        feature.emp_extraction = future_scenario_feature.emp_extraction if feature.clear_base_flag is True else \
            future_scenario_feature.emp_extraction - (future_scenario_feature.dev_pct * developable.emp_extraction) + base.emp_extraction

        feature.emp_military = future_scenario_feature.emp_military if feature.clear_base_flag is True else \
            future_scenario_feature.emp_military - (future_scenario_feature.dev_pct * developable.emp_military) + base.emp_military

        feature.bldg_sqft_detsf_ll = future_scenario_feature.bldg_sqft_detsf_ll if feature.clear_base_flag is True else \
            future_scenario_feature.bldg_sqft_detsf_ll - (future_scenario_feature.dev_pct * developable.bldg_sqft_detsf_ll) + base.bldg_sqft_detsf_ll

        feature.bldg_sqft_detsf_sl = future_scenario_feature.bldg_sqft_detsf_sl if feature.clear_base_flag is True else \
            future_scenario_feature.bldg_sqft_detsf_sl - (future_scenario_feature.dev_pct * developable.bldg_sqft_detsf_sl) + base.bldg_sqft_detsf_sl

        feature.bldg_sqft_attsf = future_scenario_feature.bldg_sqft_attsf if feature.clear_base_flag is True else \
            future_scenario_feature.bldg_sqft_attsf - (future_scenario_feature.dev_pct * developable.bldg_sqft_attsf) + base.bldg_sqft_attsf

        feature.bldg_sqft_mf = future_scenario_feature.bldg_sqft_mf if feature.clear_base_flag is True else \
            future_scenario_feature.bldg_sqft_mf - (future_scenario_feature.dev_pct * developable.bldg_sqft_mf) + base.bldg_sqft_mf

        feature.bldg_sqft_retail_services = future_scenario_feature.bldg_sqft_retail_services if feature.clear_base_flag is True else \
            future_scenario_feature.bldg_sqft_retail_services - (future_scenario_feature.dev_pct * developable.bldg_sqft_retail_services) + base.bldg_sqft_retail_services

        feature.bldg_sqft_restaurant = future_scenario_feature.bldg_sqft_restaurant if feature.clear_base_flag is True else \
            future_scenario_feature.bldg_sqft_restaurant - (future_scenario_feature.dev_pct * developable.bldg_sqft_restaurant) + base.bldg_sqft_restaurant

        feature.bldg_sqft_accommodation = future_scenario_feature.bldg_sqft_accommodation if feature.clear_base_flag is True else \
            future_scenario_feature.bldg_sqft_accommodation - (future_scenario_feature.dev_pct * developable.bldg_sqft_accommodation) + base.bldg_sqft_accommodation

        feature.bldg_sqft_arts_entertainment = future_scenario_feature.bldg_sqft_arts_entertainment if feature.clear_base_flag is True else \
            future_scenario_feature.bldg_sqft_arts_entertainment - (future_scenario_feature.dev_pct * developable.bldg_sqft_arts_entertainment) + base.bldg_sqft_arts_entertainment

        feature.bldg_sqft_other_services = future_scenario_feature.bldg_sqft_other_services if feature.clear_base_flag is True else \
            future_scenario_feature.bldg_sqft_other_services - (future_scenario_feature.dev_pct * developable.bldg_sqft_other_services) + base.bldg_sqft_other_services

        feature.bldg_sqft_office_services = future_scenario_feature.bldg_sqft_office_services if feature.clear_base_flag is True else \
            future_scenario_feature.bldg_sqft_office_services - (future_scenario_feature.dev_pct * developable.bldg_sqft_office_services) + base.bldg_sqft_office_services

        feature.bldg_sqft_public_admin = future_scenario_feature.bldg_sqft_public_admin if feature.clear_base_flag is True else \
            future_scenario_feature.bldg_sqft_public_admin - (future_scenario_feature.dev_pct * developable.bldg_sqft_public_admin) + base.bldg_sqft_public_admin

        feature.bldg_sqft_medical_services = future_scenario_feature.bldg_sqft_medical_services if feature.clear_base_flag is True else \
            future_scenario_feature.bldg_sqft_medical_services - (future_scenario_feature.dev_pct * developable.bldg_sqft_medical_services) + base.bldg_sqft_medical_services

        feature.bldg_sqft_education = future_scenario_feature.bldg_sqft_education if feature.clear_base_flag is True else \
            future_scenario_feature.bldg_sqft_education - (future_scenario_feature.dev_pct * developable.bldg_sqft_education) + base.bldg_sqft_education

        feature.bldg_sqft_wholesale = future_scenario_feature.bldg_sqft_wholesale if feature.clear_base_flag is True else \
            future_scenario_feature.bldg_sqft_wholesale - (future_scenario_feature.dev_pct * developable.bldg_sqft_wholesale) + base.bldg_sqft_wholesale

        feature.bldg_sqft_transport_warehousing = future_scenario_feature.bldg_sqft_transport_warehousing if feature.clear_base_flag is True else \
            future_scenario_feature.bldg_sqft_transport_warehousing - (future_scenario_feature.dev_pct * developable.bldg_sqft_transport_warehousing) + base.bldg_sqft_transport_warehousing

        feature.commercial_irrigated_sqft = future_scenario_feature.commercial_irrigated_sqft if feature.clear_base_flag is True else \
            future_scenario_feature.commercial_irrigated_sqft - (future_scenario_feature.dev_pct * developable.commercial_irrigated_sqft) + base.commercial_irrigated_sqft

        feature.residential_irrigated_sqft = future_scenario_feature.residential_irrigated_sqft if feature.clear_base_flag is True else \
            future_scenario_feature.residential_irrigated_sqft - (future_scenario_feature.dev_pct * developable.residential_irrigated_sqft) + base.residential_irrigated_sqft
        
        feature.save()
        
        calculate_land_development_category(feature)


def calculate_land_development_category(feature):

    if feature.intersection_density_sqmi >= 150 and feature.emp / feature.acres_gross > 70:
        land_development_category = 'urban'

    elif feature.intersection_density_sqmi >= 150 and feature.du / feature.acres_gross > 45:
        land_development_category = 'urban'

    elif feature.intersection_density_sqmi >= 150 and feature.emp / feature.acres_gross <= 70:
        land_development_category = 'compact'

    elif feature.intersection_density_sqmi >= 150 and feature.du / feature.acres_gross <= 45:
        land_development_category = 'compact'

    elif feature.intersection_density_sqmi < 150:
        land_development_category = 'standard'

    else:
        land_development_category = None
        
    feature.land_development_category = land_development_category
    feature.save()

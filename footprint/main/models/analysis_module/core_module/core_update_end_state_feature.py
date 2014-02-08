from footprint.main.models.keys.keys import Keys
from footprint.main.utils.query_parsing import annotated_related_feature_class_pk_via_geographies

__author__ = 'calthorpe'


def update_end_state_feature(config_entity):
    future_scenario_class = config_entity.feature_class_of_db_entity_key(Keys.DB_ABSTRACT_FUTURE_SCENARIO_FEATURE)
    developable_class = config_entity.feature_class_of_db_entity_key(Keys.DB_ABSTRACT_BASE_FEATURE)
    base_class = config_entity.feature_class_of_db_entity_key(Keys.DB_ABSTRACT_BASE_FEATURE)
    end_state_class = config_entity.feature_class_of_db_entity_key(Keys.DB_ABSTRACT_END_STATE_FEATURE)

    features = future_scenario_class.objects.filter(dirty_flag=True)

    annotated_features = annotated_related_feature_class_pk_via_geographies(features, config_entity, [Keys.DB_ABSTRACT_DEVELOPABLE, Keys.DB_ABSTRACT_BASE_FEATURE, Keys.DB_ABSTRACT_END_STATE_FEATURE])

    for feature in annotated_features:
        end_state = end_state_class.objects.get(id=feature.end_state)
        developable = developable_class.objects.get(id=feature.developable)
        base = base_class.objects.get(id=feature.base_feature)

        end_state.built_form_id = feature.built_form_id

        end_state.intersection_density_sqmi = feature.intersection_density_sqmi if feature.total_redev is True else \
            feature.intersection_density_sqmi + feature.dev_pct * base.intersection_density_sqmi

        end_state.acres_parcel = feature.acres_parcel if feature.total_redev is True else \
            feature.acres_parcel - (feature.dev_pct * developable.acres_parcel) + base.acres_parcel

        end_state.acres_parcel_res = feature.acres_parcel_res if feature.total_redev \
            is True else feature.acres_parcel_res - (feature.dev_pct * developable.acres_parcel_res) + \
                         base.acres_parcel_res

        end_state.acres_parcel_res_detsf_ll = feature.acres_parcel_res_detsf_ll if \
            feature.total_redev is True else feature.acres_parcel_res_detsf_ll \
                                             - (feature.dev_pct * developable.acres_parcel_res_detsf_ll) + \
                                             base.acres_parcel_res_detsf_ll

        end_state.acres_parcel_res_detsf_sl = feature.acres_parcel_res_detsf_sl if \
            feature.total_redev is True else feature.acres_parcel_res_detsf_sl \
                                             - (feature.dev_pct * developable.acres_parcel_res_detsf_sl) + \
                                             base.acres_parcel_res_detsf_sl

        end_state.acres_parcel_res_attsf = feature.acres_parcel_res_attsf if \
            feature.total_redev is True else feature.acres_parcel_res_attsf - \
                                             (feature.dev_pct * developable.acres_parcel_res_attsf) + \
                                             base.acres_parcel_res_attsf

        end_state.acres_parcel_res_mf = feature.acres_parcel_res_mf if feature.total_redev \
            is True else feature.acres_parcel_res_mf - (feature.dev_pct * developable.acres_parcel_res_mf) + \
                         base.acres_parcel_res_mf

        end_state.acres_parcel_emp = feature.acres_parcel_emp if feature.total_redev \
            is True else feature.acres_parcel_emp - (feature.dev_pct * developable.acres_parcel_emp) + \
                         base.acres_parcel_emp

        end_state.acres_parcel_emp_ret = feature.acres_parcel_emp_ret if feature.total_redev is True else \
            feature.acres_parcel_emp_ret - (feature.dev_pct * developable.acres_parcel_emp_ret) + base.acres_parcel_emp_ret

        end_state.acres_parcel_emp_off = feature.acres_parcel_emp_off if feature.total_redev is True else \
            feature.acres_parcel_emp_off - (feature.dev_pct * developable.acres_parcel_emp_off) + base.acres_parcel_emp_off

        end_state.acres_parcel_emp_ind = feature.acres_parcel_emp_ind if feature.total_redev is True else \
            feature.acres_parcel_emp_ind - (feature.dev_pct * developable.acres_parcel_emp_ind) + base.acres_parcel_emp_ind

        end_state.acres_parcel_emp_ag = feature.acres_parcel_emp_ag if feature.total_redev is True else \
            feature.acres_parcel_emp_ag - (feature.dev_pct * developable.acres_parcel_emp_ag) + base.acres_parcel_emp_ag

        end_state.acres_parcel_emp_mixed = feature.acres_parcel_emp_mixed if feature.total_redev is True else \
            feature.acres_parcel_emp_mixed - (feature.dev_pct * developable.acres_parcel_emp_mixed) + base.acres_parcel_emp_mixed

        end_state.acres_parcel_mixed = feature.acres_parcel_mixed if feature.total_redev is True else \
            feature.acres_parcel_mixed - (feature.dev_pct * developable.acres_parcel_mixed) + base.acres_parcel_mixed

        end_state.acres_parcel_mixed_w_off = feature.acres_parcel_mixed_w_off if feature.total_redev is True else \
            feature.acres_parcel_mixed_w_off - (feature.dev_pct * developable.acres_parcel_mixed_w_off) + base.acres_parcel_mixed_w_off

        end_state.acres_parcel_mixed_no_off = feature.acres_parcel_mixed_no_off if feature.total_redev is True else \
            feature.acres_parcel_mixed_no_off - (feature.dev_pct * developable.acres_parcel_mixed_no_off) + base.acres_parcel_mixed_no_off

        end_state.pop = feature.pop if feature.total_redev is True else \
            feature.pop - (feature.dev_pct * developable.pop) + base.pop

        end_state.hh = feature.hh if feature.total_redev is True else \
            feature.hh - (feature.dev_pct * developable.hh) + base.hh

        end_state.du = feature.du if feature.total_redev is True else \
            feature.du - (feature.dev_pct * developable.du) + base.du

        end_state.du_detsf_ll = feature.du_detsf_ll if feature.total_redev is True else \
            feature.du_detsf_ll - (feature.dev_pct * developable.du_detsf_ll) + base.du_detsf_ll

        end_state.du_detsf_sl = feature.du_detsf_sl if feature.total_redev is True else \
            feature.du_detsf_sl - (feature.dev_pct * developable.du_detsf_sl) + base.du_detsf_sl

        end_state.du_attsf = feature.du_attsf if feature.total_redev is True else \
            feature.du_attsf - (feature.dev_pct * developable.du_attsf) + base.du_attsf

        end_state.du_mf = feature.du_mf if feature.total_redev is True else \
            feature.du_mf - (feature.dev_pct * developable.du_mf) + base.du_mf

        end_state.du_mf2to4 = feature.du_mf2to4 if feature.total_redev is True else \
            feature.du_mf2to4 - (feature.dev_pct * developable.du_mf2to4) + base.du_mf2to4

        end_state.du_mf5p = feature.du_mf5p if feature.total_redev is True else \
            feature.du_mf5p - (feature.dev_pct * developable.du_mf5p) + base.du_mf5p

        end_state.emp = feature.emp if feature.total_redev is True else \
            feature.emp - (feature.dev_pct * developable.emp) + base.emp

        end_state.emp_ret = feature.emp_ret if feature.total_redev is True else \
            feature.emp_ret - (feature.dev_pct * developable.emp_ret) + base.emp_ret

        end_state.emp_retail_services = feature.emp_retail_services if feature.total_redev is True else \
            feature.emp_retail_services - (feature.dev_pct * developable.emp_retail_services) + base.emp_retail_services

        end_state.emp_restaurant = feature.emp_restaurant if feature.total_redev is True else \
            feature.emp_restaurant - (feature.dev_pct * developable.emp_restaurant) + base.emp_restaurant

        end_state.emp_accommodation = feature.emp_accommodation if feature.total_redev is True else \
            feature.emp_accommodation - (feature.dev_pct * developable.emp_accommodation) + base.emp_accommodation

        end_state.emp_arts_entertainment = feature.emp_arts_entertainment if feature.total_redev is True else \
            feature.emp_arts_entertainment - (feature.dev_pct * developable.emp_arts_entertainment) + base.emp_arts_entertainment

        end_state.emp_other_services = feature.emp_other_services if feature.total_redev is True else \
            feature.emp_other_services - (feature.dev_pct * developable.emp_other_services) + base.emp_other_services

        end_state.emp_off = feature.emp_off if feature.total_redev is True else \
            feature.emp_off - (feature.dev_pct * developable.emp_off) + base.emp_off

        end_state.emp_office_services = feature.emp_office_services if feature.total_redev is True else \
            feature.emp_office_services - (feature.dev_pct * developable.emp_office_services) + base.emp_office_services

        end_state.emp_education = feature.emp_education if feature.total_redev is True else \
            feature.emp_education - (feature.dev_pct * developable.emp_education) + base.emp_education

        end_state.emp_public_admin = feature.emp_public_admin if feature.total_redev is True else \
            feature.emp_public_admin - (feature.dev_pct * developable.emp_public_admin) + base.emp_public_admin

        end_state.emp_medical_services = feature.emp_medical_services if feature.total_redev is True else \
            feature.emp_medical_services - (feature.dev_pct * developable.emp_medical_services) + base.emp_medical_services

        end_state.emp_ind = feature.emp_ind if feature.total_redev is True else \
            feature.emp_ind - (feature.dev_pct * developable.emp_ind) + base.emp_ind

        end_state.emp_wholesale = feature.emp_wholesale if feature.total_redev is True else \
            feature.emp_wholesale - (feature.dev_pct * developable.emp_wholesale) + base.emp_wholesale

        end_state.emp_transport_warehousing = feature.emp_transport_warehousing if feature.total_redev is True else \
            feature.emp_transport_warehousing - (feature.dev_pct * developable.emp_transport_warehousing) + base.emp_transport_warehousing

        end_state.emp_manufacturing = feature.emp_manufacturing if feature.total_redev is True else \
            feature.emp_manufacturing - (feature.dev_pct * developable.emp_manufacturing) + base.emp_manufacturing

        end_state.emp_construction_utilities = feature.emp_construction_utilities if feature.total_redev is True else \
            feature.emp_construction_utilities - (
                (feature.dev_pct * (developable.emp_construction + developable.emp_utilities))) + \
            (base.emp_construction + base.emp_utilities)

        end_state.emp_ag = feature.emp_ag if feature.total_redev is True else \
            feature.emp_ag - (feature.dev_pct * developable.emp_ag) + base.emp_ag

        end_state.emp_agriculture = feature.emp_agriculture if feature.total_redev is True else \
            feature.emp_agriculture - (feature.dev_pct * developable.emp_agriculture) + base.emp_agriculture

        end_state.emp_extraction = feature.emp_extraction if feature.total_redev is True else \
            feature.emp_extraction - (feature.dev_pct * developable.emp_extraction) + base.emp_extraction

        end_state.emp_military = feature.emp_military if feature.total_redev is True else \
            feature.emp_military - (feature.dev_pct * developable.emp_military) + base.emp_military

        end_state.bldg_sqft_detsf_ll = feature.bldg_sqft_detsf_ll if feature.total_redev is True else \
            feature.bldg_sqft_detsf_ll - (feature.dev_pct * developable.bldg_sqft_detsf_ll) + base.bldg_sqft_detsf_ll

        end_state.bldg_sqft_detsf_sl = feature.bldg_sqft_detsf_sl if feature.total_redev is True else \
            feature.bldg_sqft_detsf_sl - (feature.dev_pct * developable.bldg_sqft_detsf_sl) + base.bldg_sqft_detsf_sl

        end_state.bldg_sqft_attsf = feature.bldg_sqft_attsf if feature.total_redev is True else \
            feature.bldg_sqft_attsf - (feature.dev_pct * developable.bldg_sqft_attsf) + base.bldg_sqft_attsf

        end_state.bldg_sqft_mf = feature.bldg_sqft_mf if feature.total_redev is True else \
            feature.bldg_sqft_mf - (feature.dev_pct * developable.bldg_sqft_mf) + base.bldg_sqft_mf

        end_state.bldg_sqft_retail_services = feature.bldg_sqft_retail_services if feature.total_redev is True else \
            feature.bldg_sqft_retail_services - (feature.dev_pct * developable.bldg_sqft_retail_services) + base.bldg_sqft_retail_services

        end_state.bldg_sqft_restaurant = feature.bldg_sqft_restaurant if feature.total_redev is True else \
            feature.bldg_sqft_restaurant - (feature.dev_pct * developable.bldg_sqft_restaurant) + base.bldg_sqft_restaurant

        end_state.bldg_sqft_accommodation = feature.bldg_sqft_accommodation if feature.total_redev is True else \
            feature.bldg_sqft_accommodation - (feature.dev_pct * developable.bldg_sqft_accommodation) + base.bldg_sqft_accommodation

        end_state.bldg_sqft_arts_entertainment = feature.bldg_sqft_arts_entertainment if feature.total_redev is True else \
            feature.bldg_sqft_arts_entertainment - (feature.dev_pct * developable.bldg_sqft_arts_entertainment) + base.bldg_sqft_arts_entertainment

        end_state.bldg_sqft_other_services = feature.bldg_sqft_other_services if feature.total_redev is True else \
            feature.bldg_sqft_other_services - (feature.dev_pct * developable.bldg_sqft_other_services) + base.bldg_sqft_other_services

        end_state.bldg_sqft_office_services = feature.bldg_sqft_office_services if feature.total_redev is True else \
            feature.bldg_sqft_office_services - (feature.dev_pct * developable.bldg_sqft_office_services) + base.bldg_sqft_office_services

        end_state.bldg_sqft_public_admin = feature.bldg_sqft_public_admin if feature.total_redev is True else \
            feature.bldg_sqft_public_admin - (feature.dev_pct * developable.bldg_sqft_public_admin) + base.bldg_sqft_public_admin

        end_state.bldg_sqft_medical_services = feature.bldg_sqft_medical_services if feature.total_redev is True else \
            feature.bldg_sqft_medical_services - (feature.dev_pct * developable.bldg_sqft_medical_services) + base.bldg_sqft_medical_services

        end_state.bldg_sqft_education = feature.bldg_sqft_education if feature.total_redev is True else \
            feature.bldg_sqft_education - (feature.dev_pct * developable.bldg_sqft_education) + base.bldg_sqft_education

        end_state.bldg_sqft_wholesale = feature.bldg_sqft_wholesale if feature.total_redev is True else \
            feature.bldg_sqft_wholesale - (feature.dev_pct * developable.bldg_sqft_wholesale) + base.bldg_sqft_wholesale

        end_state.bldg_sqft_transport_warehousing = feature.bldg_sqft_transport_warehousing if feature.total_redev is True else \
            feature.bldg_sqft_transport_warehousing - (feature.dev_pct * developable.bldg_sqft_transport_warehousing) + base.bldg_sqft_transport_warehousing

        end_state.commercial_irrigated_sqft = feature.commercial_irrigated_sqft if feature.total_redev is True else \
            feature.commercial_irrigated_sqft - (feature.dev_pct * developable.commercial_irrigated_sqft) + base.commercial_irrigated_sqft

        end_state.residential_irrigated_sqft = feature.residential_irrigated_sqft if feature.total_redev is True else \
            feature.residential_irrigated_sqft - (feature.dev_pct * developable.residential_irrigated_sqft) + base.residential_irrigated_sqft

        end_state.save()


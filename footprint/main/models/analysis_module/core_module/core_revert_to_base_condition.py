__author__ = 'calthorpe'


def core_future_scenario_revert_to_base_condition(future):
    future.dev_pct = 1.0
    future.density_pct = 1.0
    future.gross_net_pct = 1.0

    future.refill_flag = False

    future.acres_developing = 0
    future.acres_developable = 0

    future.built_form_key = None
    future.intersection_density_sqmi = 0
    future.pop = 0
    future.hh = 0
    future.du = 0
    future.du_detsf_ll = 0
    future.du_detsf_sl = 0
    future.du_attsf = 0
    future.du_mf = 0

    future.du_mf2to4 = 0
    future.du_mf5p = 0

    future.emp = 0
    future.emp_ret = 0

    future.emp_off = 0
    future.emp_pub = 0

    future.emp_ind = 0
    future.emp_ag = 0
    future.emp_military = 0

    future.emp_retail_services = 0
    future.emp_restaurant = 0
    future.emp_accommodation = 0
    future.emp_arts_entertainment = 0
    future.emp_other_services = 0

    future.emp_office_services = 0
    future.emp_medical_services = 0

    future.emp_education = 0
    future.emp_public_admin = 0

    future.emp_wholesale = 0
    future.emp_transport_warehousing = 0
    future.emp_manufacturing = 0
    future.emp_construction_utilities = 0

    future.emp_agriculture = 0
    future.emp_extraction = 0

    future.bldg_sqft_detsf_ll = 0
    future.bldg_sqft_detsf_sl = 0
    future.bldg_sqft_attsf = 0
    future.bldg_sqft_mf = 0
    future.bldg_sqft_retail_services = 0
    future.bldg_sqft_restaurant = 0
    future.bldg_sqft_accommodation = 0
    future.bldg_sqft_arts_entertainment = 0
    future.bldg_sqft_other_services = 0
    future.bldg_sqft_office_services = 0
    future.bldg_sqft_public_admin = 0
    future.bldg_sqft_medical_services = 0
    future.bldg_sqft_education = 0
    future.bldg_sqft_wholesale = 0
    future.bldg_sqft_transport_warehousing = 0

    future.commercial_irrigated_sqft = 0
    future.residential_irrigated_sqft = 0


    future.acres_parcel_res = 0
    future.acres_parcel_res_detsf_ll = 0
    future.acres_parcel_res_detsf_sl = 0
    future.acres_parcel_res_attsf = 0
    future.acres_parcel_res_mf = 0

    future.acres_parcel_emp = 0
    future.acres_parcel_emp_ret = 0
    future.acres_parcel_emp_off = 0
    future.acres_parcel_emp_ind = 0
    future.acres_parcel_emp_ag = 0
    future.acres_parcel_emp_mixed = 0
    future.acres_parcel_mixed = 0

    future.acres_parcel_mixed_w_off = 0
    future.acres_parcel_mixed_no_off = 0

    future.acres_parcel_no_use = 0

    future.save()


def core_end_state_revert_to_base_condition(end_state, base):
    
    end_state.built_form_key = base.built_form_key
    end_state.built_form_base = None
    end_state.built_form_id = base.built_form_id
    end_state.land_development_category = None
    end_state.intersection_density_sqmi = base.intersection_density_sqmi

    end_state.pop = base.pop
    end_state.hh =base.hh
    end_state.du = base.du

    end_state.du_detsf = base.du_detsf
    end_state.du_attsf = base.du_attsf
    end_state.du_mf = base.du_mf

    end_state.emp = base.emp

    end_state.emp_ret = base.emp_ret
    end_state.emp_off = base.emp_off
    end_state.emp_pub = base.emp_pub
    end_state.emp_ind = base.emp_ind
    end_state.emp_ag = base.emp_ag
    end_state.emp_military = base.emp_military

    end_state.du_detsf_sl = base.du_detsf_sl
    end_state.du_detsf_ll = base.du_detsf_ll
    end_state.du_mf2to4 = base.du_mf2to4
    end_state.du_mf5p = base.du_mf5p

    end_state.emp_retail_services = base.emp_retail_services
    end_state.emp_restaurant = base.emp_restaurant
    end_state.emp_accommodation = base.emp_accommodation
    end_state.emp_arts_entertainment = base.emp_arts_entertainment
    end_state.emp_other_services = base.emp_other_services

    end_state.emp_office_services = base.emp_office_services
    end_state.emp_public_admin = base.emp_public_admin
    end_state.emp_education =base.emp_education
    end_state.emp_medical_services = base.emp_medical_services
    
    end_state.emp_manufacturing =base.emp_manufacturing
    end_state.emp_wholesale = base.emp_wholesale
    end_state.emp_transport_warehousing = base.emp_transport_warehousing
    end_state.emp_utilities = base.emp_utilities
    end_state.emp_construction = base.emp_construction

    end_state.emp_agriculture = base.emp_agriculture
    end_state.emp_extraction = base.emp_extraction

    end_state.bldg_sqft_detsf_sl = base.bldg_sqft_detsf_sl
    end_state.bldg_sqft_detsf_ll = base.bldg_sqft_detsf_ll
    end_state.bldg_sqft_attsf = base.bldg_sqft_attsf
    end_state.bldg_sqft_mf = base.bldg_sqft_mf

    end_state.bldg_sqft_retail_services = base.bldg_sqft_retail_services
    end_state.bldg_sqft_restaurant = base.bldg_sqft_restaurant
    end_state.bldg_sqft_accommodation = base.bldg_sqft_accommodation
    end_state.bldg_sqft_arts_entertainment = base.bldg_sqft_arts_entertainment
    end_state.bldg_sqft_other_services = base.bldg_sqft_other_services
    end_state.bldg_sqft_office_services = base.bldg_sqft_office_services
    end_state.bldg_sqft_public_admin = base.bldg_sqft_public_admin
    end_state.bldg_sqft_education = base.bldg_sqft_education
    end_state.bldg_sqft_medical_services = base.bldg_sqft_medical_services
    end_state.bldg_sqft_wholesale = base.bldg_sqft_wholesale
    end_state.bldg_sqft_transport_warehousing = base.bldg_sqft_transport_warehousing

    end_state.residential_irrigated_sqft = base.residential_irrigated_sqft
    end_state.commercial_irrigated_sqft = base.commercial_irrigated_sqft

    end_state.acres_parcel_res = base.acres_parcel_res
    end_state.acres_parcel_res_detsf = base.acres_parcel_res_detsf
    end_state.acres_parcel_res_detsf_sl = base.acres_parcel_res_detsf_sl
    end_state.acres_parcel_res_detsf_ll = base.acres_parcel_res_detsf_ll
    end_state.acres_parcel_res_attsf = base.acres_parcel_res_attsf
    end_state.acres_parcel_res_mf = base.acres_parcel_res_mf
    end_state.acres_parcel_emp = base.acres_parcel_emp
    end_state.acres_parcel_emp_off = base.acres_parcel_emp_off
    end_state.acres_parcel_emp_ret = base.acres_parcel_emp_ret
    end_state.acres_parcel_emp_ind = base.acres_parcel_emp_ind
    end_state.acres_parcel_emp_ag = base.acres_parcel_emp_ag
    end_state.acres_parcel_emp_mixed = base.acres_parcel_emp_mixed
    end_state.acres_parcel_emp_military = base.acres_parcel_emp_military
    end_state.acres_parcel_mixed = base.acres_parcel_mixed
    end_state.acres_parcel_mixed_w_off = base.acres_parcel_mixed_w_off
    end_state.acres_parcel_mixed_no_off = base.acres_parcel_mixed_no_off
    end_state.acres_parcel_no_use = base.acres_parcel_no_use
    
    end_state.save()
    
def core_increment_revert_to_base_condition(increment):
    increment.built_form_key = None
    increment.built_form_id = None
    increment.land_development_category = None
    increment.refill_flag = False

    increment.pop = 0
    increment.hh = 0
    increment.du = 0
    increment.emp = 0
    increment.du_detsf = 0
    increment.du_detsf_ll = 0
    increment.du_detsf_sl = 0
    increment.du_attsf = 0
    increment.du_mf = 0

    increment.emp_ret = 0
    increment.emp_retail_services = 0
    increment.emp_restaurant = 0
    increment.emp_accommodation = 0
    increment.emp_arts_entertainment = 0
    increment.emp_other_services = 0

    increment.emp_off = 0
    increment.emp_office_services = 0
    increment.emp_medical_services = 0
    
    increment.emp_pub = 0
    increment.emp_education = 0
    increment.emp_public_admin = 0

    increment.emp_ind = 0
    increment.emp_wholesale = 0
    increment.emp_transport_warehousing = 0
    increment.emp_manufacturing = 0
    increment.emp_utilities = 0
    increment.emp_construction = 0

    increment.emp_ag = 0
    increment.emp_agriculture = 0
    increment.emp_extraction = 0

    increment.emp_military = 0

    increment.save()

def core_demographic_revert_to_base_condition(demographic, base_demographic):
    demographic.du_occupancy_rate = base_demographic.du_occupancy_rate
    demographic.pop_male = base_demographic.pop_male
    demographic.pop_female = base_demographic.pop_female

    demographic.pop_female_age20_64 = base_demographic.pop_female_age20_64
    demographic.pop_male_age20_64 = base_demographic.pop_male_age20_64
    demographic.pop_age16_up = base_demographic.pop_age16_up
    demographic.pop_age25_up = base_demographic.pop_age25_up
    demographic.pop_age65_up = base_demographic.pop_age65_up

    demographic.pop_age20_64 = base_demographic.pop_age20_64

    demographic.pop_hs_not_comp = base_demographic.pop_hs_not_comp
    demographic.pop_hs_diploma = base_demographic.pop_hs_diploma
    demographic.pop_some_college = base_demographic.pop_some_college
    demographic.pop_college_degree = base_demographic.pop_college_degree
    demographic.pop_graduate_degree = base_demographic.pop_graduate_degree
    demographic.pop_employed = base_demographic.pop_employed
    demographic.hh_inc_00_10 = base_demographic.hh_inc_00_10
    demographic.hh_inc_10_20 = base_demographic.hh_inc_10_20
    demographic.hh_inc_20_30 = base_demographic.hh_inc_20_30
    demographic.hh_inc_30_40 = base_demographic.hh_inc_30_40
    demographic.hh_inc_40_50 = base_demographic.hh_inc_40_50
    demographic.hh_inc_50_60 = base_demographic.hh_inc_50_60
    demographic.hh_inc_60_75 = base_demographic.hh_inc_60_75
    demographic.hh_inc_75_100 = base_demographic.hh_inc_75_100
    demographic.hh_inc_100_125 = base_demographic.hh_inc_100_125
    demographic.hh_inc_125_150 = base_demographic.hh_inc_125_150
    demographic.hh_inc_150_200 = base_demographic.hh_inc_150_200
    demographic.hh_inc_200p = base_demographic.hh_inc_200p
    demographic.hh_avg_vehicles = base_demographic.hh_avg_vehicles

    demographic.hh_avg_size = base_demographic.hh_avg_size
    demographic.hh_agg_inc = base_demographic.hh_agg_inc
    demographic.hh_avg_inc = base_demographic.hh_avg_inc
    demographic.hh_owner_occ = base_demographic.hh_owner_occ
    demographic.hh_rental_occ = base_demographic.hh_rental_occ

    demographic.save()
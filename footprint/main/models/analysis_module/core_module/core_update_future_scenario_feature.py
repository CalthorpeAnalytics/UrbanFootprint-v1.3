from footprint.main.lib.functions import map_to_dict
from footprint.main.models.analysis_module.core_module.core_revert_to_base_condition import core_future_scenario_revert_to_base_condition
from footprint.main.models.built_form.flat_built_form import FlatBuiltForm
from footprint.main.models.geospatial.db_entity_keys import DbEntityKey

import logging

__author__ = 'calthorpe'
logger = logging.getLogger(__name__)

def update_future_scenario_feature(config_entity, annotated_features):
    future_scenario_class = config_entity.db_entity_feature_class(DbEntityKey.FUTURE_SCENARIO)
    developable_class = config_entity.db_entity_feature_class(DbEntityKey.DEVELOPABLE)

    logger.info("annotating features for {0}".format(config_entity))
    logger.info("geography class {0}".format(annotated_features.model.geographies.field.rel.to))

    flat_built_forms = map_to_dict(
        lambda flat_built_form: [flat_built_form.built_form_id, flat_built_form],
        FlatBuiltForm.objects.filter(built_form_id__in=map(lambda feature: feature.built_form.id,
                                                           filter(lambda feature: feature.built_form, annotated_features)))
    )
    logger.debug("processing {0} future scenario features".format(len(annotated_features)))
    for update_feature in annotated_features:
        developable = developable_class.objects.get(id=update_feature.developable)
        feature = future_scenario_class.objects.get(id=update_feature.future_scenario_feature)

        flat_built_form = flat_built_forms.get(update_feature.built_form.id, FlatBuiltForm()) if update_feature.built_form else FlatBuiltForm()

        if not update_feature.built_form_id:
            # If the user reverted the built_form, it will be null and we need to set it to the base built_form
            core_future_scenario_revert_to_base_condition(feature)
            continue

        feature.dev_pct = update_feature.dev_pct
        feature.density_pct = update_feature.density_pct
        feature.gross_net_pct = update_feature.gross_net_pct

        feature.refill_flag = True if developable.acres_urban > developable.acres_greenfield else False

        feature.acres_developing = developable.acres_developable
        feature.acres_developable = developable.acres_developable * feature.dev_pct

        feature.built_form_key = flat_built_form.key

        feature.intersection_density_sqmi = flat_built_form.intersection_density * feature.dev_pct * \
            feature.gross_net_pct * feature.density_pct

        use_acres_parcel = flat_built_form.acres_parcel_residential + flat_built_form.acres_parcel_employment + flat_built_form.acres_parcel_mixed_use
        applied_acres = developable.acres_developable * feature.dev_pct * feature.gross_net_pct
        density_adjusted_acres = applied_acres * feature.density_pct

        feature.acres_parcel = use_acres_parcel * applied_acres * feature.dev_pct

        feature.pop = flat_built_form.population_density * density_adjusted_acres
        feature.hh = flat_built_form.household_density * density_adjusted_acres
        feature.du = flat_built_form.dwelling_unit_density * density_adjusted_acres
        feature.du_detsf_ll = flat_built_form.single_family_large_lot_density * density_adjusted_acres
        feature.du_detsf_sl = flat_built_form.single_family_small_lot_density * density_adjusted_acres
        feature.du_attsf = flat_built_form.attached_single_family_density * density_adjusted_acres
        feature.du_mf = (flat_built_form.multifamily_2_to_4_density + flat_built_form.multifamily_5_plus_density) * density_adjusted_acres

        feature.du_mf2to4 = flat_built_form.multifamily_2_to_4_density * density_adjusted_acres
        feature.du_mf5p = flat_built_form.multifamily_5_plus_density * density_adjusted_acres

        feature.emp = flat_built_form.employment_density * density_adjusted_acres
        feature.emp_ret = flat_built_form.retail_density * density_adjusted_acres

        feature.emp_off = (flat_built_form.office_services_density + flat_built_form.medical_services_density) * \
                          density_adjusted_acres
        feature.emp_pub = (flat_built_form.education_services_density + flat_built_form.public_admin_density) * \
                          density_adjusted_acres

        feature.emp_ind = flat_built_form.industrial_density * density_adjusted_acres
        feature.emp_ag = flat_built_form.agricultural_density * density_adjusted_acres
        feature.emp_military = flat_built_form.armed_forces_density * density_adjusted_acres

        feature.emp_retail_services = flat_built_form.retail_services_density * density_adjusted_acres
        feature.emp_restaurant = flat_built_form.restaurant_density * density_adjusted_acres
        feature.emp_accommodation = flat_built_form.accommodation_density * density_adjusted_acres
        feature.emp_arts_entertainment = flat_built_form.arts_entertainment_density * density_adjusted_acres
        feature.emp_other_services = flat_built_form.other_services_density * density_adjusted_acres

        feature.emp_office_services = flat_built_form.office_services_density * density_adjusted_acres
        feature.emp_medical_services = flat_built_form.medical_services_density * density_adjusted_acres

        feature.emp_education = flat_built_form.education_services_density * density_adjusted_acres
        feature.emp_public_admin = flat_built_form.public_admin_density * density_adjusted_acres

        feature.emp_wholesale = flat_built_form.wholesale_density * density_adjusted_acres
        feature.emp_transport_warehousing = flat_built_form.transport_warehouse_density * density_adjusted_acres
        feature.emp_manufacturing = flat_built_form.manufacturing_density * density_adjusted_acres
        feature.emp_construction_utilities = flat_built_form.construction_utilities_density * density_adjusted_acres

        feature.emp_agriculture = flat_built_form.agriculture_density * density_adjusted_acres
        feature.emp_extraction = flat_built_form.extraction_density * density_adjusted_acres

        feature.bldg_sqft_detsf_ll = flat_built_form.building_sqft_single_family_large_lot * density_adjusted_acres
        feature.bldg_sqft_detsf_sl = flat_built_form.building_sqft_single_family_small_lot * density_adjusted_acres
        feature.bldg_sqft_attsf = flat_built_form.building_sqft_attached_single_family * density_adjusted_acres
        feature.bldg_sqft_mf = (flat_built_form.building_sqft_multifamily_2_to_4 + flat_built_form.building_sqft_multifamily_5_plus) * density_adjusted_acres
        feature.bldg_sqft_retail_services = flat_built_form.building_sqft_retail_services * density_adjusted_acres
        feature.bldg_sqft_restaurant = flat_built_form.building_sqft_restaurant * density_adjusted_acres
        feature.bldg_sqft_accommodation = flat_built_form.building_sqft_accommodation * density_adjusted_acres
        feature.bldg_sqft_arts_entertainment = flat_built_form.building_sqft_arts_entertainment * density_adjusted_acres
        feature.bldg_sqft_other_services = flat_built_form.building_sqft_other_services * density_adjusted_acres
        feature.bldg_sqft_office_services = flat_built_form.building_sqft_office_services * density_adjusted_acres
        feature.bldg_sqft_public_admin = flat_built_form.building_sqft_public_admin * density_adjusted_acres
        feature.bldg_sqft_medical_services = flat_built_form.building_sqft_medical_services * density_adjusted_acres
        feature.bldg_sqft_education = flat_built_form.building_sqft_education_services * density_adjusted_acres
        feature.bldg_sqft_wholesale = flat_built_form.building_sqft_wholesale * density_adjusted_acres
        feature.bldg_sqft_transport_warehousing = flat_built_form.building_sqft_transport_warehouse * density_adjusted_acres

        feature.commercial_irrigated_sqft = flat_built_form.commercial_irrigated_square_feet * density_adjusted_acres
        feature.residential_irrigated_sqft = flat_built_form.residential_irrigated_square_feet * density_adjusted_acres


        feature.acres_parcel_res = flat_built_form.acres_parcel_residential * applied_acres
        feature.acres_parcel_res_detsf_ll = flat_built_form.acres_parcel_residential_single_family_large_lot * applied_acres
        feature.acres_parcel_res_detsf_sl = flat_built_form.acres_parcel_residential_single_family_small_lot * applied_acres
        feature.acres_parcel_res_attsf = flat_built_form.acres_parcel_residential_attached_single_family * applied_acres
        feature.acres_parcel_res_mf = flat_built_form.acres_parcel_residential_multifamily * applied_acres

        feature.acres_parcel_emp = flat_built_form.acres_parcel_employment * applied_acres
        feature.acres_parcel_emp_ret = flat_built_form.acres_parcel_employment_retail * applied_acres
        feature.acres_parcel_emp_off = flat_built_form.acres_parcel_employment_office * applied_acres
        feature.acres_parcel_emp_ind = flat_built_form.acres_parcel_employment_industrial * applied_acres
        feature.acres_parcel_emp_ag = flat_built_form.acres_parcel_employment_agriculture * applied_acres
        feature.acres_parcel_emp_mixed = flat_built_form.acres_parcel_employment_mixed * applied_acres
        feature.acres_parcel_mixed = flat_built_form.acres_parcel_mixed_use * applied_acres

        feature.acres_parcel_mixed_w_off = flat_built_form.acres_parcel_mixed_use_with_office * applied_acres
        feature.acres_parcel_mixed_no_off = flat_built_form.acres_parcel_mixed_use_without_office * applied_acres

        feature.acres_parcel_no_use = use_acres_parcel * developable.acres_developable * feature.dev_pct * \
            (1 - feature.gross_net_pct) if update_feature.clear_base_flag is False else \
            (use_acres_parcel * developable.acres_developable * (1 - feature.dev_pct)) + (use_acres_parcel * \
            developable.acres_developable * feature.dev_pct * (1 - feature.gross_net_pct))

        feature.save()

from footprint.main.lib.functions import map_to_dict
from footprint.main.models import FlatBuiltForm
from footprint.main.models.keys.keys import Keys
from footprint.main.utils.query_parsing import annotated_related_feature_class_pk_via_geographies
from django.utils.timezone import utc
import datetime

__author__ = 'calthorpe'


def update_future_scenario_feature(config_entity):
    future_scenario_class = config_entity.feature_class_of_db_entity_key(Keys.DB_ABSTRACT_FUTURE_SCENARIO_FEATURE)
    developable_class = config_entity.feature_class_of_db_entity_key(Keys.DB_ABSTRACT_DEVELOPABLE)

    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    features = future_scenario_class.objects.filter(
        updated__gt=now - datetime.timedelta(seconds=60))

    annotated_features = annotated_related_feature_class_pk_via_geographies(features, config_entity, [Keys.DB_ABSTRACT_DEVELOPABLE])
    flat_built_forms = map_to_dict(
        lambda flat_built_form: [flat_built_form.built_form_id, flat_built_form],
        FlatBuiltForm.objects.filter(built_form_id__in=map(lambda feature: feature.built_form.id, filter(lambda feature: feature.built_form, features)))
    )

    for feature in annotated_features:

        developable = developable_class.objects.get(id=feature.developable)
        flat_built_form = flat_built_forms.get(feature.built_form.id, FlatBuiltForm()) if feature.built_form else FlatBuiltForm()

        feature.dirty_flag = True
        feature.refill_flag = True if developable.acres_urban > developable.acres_greenfield else False

        feature.acres_developing = developable.acres_developable
        feature.acres_developable = developable.acres_developable * feature.dev_pct

        feature.intersection_density_sqmi = flat_built_form.intersection_density * feature.dev_pct

        feature.acres_parcel = (flat_built_form.acres_parcel_residential + flat_built_form.acres_parcel_employment +
        flat_built_form.acres_parcel_mixed_use) * developable.acres_developable * feature.dev_pct 


        feature.acres_parcel_res = flat_built_form.acres_parcel_residential * developable.acres_developable * \
        feature.dev_pct if feature.total_redev is False else flat_built_form.acres_parcel_residential * \
        developable.acres_developable

        feature.acres_parcel_res_detsf_ll = flat_built_form.acres_parcel_residential_single_family_large_lot * \
        developable.acres_developable * feature.dev_pct if feature.total_redev is False \
        else flat_built_form.acres_parcel_residential_single_family_large_lot * developable.acres_developable

        feature.acres_parcel_res_detsf_sl = flat_built_form.acres_parcel_residential_single_family_small_lot * \
        developable.acres_developable * feature.dev_pct if feature.total_redev is False \
        else flat_built_form.acres_parcel_residential_single_family_small_lot * developable.acres_developable

        feature.acres_parcel_res_attsf = flat_built_form.acres_parcel_residential_attached_single_family * \
        developable.acres_developable * feature.dev_pct if feature.total_redev is False \
        else flat_built_form.acres_parcel_residential_attached_single_family * developable.acres_developable

        feature.acres_parcel_res_mf = flat_built_form.acres_parcel_residential_multifamily * \
        developable.acres_developable * feature.dev_pct if feature.total_redev is False \
        else flat_built_form.acres_parcel_residential_multifamily * developable.acres_developable

        feature.acres_parcel_emp = flat_built_form.acres_parcel_employment * \
        developable.acres_developable * feature.dev_pct if feature.total_redev is False \
        else flat_built_form.acres_parcel_employment * developable.acres_developable

        feature.acres_parcel_emp_ret = flat_built_form.acres_parcel_employment_retail * \
        developable.acres_developable * feature.dev_pct if feature.total_redev is False \
        else flat_built_form.acres_parcel_employment_retail * developable.acres_developable

        feature.acres_parcel_emp_off = flat_built_form.acres_parcel_employment_office * \
        developable.acres_developable * feature.dev_pct if feature.total_redev is False \
        else flat_built_form.acres_parcel_employment_office * developable.acres_developable

        feature.acres_parcel_emp_ind = flat_built_form.acres_parcel_employment_industrial * \
        developable.acres_developable * feature.dev_pct if feature.total_redev is False \
        else flat_built_form.acres_parcel_employment_industrial * developable.acres_developable

        feature.acres_parcel_emp_ag = flat_built_form.acres_parcel_employment_agriculture * \
        developable.acres_developable * feature.dev_pct if feature.total_redev is False \
        else flat_built_form.acres_parcel_employment_agriculture * developable.acres_developable

        feature.acres_parcel_emp_mixed = flat_built_form.acres_parcel_employment_mixed * \
        developable.acres_developable * feature.dev_pct if feature.total_redev is False \
        else flat_built_form.acres_parcel_employment_mixed * developable.acres_developable

        feature.acres_parcel_mixed = flat_built_form.acres_parcel_mixed_use * \
        developable.acres_developable * feature.dev_pct if feature.total_redev is False \
        else flat_built_form.acres_parcel_mixed_use * developable.acres_developable

        feature.acres_parcel_mixed_w_off = flat_built_form.acres_parcel_mixed_use_with_office * \
        developable.acres_developable * feature.dev_pct if feature.total_redev is False \
        else flat_built_form.acres_parcel_mixed_use_with_office * developable.acres_developable

        feature.acres_parcel_mixed_no_off = flat_built_form.acres_parcel_mixed_use_without_office * \
        developable.acres_developable * feature.dev_pct if feature.total_redev is False \
        else flat_built_form.acres_parcel_mixed_use_without_office * developable.acres_developable

        feature.pop = flat_built_form.population_density \
                      * developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.hh = flat_built_form.household_density \
                     * developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.du = flat_built_form.dwelling_unit_density \
                     * developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.du_detsf_ll = flat_built_form.single_family_large_lot_density \
                              * developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.du_detsf_sl = flat_built_form.single_family_small_lot_density \
                              * developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.du_attsf = flat_built_form.attached_single_family_density \
                           * developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.du_mf = (flat_built_form.multifamily_2_to_4_density + flat_built_form.multifamily_5_plus_density) \
                        * developable.acres_developable * feature.dev_pct * feature.density_pct

        feature.du_mf2to4 = flat_built_form.multifamily_2_to_4_density \
                        * developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.du_mf5p = flat_built_form.multifamily_5_plus_density \
                        * developable.acres_developable * feature.dev_pct * feature.density_pct


        feature.emp = flat_built_form.employment_density \
                      * developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.emp_ret = flat_built_form.retail_density \
                          * developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.emp_retail_services = flat_built_form.retail_services_density \
                                      * developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.emp_restaurant = flat_built_form.residential_density \
                                 * developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.emp_accommodation = flat_built_form.accommodation_density \
                                    * developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.emp_arts_entertainment = flat_built_form.arts_entertainment_density \
                                         * developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.emp_other_services = flat_built_form.other_services_density \
                                     * developable.acres_developable * feature.dev_pct * feature.density_pct

        feature.emp_off = flat_built_form.office_density \
                          * developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.emp_office_services = flat_built_form.office_services_density \
                                      * developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.emp_education = flat_built_form.education_services_density \
                                * developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.emp_public_admin = flat_built_form.public_admin_density \
                                   * developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.emp_medical_services = flat_built_form.medical_services_density \
                                       * developable.acres_developable * feature.dev_pct * feature.density_pct

        feature.emp_ind = flat_built_form.industrial_density \
                          * developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.emp_wholesale = flat_built_form.wholesale_density \
                                * developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.emp_transport_warehousing = flat_built_form.transport_warehouse_density \
                                            * developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.emp_manufacturing = flat_built_form.manufacturing_density \
                                    * developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.emp_construction_utilities = flat_built_form.construction_utilities_density \
                                             * developable.acres_developable * feature.dev_pct * feature.density_pct

        feature.emp_ag = flat_built_form.agricultural_density \
                         * developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.emp_agriculture = flat_built_form.agriculture_density \
                                  * developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.emp_extraction = flat_built_form.extraction_density \
                                 * developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.emp_military = flat_built_form.armed_forces_density \
                               * developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.bldg_sqft_detsf_ll = flat_built_form.building_sqft_single_family_large_lot \
                                     * developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.bldg_sqft_detsf_sl = flat_built_form.building_sqft_single_family_small_lot \
                                     * developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.bldg_sqft_attsf = flat_built_form.building_sqft_attached_single_family \
                                  * developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.bldg_sqft_mf = (
                                   flat_built_form.building_sqft_multifamily_2_to_4 + flat_built_form.building_sqft_multifamily_5_plus) * developable.acres_developable \
                               * feature.dev_pct * feature.density_pct
        feature.bldg_sqft_retail_services = flat_built_form.building_sqft_retail_services \
                                            * developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.bldg_sqft_restaurant = flat_built_form.building_sqft_restaurant \
                                       * developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.bldg_sqft_accommodation = flat_built_form.building_sqft_accommodation \
                                          * developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.bldg_sqft_arts_entertainment = flat_built_form.building_sqft_arts_entertainment \
                                               * developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.bldg_sqft_other_services = flat_built_form.building_sqft_other_services \
                                           * developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.bldg_sqft_office_services = flat_built_form.building_sqft_office_services \
                                            * developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.bldg_sqft_public_admin = flat_built_form.building_sqft_public_admin \
                                         * developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.bldg_sqft_medical_services = flat_built_form.building_sqft_medical_services \
                                             * developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.bldg_sqft_education = flat_built_form.building_sqft_education_services \
                                      * developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.bldg_sqft_wholesale = flat_built_form.building_sqft_wholesale \
                                      * developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.bldg_sqft_transport_warehousing = flat_built_form.building_sqft_transport_warehouse \
                                                  * developable.acres_developable * feature.dev_pct * feature.density_pct

        feature.commercial_irrigated_sqft = flat_built_form.commercial_irrigated_square_feet \
                                            * developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.residential_irrigated_sqft = flat_built_form.residential_irrigated_square_feet \
                                             * developable.acres_developable * feature.dev_pct * feature.density_pct

        feature.save()

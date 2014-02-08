# coding=utf-8
# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
#
# Copyright (C) 2012 Calthorpe Associates # # This program is free software: you can redistribute it and/or modify it under the terms of the # GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; # without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.
#
# Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates.
# Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709.
# Phone: (510) 548-6800. Web: www.calthorpe.com

import datetime
from django.utils.timezone import utc
from footprint.models import FlatBuiltForm
from footprint.models.keys.keys import Keys

def update_future_scenario_feature(config_entity):
    future_scenario_class = config_entity.feature_class_of_db_entity(Keys.DB_ABSTRACT_FUTURE_SCENARIO_FEATURE)
    developable_class = config_entity.feature_class_of_db_entity(Keys.DB_ABSTRACT_DEVELOPABLE)

    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    features = future_scenario_class.objects.filter(
        updated__gt=now - datetime.timedelta(seconds=30))
    # empty_builtform = FlatBuiltForm()

    for feature in features:
        flat_built_form = FlatBuiltForm.objects.get(built_form_id=feature.built_form.id) if feature.built_form else FlatBuiltForm()
        developable = developable_class.objects.get(id=feature.id)

        # feature.built_from = feature.built_form if \
        #     feature.built_form else \
        #     empty_builtform
        feature.dirty_flag = True
        feature.refill_flag = True if developable.acres_urban > 0.5 * float(developable.acres_parcel) else False
        feature.acres_developing = developable.acres_developable
        feature.acres_developable = developable.acres_developable * feature.dev_pct
        feature.acres_parcel = (flat_built_form.acres_parcel_residential + flat_built_form.acres_parcel_employment \
                                + flat_built_form.acres_parcel_mixed_use) * developable.acres_developable \
                               * feature.dev_pct * feature.density_pct
        feature.acres_parcel_res = flat_built_form.acres_parcel_residential * developable.acres_developable \
                                   * feature.dev_pct * feature.density_pct
        feature.acres_parcel_res_detsf_ll = flat_built_form.acres_parcel_residential_single_family_large_lot * \
                                            developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.acres_parcel_res_detsf_sl = flat_built_form.acres_parcel_residential_single_family_small_lot \
                                            * developable.acres_developable * feature.dev_pct * feature.density_pct

        feature.acres_parcel_res_attsf = flat_built_form.acres_parcel_residential_attached_single_family * \
                                         developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.acres_parcel_res_mf = flat_built_form.acres_parcel_residential_multifamily * \
                                      developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.acres_parcel_emp = flat_built_form.acres_parcel_employment * developable.acres_developable \
                                   * feature.dev_pct * feature.density_pct
        feature.acres_parcel_emp_ret = flat_built_form.acres_parcel_employment_retail * developable.acres_developable \
                                       * feature.dev_pct * feature.density_pct
        feature.acres_parcel_emp_off = flat_built_form.acres_parcel_employment_office * developable.acres_developable \
                                       * feature.dev_pct * feature.density_pct
        feature.acres_parcel_emp_ind = flat_built_form.acres_parcel_employment_industrial * \
                                       developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.acres_parcel_emp_ag = flat_built_form.acres_parcel_employment_agriculture * \
                                      developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.acres_parcel_emp_mixed = flat_built_form.acres_parcel_employment_mixed * \
                                         developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.acres_parcel_mixed = flat_built_form.acres_parcel_mixed_use * developable.acres_developable \
                                     * feature.dev_pct * feature.density_pct
        feature.acres_parcel_mixed_w_off = flat_built_form.acres_parcel_mixed_use_with_office * \
                                           developable.acres_developable * feature.dev_pct * feature.density_pct
        feature.acres_parcel_mixed_no_off = flat_built_form.acres_parcel_mixed_use_without_office \
                                            * developable.acres_developable * feature.dev_pct * feature.density_pct

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


def update_end_state_feature(config_entity):
    future_scenario_class = config_entity.feature_class_of_db_entity(Keys.DB_ABSTRACT_FUTURE_SCENARIO_FEATURE)
    developable_class = config_entity.feature_class_of_db_entity(Keys.DB_ABSTRACT_DEVELOPABLE)
    base_class = config_entity.feature_class_of_db_entity(Keys.DB_ABSTRACT_BASE_FEATURE)
    end_state_class = config_entity.feature_class_of_db_entity(Keys.DB_ABSTRACT_END_STATE_FEATURE)

    features = future_scenario_class.objects.filter(dirty_flag=True)

    for feature in features:
        end_state = end_state_class.objects.get(id=feature.id)
        developable = developable_class.objects.get(id=feature.id)
        base = base_class.objects.get(id=feature.id)

        end_state.built_form_id = feature.built_form_id
        end_state.acres_parcel = feature.acres_parcel if feature.total_redev is True else \
            feature.acres_parcel - developable.acres_parcel + base.acres_parcel

        end_state.acres_parcel_res = feature.acres_parcel_res if feature.total_redev \
            is True else feature.acres_parcel_res - developable.acres_parcel_res + \
                         base.acres_parcel_res

        end_state.acres_parcel_res_detsf_ll = feature.acres_parcel_res_detsf_ll if \
            feature.total_redev is True else feature.acres_parcel_res_detsf_ll \
                                             - developable.acres_parcel_res_detsf_ll + \
                                             base.acres_parcel_res_detsf_ll

        end_state.acres_parcel_res_detsf_sl = feature.acres_parcel_res_detsf_sl if \
            feature.total_redev is True else feature.acres_parcel_res_detsf_sl \
                                             - developable.acres_parcel_res_detsf_sl + \
                                             base.acres_parcel_res_detsf_sl

        end_state.acres_parcel_res_attsf = feature.acres_parcel_res_attsf if \
            feature.total_redev is True else feature.acres_parcel_res_attsf - \
                                             developable.acres_parcel_res_attsf + \
                                             base.acres_parcel_res_attsf

        end_state.acres_parcel_res_mf = feature.acres_parcel_res_mf if feature.total_redev \
            is True else feature.acres_parcel_res_mf - developable.acres_parcel_res_mf + \
                         base.acres_parcel_res_mf

        end_state.acres_parcel_emp = feature.acres_parcel_emp if feature.total_redev \
            is True else feature.acres_parcel_emp - developable.acres_parcel_emp + \
                         base.acres_parcel_emp

        end_state.acres_parcel_emp_ret = feature.acres_parcel_emp_ret if feature.total_redev is True else \
            feature.acres_parcel_emp_ret - developable.acres_parcel_emp_ret + base.acres_parcel_emp_ret
        end_state.acres_parcel_emp_off = feature.acres_parcel_emp_off if feature.total_redev is True else \
            feature.acres_parcel_emp_off - developable.acres_parcel_emp_off + base.acres_parcel_emp_off
        end_state.acres_parcel_emp_ind = feature.acres_parcel_emp_ind if feature.total_redev is True else \
            feature.acres_parcel_emp_ind - developable.acres_parcel_emp_ind + base.acres_parcel_emp_ind

        end_state.acres_parcel_emp_ag = feature.acres_parcel_emp_ag if feature.total_redev is True else \
            feature.acres_parcel_emp_ag - developable.acres_parcel_emp_ag + base.acres_parcel_emp_ag
        end_state.acres_parcel_emp_mixed = feature.acres_parcel_emp_mixed if feature.total_redev is True else \
            feature.acres_parcel_emp_mixed - developable.acres_parcel_emp_mixed + base.acres_parcel_emp_mixed
        end_state.acres_parcel_mixed = feature.acres_parcel_mixed if feature.total_redev is True else \
            feature.acres_parcel_mixed - developable.acres_parcel_mixed + base.acres_parcel_mixed
        end_state.acres_parcel_mixed_w_off = feature.acres_parcel_mixed_w_off if feature.total_redev is True else \
            feature.acres_parcel_mixed_w_off - developable.acres_parcel_mixed_w_off + base.acres_parcel_mixed_w_off
        end_state.acres_parcel_mixed_no_off = feature.acres_parcel_mixed_no_off if feature.total_redev is True else \
            feature.acres_parcel_mixed_no_off - developable.acres_parcel_mixed_no_off + base.acres_parcel_mixed_no_off

        end_state.pop = feature.pop if feature.total_redev is True else \
            feature.pop - developable.pop + base.pop
        end_state.hh = feature.hh if feature.total_redev is True else \
            feature.hh - developable.hh + base.hh
        end_state.du = feature.du if feature.total_redev is True else \
            feature.du - developable.du + base.du
        end_state.du_detsf_ll = feature.du_detsf_ll if feature.total_redev is True else \
            feature.du_detsf_ll - developable.du_detsf_ll + base.du_detsf_ll
        end_state.du_detsf_sl = feature.du_detsf_sl if feature.total_redev is True else \
            feature.du_detsf_sl - developable.du_detsf_sl + base.du_detsf_sl
        end_state.du_attsf = feature.du_attsf if feature.total_redev is True else \
            feature.du_attsf - developable.du_attsf + base.du_attsf
        end_state.du_mf = feature.du_mf if feature.total_redev is True else \
            feature.du_mf - developable.du_mf + base.du_mf

        end_state.emp = feature.emp if feature.total_redev is True else \
            feature.emp - developable.emp + base.emp
        end_state.emp_ret = feature.emp_ret if feature.total_redev is True else \
            feature.emp_ret - developable.emp_ret + base.emp_ret
        end_state.emp_retail_services = feature.emp_retail_services if feature.total_redev is True else \
            feature.emp_retail_services - developable.emp_retail_services + base.emp_retail_services
        end_state.emp_restaurant = feature.emp_restaurant if feature.total_redev is True else \
            feature.emp_restaurant - developable.emp_restaurant + base.emp_restaurant
        end_state.emp_accommodation = feature.emp_accommodation if feature.total_redev is True else \
            feature.emp_accommodation - developable.emp_accommodation + base.emp_accommodation
        end_state.emp_arts_entertainment = feature.emp_arts_entertainment if feature.total_redev is True else \
            feature.emp_arts_entertainment - developable.emp_arts_entertainment + base.emp_arts_entertainment
        end_state.emp_other_services = feature.emp_other_services if feature.total_redev is True else \
            feature.emp_other_services - developable.emp_other_services + base.emp_other_services

        end_state.emp_off = feature.emp_off if feature.total_redev is True else \
            feature.emp_off - developable.emp_off + base.emp_off
        end_state.emp_office_services = feature.emp_office_services if feature.total_redev is True else \
            feature.emp_office_services - developable.emp_office_services + base.emp_office_services
        end_state.emp_education = feature.emp_education if feature.total_redev is True else \
            feature.emp_education - developable.emp_education + base.emp_education
        end_state.emp_public_admin = feature.emp_public_admin if feature.total_redev is True else \
            feature.emp_public_admin - developable.emp_public_admin + base.emp_public_admin
        end_state.emp_medical_services = feature.emp_medical_services if feature.total_redev is True else \
            feature.emp_medical_services - developable.emp_medical_services + base.emp_medical_services

        end_state.emp_ind = feature.emp_ind if feature.total_redev is True else \
            feature.emp_ind - developable.emp_ind + base.emp_ind
        end_state.emp_wholesale = feature.emp_wholesale if feature.total_redev is True else \
            feature.emp_wholesale - developable.emp_wholesale + base.emp_wholesale
        end_state.emp_transport_warehousing = feature.emp_transport_warehousing if feature.total_redev is True else \
            feature.emp_transport_warehousing - developable.emp_transport_warehousing + base.emp_transport_warehousing
        end_state.emp_manufacturing = feature.emp_manufacturing if feature.total_redev is True else \
            feature.emp_manufacturing - developable.emp_manufacturing + base.emp_manufacturing
        end_state.emp_construction_utilities = feature.emp_construction_utilities if feature.total_redev is True else \
            feature.emp_construction_utilities - (
                developable.emp_construction + developable.emp_utilities) + \
            (base.emp_construction + base.emp_utilities)

        end_state.emp_ag = feature.emp_ag if feature.total_redev is True else \
            feature.emp_ag - developable.emp_ag + base.emp_ag

        end_state.emp_agriculture = feature.emp_agriculture if feature.total_redev is True else \
            feature.emp_agriculture - developable.emp_agriculture + base.emp_agriculture

        end_state.emp_extraction = feature.emp_extraction if feature.total_redev is True else \
            feature.emp_extraction - developable.emp_extraction + base.emp_extraction

        end_state.emp_military = feature.emp_military if feature.total_redev is True else \
            feature.emp_military - developable.emp_military + base.emp_military

        end_state.bldg_sqft_detsf_ll = feature.bldg_sqft_detsf_ll if feature.total_redev is True else \
            feature.bldg_sqft_detsf_ll - developable.bldg_sqft_detsf_ll + base.bldg_sqft_detsf_ll

        end_state.bldg_sqft_detsf_sl = feature.bldg_sqft_detsf_sl if feature.total_redev is True else \
            feature.bldg_sqft_detsf_sl - developable.bldg_sqft_detsf_sl + base.bldg_sqft_detsf_sl
        end_state.bldg_sqft_attsf = feature.bldg_sqft_attsf if feature.total_redev is True else \
            feature.bldg_sqft_attsf - developable.bldg_sqft_attsf + base.bldg_sqft_attsf
        end_state.bldg_sqft_mf = feature.bldg_sqft_mf if feature.total_redev is True else \
            feature.bldg_sqft_mf - developable.bldg_sqft_mf + base.bldg_sqft_mf

        end_state.bldg_sqft_retail_services = feature.bldg_sqft_retail_services if feature.total_redev is True else \
            feature.bldg_sqft_retail_services - developable.bldg_sqft_retail_services + base.bldg_sqft_retail_services

        end_state.bldg_sqft_restaurant = feature.bldg_sqft_restaurant if feature.total_redev is True else \
            feature.bldg_sqft_restaurant - developable.bldg_sqft_restaurant + base.bldg_sqft_restaurant
        end_state.bldg_sqft_accommodation = feature.bldg_sqft_accommodation if feature.total_redev is True else \
            feature.bldg_sqft_accommodation - developable.bldg_sqft_accommodation + base.bldg_sqft_accommodation
        end_state.bldg_sqft_arts_entertainment = feature.bldg_sqft_arts_entertainment if feature.total_redev is True else \
            feature.bldg_sqft_arts_entertainment - developable.bldg_sqft_arts_entertainment + base.bldg_sqft_arts_entertainment
        end_state.bldg_sqft_other_services = feature.bldg_sqft_other_services if feature.total_redev is True else \
            feature.bldg_sqft_other_services - developable.bldg_sqft_other_services + base.bldg_sqft_other_services
        end_state.bldg_sqft_office_services = feature.bldg_sqft_office_services if feature.total_redev is True else \
            feature.bldg_sqft_office_services - developable.bldg_sqft_office_services + base.bldg_sqft_office_services
        end_state.bldg_sqft_public_admin = feature.bldg_sqft_public_admin if feature.total_redev is True else \
            feature.bldg_sqft_public_admin - developable.bldg_sqft_public_admin + base.bldg_sqft_public_admin
        end_state.bldg_sqft_medical_services = feature.bldg_sqft_medical_services if feature.total_redev is True else \
            feature.bldg_sqft_medical_services - developable.bldg_sqft_medical_services + base.bldg_sqft_medical_services
        end_state.bldg_sqft_education = feature.bldg_sqft_education if feature.total_redev is True else \
            feature.bldg_sqft_education - developable.bldg_sqft_education + base.bldg_sqft_education
        end_state.bldg_sqft_wholesale = feature.bldg_sqft_wholesale if feature.total_redev is True else \
            feature.bldg_sqft_wholesale - developable.bldg_sqft_wholesale + base.bldg_sqft_wholesale
        end_state.bldg_sqft_transport_warehousing = feature.bldg_sqft_transport_warehousing if feature.total_redev is True else \
            feature.bldg_sqft_transport_warehousing - developable.bldg_sqft_transport_warehousing + base.bldg_sqft_transport_warehousing
        end_state.commercial_irrigated_sqft = feature.commercial_irrigated_sqft if feature.total_redev is True else \
            feature.commercial_irrigated_sqft - developable.commercial_irrigated_sqft + base.commercial_irrigated_sqft
        end_state.residential_irrigated_sqft = feature.residential_irrigated_sqft if feature.total_redev is True else \
            feature.residential_irrigated_sqft - developable.residential_irrigated_sqft + base.residential_irrigated_sqft

        end_state.save()


def update_increment_feature(config_entity):
    future_scenario_class = config_entity.feature_class_of_db_entity(Keys.DB_ABSTRACT_FUTURE_SCENARIO_FEATURE)
    end_state_class = config_entity.feature_class_of_db_entity(Keys.DB_ABSTRACT_END_STATE_FEATURE)
    base_class = config_entity.feature_class_of_db_entity(Keys.DB_ABSTRACT_BASE_FEATURE)
    increment_class = config_entity.feature_class_of_db_entity(Keys.DB_ABSTRACT_INCREMENT_FEATURE)

    features = future_scenario_class.objects.filter(dirty_flag=True)

    for feature in features:
        increment = increment_class.objects.get(geography__id=feature.geography.id)
        end_state = end_state_class.objects.get(id=feature.id)
        base = base_class.objects.get(id=feature.id)
        increment.pop = end_state.pop - base.pop
        increment.hh = end_state.hh - base.hh
        increment.du = end_state.du - base.du
        increment.emp = end_state.emp - base.emp
        increment.du_detsf = end_state.du_detsf - base.du_detsf
        increment.du_detsf_ll = end_state.du_detsf_ll - base.du_detsf_ll
        increment.du_detsf_sl = end_state.du_detsf_sl - base.du_detsf_sl
        increment.du_attsf = end_state.du_attsf - base.du_attsf
        increment.du_mf = end_state.du_mf - base.du_mf

        increment.emp_ret = end_state.emp_ret - base.emp_ret
        increment.emp_retail_services = end_state.emp_retail_services - base.emp_retail_services
        increment.emp_restaurant = end_state.emp_restaurant - base.emp_restaurant
        increment.emp_accommodation = end_state.emp_accommodation - base.emp_accommodation
        increment.emp_arts_entertainment = end_state.emp_arts_entertainment - base.emp_arts_entertainment
        increment.emp_other_services = end_state.emp_other_services - base.emp_other_services

        increment.emp_off = end_state.emp_off - base.emp_off
        increment.emp_office_services = end_state.emp_office_services - base.emp_office_services
        increment.emp_education = end_state.emp_education - base.emp_education
        increment.emp_public_admin = end_state.emp_public_admin - base.emp_public_admin
        increment.emp_medical_services = end_state.emp_medical_services - base.emp_medical_services

        increment.emp_ind = end_state.emp_ind - base.emp_ind
        increment.emp_wholesale = end_state.emp_wholesale - base.emp_wholesale
        increment.emp_transport_warehousing = end_state.emp_transport_warehousing - base.emp_transport_warehousing
        increment.emp_manufacturing = end_state.emp_manufacturing - base.emp_manufacturing
        increment.emp_utilities = end_state.emp_utilities - base.emp_utilities
        increment.emp_construction = end_state.emp_construction - base.emp_construction

        increment.emp_ag = end_state.emp_ag - base.emp_ag
        increment.emp_agriculture = end_state.emp_agriculture - base.emp_agriculture
        increment.emp_extraction = end_state.emp_extraction - base.emp_extraction

        increment.emp_military = end_state.emp_military - base.emp_military

        feature.dirty_flag = False

        increment.save()
        feature.save()


def run_core(config_entity):
    update_future_scenario_feature(config_entity)
    update_end_state_feature(config_entity)
    update_increment_feature(config_entity)
    from footprint.models.signals import post_analytic_run
    post_analytic_run.send(sender=config_entity.__class__, config_entity=config_entity, module='core')

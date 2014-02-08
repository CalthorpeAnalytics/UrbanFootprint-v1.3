from footprint.main.models import FlatBuiltForm
from footprint.main.models.keys.keys import Keys
from footprint.main.utils.query_parsing import annotated_related_feature_class_pk_via_geographies

__author__ = 'calthorpe'


def update_increment_feature(config_entity):
    future_scenario_class = config_entity.feature_class_of_db_entity_key(Keys.DB_ABSTRACT_FUTURE_SCENARIO_FEATURE)
    end_state_class = config_entity.feature_class_of_db_entity_key(Keys.DB_ABSTRACT_END_STATE_FEATURE)
    base_class = config_entity.feature_class_of_db_entity_key(Keys.DB_ABSTRACT_BASE_FEATURE)
    increment_class = config_entity.feature_class_of_db_entity_key(Keys.DB_ABSTRACT_INCREMENT_FEATURE)
    developable_class = config_entity.feature_class_of_db_entity_key(Keys.DB_ABSTRACT_DEVELOPABLE)

    features = future_scenario_class.objects.filter(dirty_flag=True)


    annotated_features = annotated_related_feature_class_pk_via_geographies(features, config_entity, [Keys.DB_ABSTRACT_DEVELOPABLE, Keys.DB_ABSTRACT_BASE_FEATURE, Keys.DB_ABSTRACT_END_STATE_FEATURE, Keys.DB_ABSTRACT_INCREMENT_FEATURE])

    for feature in annotated_features:
        built_form = FlatBuiltForm.objects.get(built_form_id=feature.built_form.id) \
            if feature.built_form \
            else FlatBuiltForm()

        increment = increment_class.objects.get(id=feature.increments)
        end_state = end_state_class.objects.get(id=feature.end_state)
        base = base_class.objects.get(id=feature.base_feature)
        developable = developable_class.objects.get(id=feature.developable)

        increment.land_development_category = calculate_land_development_category(base, built_form)

        if developable.acres_greenfield < developable.acres_urban:
            increment.refill_flag = 1
        else:
            increment.refill_flag = None

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


def calculate_land_development_category(base, built_form):

    try:

        if built_form.intersection_density >= 150 and built_form.employment_density > 70:
            land_development_category = 'urban'

        elif built_form.intersection_density >= 150 and built_form.dwelling_unit_density > 45:
            land_development_category = 'urban'

        elif built_form.intersection_density >= 150 and built_form.employment_density <= 70:
            land_development_category = 'compact'

        elif built_form.intersection_density >= 150 and built_form.dwelling_unit_density <= 45:
            land_development_category = 'compact'

        elif built_form.intersection_density < 150:
            land_development_category = 'standard'

        else:
            land_development_category = None
    except:
        raise Exception
        print 'failure to calculate land development category'
    return land_development_category


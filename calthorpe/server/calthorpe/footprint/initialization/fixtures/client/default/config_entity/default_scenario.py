from footprint.initialization.fixture import ScenarioFixture, ProjectFixture, project_specific_project_fixtures
from footprint.initialization.fixtures.client.default.default_mixin import DefaultMixin
from footprint.initialization.utils import resolve_fixture
from footprint.lib.functions import merge, flat_map
from footprint.models import FutureScenarioFeature, CoreIncrementFeature, CoreEndStateFeature
from footprint.models.config.scenario import FutureScenario
from footprint.models.keys.keys import Keys

__author__ = 'calthorpe'


class DefaultScenarioFixture(DefaultMixin, ScenarioFixture):
    def feature_class_lookup(self):
        # Get the client project fixture (or the default region if the former doesn't exist)
        project_class_lookup = merge(*map(lambda project_fixture: project_fixture.feature_class_lookup(), project_specific_project_fixtures()))
        return merge(project_class_lookup, {
            # TODO automate
            Keys.DB_ABSTRACT_FUTURE_SCENARIO_FEATURE: FutureScenarioFeature,
            Keys.DB_ABSTRACT_INCREMENT_FEATURE: CoreIncrementFeature,
            Keys.DB_ABSTRACT_END_STATE_FEATURE: CoreEndStateFeature
        })

    def default_db_entity_setups(self):
        """
            Scenarios define DbEntities specific to the Scenario. Creates a list a dictionary of configuration functionality. Some DbEntities have associated base classes for
            which a dynamic model subclass is created. Some of these subclasses also have associated fields which
            refer to other dynamically created subclasses
        :return:
        """
        config_entity = self.config_entity

        return self.matching_scope([

                                   config_entity.create_db_entity_and_subclass(
                                       class_scope=FutureScenario,
                                       key=Keys.DB_ABSTRACT_FUTURE_SCENARIO_FEATURE,
                                       base_class=FutureScenarioFeature,
                                       import_from_db_entity_key=Keys.DB_ABSTRACT_BASE_FEATURE,
                                       map_layer=True,
                                   ),
                                   config_entity.create_db_entity_and_subclass(
                                       class_scope=FutureScenario,
                                       key=Keys.DB_ABSTRACT_INCREMENT_FEATURE,
                                       base_class=CoreIncrementFeature,
                                       import_from_db_entity_key=Keys.DB_ABSTRACT_BASE_FEATURE,
                                       map_layer=False,
                                   ),
                                   config_entity.create_db_entity_and_subclass(
                                       class_scope=FutureScenario,
                                       key=Keys.DB_ABSTRACT_END_STATE_FEATURE,
                                       base_class=CoreEndStateFeature,
                                       import_from_db_entity_key=Keys.DB_ABSTRACT_BASE_FEATURE,
                                       import_fields=['geography_id', 'wkb_geometry', 'built_form_id',
                                                      'acres_parcel', 'acres_parcel_res', 'acres_parcel_res_detsf',
                                                      'acres_parcel_res_detsf_ll', 'acres_parcel_res_detsf_sl',
                                                      'acres_parcel_res_attsf', 'acres_parcel_res_mf',
                                                      'acres_parcel_emp',
                                                      'acres_parcel_emp_ret', 'acres_parcel_emp_off',
                                                      'acres_parcel_emp_ind',
                                                      'acres_parcel_emp_ag', 'acres_parcel_mixed',
                                                      'acres_parcel_mixed_w_off',
                                                      'acres_parcel_mixed_no_off', 'acres_parcel_no_use',
                                                      'acres_parcel_emp_military', 'pop', 'hh', 'du', 'du_detsf',
                                                      'du_detsf_ll', 'du_detsf_sl', 'du_attsf', 'du_mf', 'emp',
                                                      'emp_ret',
                                                      'emp_retail_services', 'emp_restaurant', 'emp_accommodation',
                                                      'emp_arts_entertainment', 'emp_other_services', 'emp_off',
                                                      'emp_office_services', 'emp_education', 'emp_public_admin',
                                                      'emp_medical_services', 'emp_ind', 'emp_wholesale',
                                                      'emp_transport_warehousing', 'emp_manufacturing',
                                                      'emp_utilities', 'emp_construction',
                                                      'emp_ag', 'emp_agriculture', 'emp_extraction', 'emp_military',
                                                      'bldg_sqft_detsf_ll',
                                                      'bldg_sqft_detsf_sl', 'bldg_sqft_attsf', 'bldg_sqft_mf',
                                                      'bldg_sqft_retail_services', 'bldg_sqft_restaurant',
                                                      'bldg_sqft_accommodation',
                                                      'bldg_sqft_arts_entertainment', 'bldg_sqft_other_services',
                                                      'bldg_sqft_office_services',
                                                      'bldg_sqft_public_admin', 'bldg_sqft_medical_services',
                                                      'bldg_sqft_education',
                                                      'bldg_sqft_wholesale', 'bldg_sqft_transport_warehousing',
                                                      'commercial_irrigated_sqft',
                                                      'residential_irrigated_sqft'],
                                       map_layer=False,
                                   )
                               ],
                               class_scope=self.config_entity.__class__)


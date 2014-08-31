# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
#
# Copyright (C) 2014 Calthorpe Associates
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com

from footprint.client.configuration.fixture import ResultConfigurationFixture
from footprint.client.configuration.default.default_mixin import DefaultMixin
from footprint.main.models.geospatial.db_entity_keys import DbEntityKey
from footprint.main.models.keys.content_type_key import ContentTypeKey
from footprint.main.publishing.result_initialization import ResultConfiguration, ResultLibraryConfiguration, \
    ResultLibraryKey, ResultKey, ResultMediumKey, ResultSort
from footprint.main.models import Scenario, Medium
from footprint.main.models.config.scenario import BaseScenario, FutureScenario
from footprint.main.utils.utils import create_media_subdir


class DefaultResultConfigurationFixtures(DefaultMixin, ResultConfigurationFixture):

    @property
    def employment_breakdown_query(self):
        return 'SELECT SUM(emp_ret) as emp_ret__sum, '\
            'SUM(emp_off) as emp_off__sum, '\
            'SUM(emp_ind + emp_ag) as emp_ind__sum, '\
            'SUM(emp_pub) as emp_pub__sum, '\
            'SUM(emp_military) as emp_military__sum FROM %({0})s'.format

    def result_libraries(self):
        """
            Used to update or create ResultLibraries per ConfigEntity instance
            Returns the result library(ies) scoped for the class of self.config_entity
        :return:
        """
        return self.matching_scope([
            ResultLibraryConfiguration(
                class_scope=Scenario,
                key=ResultLibraryKey.DEFAULT,
                name='{0} Default Result Library',
                description='The default result library for {0}'
            )],
            class_scope=self.config_entity and self.config_entity.__class__
        )

    def results(self):
        """
            Used to update or create Results per ConfigEntity instance
            Returns the result library(ies) scoped for the class of self.config_entity.
            The Result will belong to the ResultLibrary specified by result_library_key

            To update this in the DB, use footprint_init --skip --result
        :return:
        """
        return self.matching_scope([
            # Basic Core result query that summarizes increments

            ResultConfiguration(
                class_scope=BaseScenario,
                result_type='bar_graph',
                result_library_key=ResultLibraryKey.DEFAULT,
                result_db_entity_key=ResultKey.BASE_EMPLOYMENT_BY_TYPE,
                source_db_entity_key=DbEntityKey.BASE,

                name='Base: Employment by Sector',
                attributes=['retail', 'office', 'industrial', 'public', 'other'],
                db_column_lookup=dict(
                    retail='emp_ret',
                    office='emp_off',
                    industrial='emp_ind',
                    public='emp_pub',
                    other='emp_military',
                ),
                labels=['Retail', 'Office', 'Industrial', 'Public', 'Other'],
                stackable=True,
                is_stacked=False,
                create_query=lambda result_config: self.employment_breakdown_query(DbEntityKey.BASE),
                sort_priority=ResultSort.BASE
            ),

            ResultConfiguration(
                class_scope=BaseScenario,
                result_type='bar_graph',
                result_library_key=ResultLibraryKey.DEFAULT,
                result_db_entity_key=ResultKey.BASE_DWELLING_UNITS_BY_TYPE,
                source_db_entity_key=DbEntityKey.BASE,

                name='Base: Dwelling Units by Type',
                attributes=['single_family', 'attached', 'multifamily'],
                db_column_lookup=dict(
                    single_family='du_detsf',
                    attached='du_attsf',
                    multifamily='du_mf'
                ),
                labels=['Single Family', 'Attached', 'Multifamily'],
                stackable=True,
                is_stacked=False,
                create_query=self.simple_aggregate,
                sort_priority=ResultSort.BASE
             ),

            ResultConfiguration(
                class_scope=FutureScenario,
                result_library_key=ResultLibraryKey.DEFAULT,
                result_type='bar_graph',
                result_db_entity_key=ResultKey.INCREMENTS,
                source_db_entity_key=DbEntityKey.INCREMENT,

                name='Increments: All Metrics',
                attributes=['population', 'dwelling_units', 'employment'],
                db_column_lookup=dict(
                    population='pop',
                    dwelling_units='du',
                    employment='emp'
                ),
                extent_lookup=dict(
                    population=dict(min=-25000, max=25000),
                    dwelling_units=dict(min=-2500, max=2500),
                    employment=dict(min=-2500, max=2500),
                ),
                labels=['Population', 'Dwelling Units', 'Employment'],
                stackable=False,
                is_stacked=False,
                create_query=self.simple_aggregate,
                sort_priority=ResultSort.FUTURE
            ),

            # DB Entity Core result query that summarizes dwellings by type
            ResultConfiguration(
                class_scope=FutureScenario,
                result_library_key=ResultLibraryKey.DEFAULT,
                result_type='bar_graph',
                result_db_entity_key=ResultKey.INCREMENTS_DWELLING_UNITS_BY_TYPE,
                source_db_entity_key=DbEntityKey.INCREMENT,

                name='Increments: Dwelling Units by Type',
                attributes=['single_family_large_lot', 'single_family_small_lot', 'multifamily', 'attached_single_family'],
                db_column_lookup=dict(
                    single_family_large_lot='du_detsf_ll',
                    single_family_small_lot='du_detsf_sl',
                    multifamily='du_mf',
                    attached_single_family='du_attsf',
                ),
                labels=['SF Large Lot', 'SF Small Lot', 'MF', 'Attached SF'],
                stackable=False,
                is_stacked=False,
                create_query=self.simple_aggregate,
                sort_priority=ResultSort.FUTURE
            ),
            ResultConfiguration(
                class_scope=FutureScenario,
                result_library_key=ResultLibraryKey.DEFAULT,
                result_type='bar_graph',
                result_db_entity_key=ResultKey.END_STATE_DWELLING_UNITS_BY_TYPE,
                source_db_entity_key=DbEntityKey.END_STATE,

                name='End State: Dwelling Units by Type',
                attributes=['single_family_large_lot', 'single_family_small_lot', 'multifamily', 'attached_single_family'],
                db_column_lookup=dict(
                    single_family_large_lot='du_detsf_ll',
                    single_family_small_lot='du_detsf_sl',
                    multifamily='du_mf',
                    attached_single_family='du_attsf',
                ),
                labels=['SF Large Lot', 'SF Small Lot', 'MF', 'Attached SF'],
                stackable=True,
                is_stacked=False,
                show_attrs_as_percents=True,
                create_query=self.simple_aggregate,
                sort_priority=ResultSort.FUTURE
            ),
            ResultConfiguration(
                class_scope=FutureScenario,
                result_library_key=ResultLibraryKey.DEFAULT,
                result_type='bar_graph',
                result_db_entity_key=ResultKey.INCREMENTS_EMPLOYMENT_BY_TYPE,
                source_db_entity_key=DbEntityKey.INCREMENT,

                name='Increments: Employment by Sector',
                attributes=['retail', 'office', 'industrial', 'public', 'other'],
                db_column_lookup=dict(
                    retail='emp_ret',
                    office='emp_off',
                    industrial='emp_ind',
                    public='emp_pub',
                    other='emp_military',
                ),
                labels=['Retail', 'Office', 'Industrial', 'Public', 'Other'],
                stackable=False,
                is_stacked=False,
                create_query=lambda result_config: self.employment_breakdown_query(DbEntityKey.INCREMENT),
                sort_priority=ResultSort.FUTURE
            ),
            ResultConfiguration(
                class_scope=FutureScenario,
                result_library_key=ResultLibraryKey.DEFAULT,
                result_type='bar_graph',
                result_db_entity_key=ResultKey.END_STATE_EMPLOYMENT_BY_TYPE,
                source_db_entity_key=DbEntityKey.END_STATE,

                name='End State: Employment by Sector',
                attributes=['retail', 'office', 'industrial', 'public', 'other'],
                db_column_lookup=dict(
                    retail='emp_ret',
                    office='emp_off',
                    industrial='emp_ind',
                    public='emp_pub',
                    other='emp_military',
                ),
                labels=['Retail', 'Office', 'Industrial', 'Public', 'Other'],
                stackable=True,
                is_stacked=False,
                create_query=lambda result_config: self.employment_breakdown_query(DbEntityKey.END_STATE),
                sort_priority=ResultSort.FUTURE
            ),

            ResultConfiguration(
                class_scope=FutureScenario,
                result_library_key=ResultLibraryKey.DEFAULT,
                result_type='analytic_bars',
                result_db_entity_key=ResultKey.INCREMENTS_BARS,
                source_db_entity_key=DbEntityKey.END_STATE,

                name='Results Increments',
                attributes=['population', 'dwelling_units', 'employment'],
                db_column_lookup=dict(
                    population='pop',
                    dwelling_units='du',
                    employment='emp'
                ),
                extent_lookup=dict(
                    population=dict(min=0, max=5000000),
                    dwelling_units=dict(min=0, max=1000000),
                    employment=dict(min=0, max=1000000)
                ),
                labels=['Population', 'Dwelling Units', 'Employment'],
                stackable=False,
                is_stacked=False,
                create_query=self.simple_aggregate,
                sort_priority=ResultSort.FUTURE
            ),
            ResultConfiguration(
                class_scope=FutureScenario,
                result_library_key=ResultLibraryKey.DEFAULT,
                result_type='analytic_result',
                result_db_entity_key=ResultKey.FISCAL,
                source_db_entity_key=DbEntityKey.FISCAL,

                name='Fiscal',
                attributes=['capital_costs', 'operations_maintenance', 'revenue'],
                db_column_lookup=dict(
                    capital_costs='residential_capital_costs',
                    operations_maintenance='residential_operations_maintenance_costs',
                    revenue='residential_revenue'
                ),
                labels=['capital_costs', 'operations_maintenance', 'revenue'],
                stackable=False,
                is_stacked=False,
                create_query=self.simple_aggregate,
                sort_priority=ResultSort.FUTURE
            ),
            ResultConfiguration(
                class_scope=Scenario,
                result_type='analytic_result',
                result_library_key=ResultLibraryKey.DEFAULT,
                result_db_entity_key=ResultKey.VMT,
                source_db_entity_key=DbEntityKey.VMT,

                name='VMT',
                attributes=['annual_vmt', 'daily_vmt', 'daily_vmt_per_hh', 'annual_vmt_per_capita'],
                db_column_lookup=dict(
                    annual_vmt='vmt_annual_w_trucks',
                    daily_vmt='vmt_daily_w_trucks',
                    daily_vmt_per_hh='vmt_daily_per_hh',
                    annual_vmt_per_capita='vmt_annual_per_capita'
                ),
                labels=['Annual VMT', 'Daily VMT', 'Daily VMT Per HH', 'Annual VMT Per Capita'],
                stackable=False,
                is_stacked=False,
                create_query=lambda result_config: 'SELECT SUM(vmt_annual_w_trucks) as annual_vmt__sum, SUM(vmt_daily_w_trucks) as daily_vmt__sum, Case when SUM(hh) > 0 then SUM(vmt_daily_w_trucks) / SUM(hh) else 0 end as daily_vmt_per_hh__sum, Case when SUM(hh) > 0 then SUM(vmt_daily_w_trucks) * 350 / SUM(hh) else 0 end as annual_vmt_per_hh__sum, Case when SUM(pop) > 0 then SUM(vmt_daily_w_trucks) * 350 / SUM(pop) else 0 end as annual_vmt_per_capita__sum, Case when SUM(pop) > 0 then SUM(vmt_daily_w_trucks) / SUM(pop) else 0 end as daily_vmt_per_capita__sum, Case when SUM(emp) > 0 then SUM(vmt_daily_w_trucks) / SUM(emp) else 0 end as daily_vmt_per_emp__sum, Case when SUM(emp) > 0 then SUM(vmt_daily_w_trucks) * 350 / SUM(emp) else 0 end as annual_vmt_per_emp__sum   FROM %({0})s'.format(DbEntityKey.VMT),
                sort_priority=ResultSort.FUTURE
            ),
            ResultConfiguration(
                class_scope=Scenario,
                result_type='analytic_result',
                result_library_key=ResultLibraryKey.DEFAULT,
                result_db_entity_key=ResultKey.ENERGY,
                source_db_entity_key=DbEntityKey.ENERGY,

                name='Energy',
                attributes=['total_gas_use', 'total_electricity_use', 'residential_gas_use', 'residential_electricity_use', 'commercial_gas_use', 'commercial_electricity_use'],
                db_column_lookup=dict(
                    total_gas_use='total_gas_use',
                    total_electricity_use='total_electricity_use',
                    residential_gas_use='residential_gas_use',
                    residential_electricity_use='residential_electricity_use',
                    commercial_gas_use='commercial_gas_use',
                    commercial_electricity_use='commercial_electricity_use'
                ),
                labels=['total_gas_use', 'total_electricity_use', 'residential_gas_use', 'residential_electricity_use', 'commercial_gas_use', 'commercial_electricity_use'],
                stackable=False,
                is_stacked=False,
                create_query=lambda result_config: 'SELECT SUM(total_gas_use) as total_gas_use__sum, SUM(total_electricity_use) as total_electricity_use__sum, SUM(residential_gas_use) as residential_gas_use__sum, SUM(residential_electricity_use) as residential_electricity_use__sum, SUM(commercial_gas_use) as commercial_gas_use__sum, SUM(commercial_electricity_use) as commercial_electricity_use__sum, Case when SUM(hh) > 0 then SUM(residential_gas_use) / SUM(hh) else 0 end as residenital_per_hh_gas_use__sum, Case when SUM(hh) > 0 then SUM(residential_electricity_use) / SUM(hh) else 0 end as residenital_per_hh_electricity_use__sum, Case when SUM(total_commercial_sqft) > 0 then SUM(commercial_gas_use) / SUM(emp) else 0 end as commercial_per_emp_gas_use__sum, Case when SUM(total_commercial_sqft) > 0 then SUM(commercial_electricity_use) / SUM(emp) else 0 end as commercial_per_emp_electricity_use__sum FROM %({0})s'.format(DbEntityKey.ENERGY),
                sort_priority=ResultSort.FUTURE
            ),
            ResultConfiguration(
                class_scope=FutureScenario,
                result_type='analytic_result',
                result_library_key=ResultLibraryKey.DEFAULT,
                result_db_entity_key=ResultKey.AGRICULTURE,
                source_db_entity_key=DbEntityKey.FUTURE_AGRICULTURE,

                name='Agriculture',
                attributes=['crop_yield', 'water_consumption', 'labor_force', 'truck_trips', 'production_cost', 'market_value'],
                db_column_lookup=dict(
                    crop_yield='crop_yield',
                    water_consumption='water_consumption',
                    labor_force='labor_force',
                    truck_trips='truck_trips',
                    production_cost='production_cost',
                    market_value='market_value'
                ),
                labels=['crop_yield', 'water_consumption', 'labor_force', 'truck_trips', 'production_cost', 'market_value'],
                stackable=False,
                is_stacked=False,
                create_query=self.simple_aggregate,
                sort_priority=ResultSort.FUTURE
            ),
            ResultConfiguration(
                class_scope=BaseScenario,
                result_type='analytic_result',
                result_library_key=ResultLibraryKey.DEFAULT,
                result_db_entity_key=ResultKey.AGRICULTURE,
                source_db_entity_key=DbEntityKey.BASE_AGRICULTURE,

                name='Agriculture',
                attributes=['crop_yield', 'water_consumption', 'labor_force', 'truck_trips', 'production_cost', 'market_value'],
                db_column_lookup=dict(
                    crop_yield='crop_yield',
                    water_consumption='water_consumption',
                    labor_force='labor_force',
                    truck_trips='truck_trips',
                    production_cost='production_cost',
                    market_value='market_value'
                ),
                labels=['crop_yield', 'water_consumption', 'labor_force', 'truck_trips', 'production_cost', 'market_value'],
                stackable=False,
                is_stacked=False,
                create_query=self.simple_aggregate,
                sort_priority=ResultSort.BASE
            ),
            ResultConfiguration(
                class_scope=Scenario,
                result_type='analytic_result',
                result_library_key=ResultLibraryKey.DEFAULT,
                result_db_entity_key=ResultKey.WATER,
                source_db_entity_key=DbEntityKey.WATER,

                name='Water',
                attributes=['total_water_use', 'residential_water_use', 'commercial_water_use',
                            'residential_indoor_water_use', 'residential_outdoor_water_use',
                            'commercial_indoor_water_use', 'commercial_outdoor_water_use'],
                db_column_lookup=dict(
                    total_water_use='total_water_use',
                    residential_water_use='residential_water_use',
                    commercial_water_use='commercial_water_use',
                    residential_indoor_water_use='residential_indoor_water_use',
                    residential_outdoor_water_use='residential_outdoor_water_use',
                    commercial_indoor_water_use='commercial_indoor_water_use',
                    commercial_outdoor_water_use='commercial_outdoor_water_use'
                ),
                labels=['total_water_use', 'residential_water_use', 'commercial_water_use',
                            'residential_indoor_water_use', 'residential_outdoor_water_use',
                            'commercial_indoor_water_use', 'commercial_outdoor_water_use'],
                stackable=False,
                is_stacked=False,
                create_query=lambda result_config: 'SELECT SUM(total_water_use) as total_water_use__sum, SUM(residential_water_use) as residential_water_use__sum, SUM(commercial_water_use) as commercial_water_use__sum, SUM(residential_indoor_water_use) as residential_indoor_water_use__sum, SUM(residential_outdoor_water_use) as residential_outdoor_water_use__sum, SUM(commercial_indoor_water_use) as commercial_indoor_water_use__sum, SUM(commercial_outdoor_water_use) as commercial_outdoor_water_use__sum FROM %({0})s'.format(DbEntityKey.WATER),
                sort_priority=ResultSort.FUTURE
            )
        ], class_scope=self.config_entity and self.config_entity.__class__)

    def update_or_create_media(self, db_entity_keys=None):
        """
        :return: Creates a Media used by the default results
        """

        # Make sure the styles directory exists so that Result css can be stored there
        # TODO do we need to store styles in the filesystem. Or can they just be in the DB??
        create_media_subdir('styles')

        # Used by any Result that has no explicit Medium
        Medium.objects.update_or_create(
            key=ResultMediumKey.DEFAULT,
            name=ResultMediumKey.DEFAULT,
            defaults={
                'content_type': ContentTypeKey.PYTHON,
                'content': {
                    'colorRange': ['yellow', 'purple']
                },
                'description': 'Default'}
        )

        Medium.objects.update_or_create(
            key=ResultMediumKey.BASE_EMPLOYMENT_BY_TYPE,
            name=ResultMediumKey.BASE_EMPLOYMENT_BY_TYPE,
            defaults={
                'content_type': ContentTypeKey.PYTHON,
                'content': {
                    'colorRange': ['purple', 'pink']
                },
                'description': 'Base: Employment by Type'}
        ),

        Medium.objects.update_or_create(
            key=ResultMediumKey.BASE_DWELLING_UNITS_BY_TYPE,
            name=ResultMediumKey.BASE_DWELLING_UNITS_BY_TYPE,
            defaults={
                'content_type': ContentTypeKey.PYTHON,
                'content': {
                    'colorRange': ['yellow', 'red']
                },
                'description': 'Base: Dwelling Units by Type'}
        ),

        Medium.objects.update_or_create(
            key=ResultMediumKey.INCREMENTS,
            name=ResultMediumKey.INCREMENTS,
            defaults={
                'content_type': ContentTypeKey.PYTHON,
                'content': {
                    'colorRange': ['yellow', 'purple']
                },
                'description': 'Increments'}
        )

        Medium.objects.update_or_create(
            key=ResultMediumKey.INCREMENTS_EMPLOYMENT_BY_TYPE,
            name=ResultMediumKey.INCREMENTS_EMPLOYMENT_BY_TYPE,
            defaults={
                'content_type': ContentTypeKey.PYTHON,
                'content': {
                    'colorRange': ['purple', 'pink']
                },
                'description': 'Increments: Employment by Type'}
        ),

        Medium.objects.update_or_create(
            key=ResultMediumKey.INCREMENTS_DWELLING_UNITS_BY_TYPE,
            name=ResultMediumKey.INCREMENTS_DWELLING_UNITS_BY_TYPE,
            defaults={
                'content_type': ContentTypeKey.PYTHON,
                'content': {
                    'colorRange': ['yellow', 'red']
                },
                'description': 'Increments: Dwelling Units by Type'}
        ),
        
        Medium.objects.update_or_create(
            key=ResultMediumKey.END_STATE,
            name=ResultMediumKey.END_STATE,
            defaults={
                'content_type': ContentTypeKey.PYTHON,
                'content': {
                    'colorRange': ['yellow', 'purple']
                },
                'description': 'End State'}
        ),

        Medium.objects.update_or_create(
            key=ResultMediumKey.END_STATE_EMPLOYMENT_BY_TYPE,
            name=ResultMediumKey.END_STATE_EMPLOYMENT_BY_TYPE,
            defaults={
                'content_type': ContentTypeKey.PYTHON,
                'content': {
                    'colorRange': ['purple', 'pink']
                },
                'description': 'End State: Employment by Type'}
        ),

        Medium.objects.update_or_create(
            key=ResultMediumKey.END_STATE_DWELLING_UNITS_BY_TYPE,
            name=ResultMediumKey.END_STATE_DWELLING_UNITS_BY_TYPE,
            defaults={
                'content_type': ContentTypeKey.PYTHON,
                'content': {
                    'colorRange': ['yellow', 'red']
                },
                'description': 'End State: Dwelling Units by Type'}
        )

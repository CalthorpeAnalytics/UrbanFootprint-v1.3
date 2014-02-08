# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
#
# Copyright (C) 2013 Calthorpe Associates
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com

from footprint.initialization.fixture import ResultConfigurationFixture
from footprint.initialization.fixtures.client.default.default_mixin import DefaultMixin
from footprint.initialization.publishing.result_initialization import ResultConfiguration, ResultLibraryConfiguration, ResultLibraryKey, ResultKey, ResultMediumKey
from footprint.models import Scenario, Medium
from footprint.models.config.scenario import BaseScenario, FutureScenario
from footprint.models.keys.keys import Keys
from footprint.utils.utils import create_media_subdir


class DefaultResultConfigurationFixtures(DefaultMixin, ResultConfigurationFixture):

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
            class_scope=self.config_entity.__class__
        )

    def results(self):
        """
            Used to update or create Results per ConfigEntity instance
            Returns the result library(ies) scoped for the class of self.config_entity.
            The Result will belong to the ResultLibrary specified by result_library_key
        :return:
        """
        return self.matching_scope([
                # Basic Core result query that summarizes increments

                ResultConfiguration(
                    class_scope=BaseScenario,
                    result_type='bar_graph',
                    result_library_key=ResultLibraryKey.DEFAULT,
                    result_db_entity_key=ResultKey.BASE_EMPLOYMENT_BY_TYPE,
                    source_db_entity_key=Keys.DB_ABSTRACT_BASE_FEATURE,

                    name='Base: Employment by Sector',
                    attributes=['retail', 'office', 'industrial', 'public', 'other'],
                    db_column_lookup=dict(
                        retail='emp_ret',
                        office='emp_off',
                        industrial='emp_ind',
                        public='emp_public_admin',
                        other='emp_military',
                    ),
                    labels=['Retail', 'Office', 'Industrial', 'Public', 'Other'],
                    stackable=True,
                    is_stacked=False,
                    create_query=lambda result_config: 'SELECT SUM(emp_ret) as emp_ret__sum, SUM(case when emp_off - emp_public_admin < 0 then 0 else emp_off - emp_public_admin end) as emp_off__sum, SUM(emp_ind + emp_ag) as emp_ind__sum, SUM(emp_public_admin) as emp_public_admin__sum, SUM(emp_military) as emp_military__sum FROM %({0})s'.format(Keys.DB_ABSTRACT_BASE_FEATURE)
                ),

                ResultConfiguration(
                    class_scope=BaseScenario,
                    result_type='bar_graph',
                    result_library_key=ResultLibraryKey.DEFAULT,
                    result_db_entity_key=ResultKey.BASE_DWELLING_UNITS_BY_TYPE,
                    source_db_entity_key=Keys.DB_ABSTRACT_BASE_FEATURE,

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
                    create_query=self.simple_aggregate
                 ),

                ResultConfiguration(
                    class_scope=FutureScenario,
                    result_library_key=ResultLibraryKey.DEFAULT,
                    result_type='bar_graph',
                    result_db_entity_key=ResultKey.INCREMENTS,
                    source_db_entity_key=Keys.DB_ABSTRACT_INCREMENT_FEATURE,

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
                    create_query=self.simple_aggregate
                ),
                ResultConfiguration(
                    class_scope=FutureScenario,
                    result_library_key=ResultLibraryKey.DEFAULT,
                    result_type='bar_graph',
                    result_db_entity_key=ResultKey.END_STATE,
                    source_db_entity_key=Keys.DB_ABSTRACT_END_STATE_FEATURE,

                    name='End State: All Metrics',
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
                    create_query=self.simple_aggregate
                ),

                # DB Entity Core result query that summarizes dwellings by type
                ResultConfiguration(
                    class_scope=FutureScenario,
                    result_library_key=ResultLibraryKey.DEFAULT,
                    result_type='bar_graph',
                    result_db_entity_key=ResultKey.INCREMENTS_DWELLING_UNITS_BY_TYPE,
                    source_db_entity_key=Keys.DB_ABSTRACT_INCREMENT_FEATURE,

                    name='Increments: Dwelling Units by Type',
                    attributes=['single_family_large_lot', 'single_family_small_lot', 'multi_family', 'attached_single_family'],
                    db_column_lookup=dict(
                        single_family_large_lot='du_detsf_ll',
                        single_family_small_lot='du_detsf_sl',
                        multi_family='du_mf',
                        attached_single_family='du_attsf',
                    ),
                    labels=['SF Large Lot', 'SF Small Lot', 'MF', 'Attached SF'],
                    stackable=False,
                    is_stacked=False,
                    create_query=self.simple_aggregate
                ),
                ResultConfiguration(
                    class_scope=FutureScenario,
                    result_library_key=ResultLibraryKey.DEFAULT,
                    result_type='bar_graph',
                    result_db_entity_key=ResultKey.END_STATE_DWELLING_UNITS_BY_TYPE,
                    source_db_entity_key=Keys.DB_ABSTRACT_END_STATE_FEATURE,

                    name='End State: Dwelling Units by Type',
                    attributes=['single_family_large_lot', 'single_family_small_lot', 'multi_family', 'attached_single_family'],
                    db_column_lookup=dict(
                        single_family_large_lot='du_detsf_ll',
                        single_family_small_lot='du_detsf_sl',
                        multi_family='du_mf',
                        attached_single_family='du_attsf',
                    ),
                    labels=['SF Large Lot', 'SF Small Lot', 'MF', 'Attached SF'],
                    stackable=True,
                    is_stacked=True,
                    show_attrs_as_percents=True,
                    create_query=self.simple_aggregate
                ),

                ResultConfiguration(
                    class_scope=FutureScenario,
                    result_library_key=ResultLibraryKey.DEFAULT,
                    result_type='bar_graph',
                    result_db_entity_key=ResultKey.INCREMENTS_EMPLOYMENT_BY_TYPE,
                    source_db_entity_key=Keys.DB_ABSTRACT_INCREMENT_FEATURE,

                    name='Increments: Employment by Sector',
                    attributes=['retail', 'office', 'industrial', 'public', 'other'],
                    db_column_lookup=dict(
                        retail='emp_ret',
                        office='emp_off',
                        industrial='emp_ind',
                        public='emp_public_admin',
                        other='emp_military',
                    ),
                    labels=['Retail', 'Office', 'Industrial', 'Public', 'Other'],
                    stackable=False,
                    is_stacked=False,
                    create_query=lambda result_config: 'SELECT SUM(emp_ret) as emp_ret__sum, SUM(case when emp_off - emp_public_admin < 0 then 0 else emp_off - emp_public_admin end) as emp_off__sum, SUM(emp_ind + emp_ag) as emp_ind__sum, SUM(emp_public_admin) as emp_public_admin__sum, SUM(emp_military) as emp_military__sum FROM %({0})s'.format(Keys.DB_ABSTRACT_INCREMENT_FEATURE)
                ),
                ResultConfiguration(
                    class_scope=FutureScenario,
                    result_library_key=ResultLibraryKey.DEFAULT,
                    result_type='bar_graph',
                    result_db_entity_key=ResultKey.END_STATE_EMPLOYMENT_BY_TYPE,
                    source_db_entity_key=Keys.DB_ABSTRACT_END_STATE_FEATURE,

                    name='End State: Employment by Sector',
                    attributes=['retail', 'office', 'industrial', 'public', 'other'],
                    db_column_lookup=dict(
                        retail='emp_ret',
                        office='emp_off',
                        industrial='emp_ind',
                        public='emp_public_admin',
                        other='emp_military',
                    ),
                    labels=['Retail', 'Office', 'Industrial', 'Public', 'Other'],
                    stackable=True,
                    is_stacked=True,
                    create_query=lambda result_config: 'SELECT SUM(emp_ret) as emp_ret__sum, SUM(case when emp_off - emp_public_admin < 0 then 0 else emp_off - emp_public_admin end) as emp_off__sum, SUM(emp_ind + emp_ag) as emp_ind__sum, SUM(emp_public_admin) as emp_public_admin__sum, SUM(emp_military) as emp_military__sum FROM %({0})s'.format(Keys.DB_ABSTRACT_END_STATE_FEATURE)
                ),

                ResultConfiguration(
                    class_scope=FutureScenario,
                    result_library_key=ResultLibraryKey.DEFAULT,
                    result_type='analytic_bars',
                    result_db_entity_key=ResultKey.INCREMENTS_BARS,
                    source_db_entity_key=Keys.DB_ABSTRACT_END_STATE_FEATURE,

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
                    create_query=self.simple_aggregate
                )
            ], class_scope=self.config_entity.__class__)

    def update_or_create_media(self):
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
                'content_type': Keys.CONTENT_TYPE_PYTHON,
                'content': {
                    'colorRange': ['yellow', 'purple']
                },
                'description': 'Default'}
        )

        Medium.objects.update_or_create(
            key=ResultMediumKey.BASE_EMPLOYMENT_BY_TYPE,
            name=ResultMediumKey.BASE_EMPLOYMENT_BY_TYPE,
            defaults={
                'content_type': Keys.CONTENT_TYPE_PYTHON,
                'content': {
                    'colorRange': ['purple', 'pink']
                },
                'description': 'Base: Employment by Type'}
        ),

        Medium.objects.update_or_create(
            key=ResultMediumKey.BASE_DWELLING_UNITS_BY_TYPE,
            name=ResultMediumKey.BASE_DWELLING_UNITS_BY_TYPE,
            defaults={
                'content_type': Keys.CONTENT_TYPE_PYTHON,
                'content': {
                    'colorRange': ['yellow', 'red']
                },
                'description': 'Base: Dwelling Units by Type'}
        ),

        Medium.objects.update_or_create(
            key=ResultMediumKey.INCREMENTS,
            name=ResultMediumKey.INCREMENTS,
            defaults={
                'content_type': Keys.CONTENT_TYPE_PYTHON,
                'content': {
                    'colorRange': ['yellow', 'purple']
                },
                'description': 'Increments'}
        )

        Medium.objects.update_or_create(
            key=ResultMediumKey.INCREMENTS_EMPLOYMENT_BY_TYPE,
            name=ResultMediumKey.INCREMENTS_EMPLOYMENT_BY_TYPE,
            defaults={
                'content_type': Keys.CONTENT_TYPE_PYTHON,
                'content': {
                    'colorRange': ['purple', 'pink']
                },
                'description': 'Increments: Employment by Type'}
        ),

        Medium.objects.update_or_create(
            key=ResultMediumKey.INCREMENTS_DWELLING_UNITS_BY_TYPE,
            name=ResultMediumKey.INCREMENTS_DWELLING_UNITS_BY_TYPE,
            defaults={
                'content_type': Keys.CONTENT_TYPE_PYTHON,
                'content': {
                    'colorRange': ['yellow', 'red']
                },
                'description': 'Increments: Dwelling Units by Type'}
        ),
        
        Medium.objects.update_or_create(
            key=ResultMediumKey.END_STATE,
            name=ResultMediumKey.END_STATE,
            defaults={
                'content_type': Keys.CONTENT_TYPE_PYTHON,
                'content': {
                    'colorRange': ['yellow', 'purple']
                },
                'description': 'End State'}
        ),

        Medium.objects.update_or_create(
            key=ResultMediumKey.END_STATE_EMPLOYMENT_BY_TYPE,
            name=ResultMediumKey.END_STATE_EMPLOYMENT_BY_TYPE,
            defaults={
                'content_type': Keys.CONTENT_TYPE_PYTHON,
                'content': {
                    'colorRange': ['purple', 'pink']
                },
                'description': 'End State: Employment by Type'}
        ),

        Medium.objects.update_or_create(
            key=ResultMediumKey.END_STATE_DWELLING_UNITS_BY_TYPE,
            name=ResultMediumKey.END_STATE_DWELLING_UNITS_BY_TYPE,
            defaults={
                'content_type': Keys.CONTENT_TYPE_PYTHON,
                'content': {
                    'colorRange': ['yellow', 'red']
                },
                'description': 'End State: Dwelling Units by Type'}
        )

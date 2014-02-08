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
from footprint.client.configuration.fixture import ResultConfigurationFixture
from footprint.main.publishing.result_initialization import ResultConfiguration, ResultLibraryKey, ResultKey, ResultSort
from footprint.main.models.config.scenario import BaseScenario
from footprint.main.models.keys.keys import Keys


class ScagResultConfigurationFixtures(ResultConfigurationFixture):
    def results(self):
        """
            Used to update or create Results per ConfigEntity instance
            Returns the result library(ies) scoped for the class of self.config_entity.
            The Result will belong to the ResultLibrary specified by result_library_key
        :return:
        """
        return self.matching_scope(
            # Basic Core result query that summarizes increments
            self.parent_fixture.results() + [
                # Aggregate result from the Analytic Bars
                ResultConfiguration(
                    class_scope=BaseScenario,
                    result_type='analytic_bars',
                    result_library_key=ResultLibraryKey.DEFAULT,
                    source_db_entity_key=Keys.DB_ABSTRACT_BASE_FEATURE,
                    result_db_entity_key=ResultKey.Fab.ricate('base_bars'),

                    name='Base Results',
                    attributes=['population', 'employment', 'dwelling_units'],
                    db_column_lookup=dict(
                        population='pop',
                        employment='emp',
                        dwelling_units='du',
                    ),
                    extent_lookup=dict(
                        population=dict(min=-25000, max=25000),
                        dwelling_units=dict(min=-2500, max=2500),
                        employment=dict(min=-2500, max=2500),
                    ),
                    labels=['Population', 'Employees', 'Dwelling Units'],
                    stackable=False,
                    create_query=self.simple_aggregate,
                    sort_priority=ResultSort.BASE
                )
            ],
            class_scope=self.config_entity and self.config_entity.__class__)


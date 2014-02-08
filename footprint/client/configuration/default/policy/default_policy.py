# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
#
# Copyright (C) 2012 Calthorpe Associates
#
# This program is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.
#
# Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates.
# Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709.
# Phone: (510) 548-6800. Web: www.calthorpe.com
from footprint.client.configuration.fixture import PolicyConfigurationFixture
from footprint.client.configuration.default.default_mixin import DefaultMixin
__author__ = 'calthorpe_associates'


class DefaultPolicyConfigurationFixture(DefaultMixin, PolicyConfigurationFixture):

    def policy_sets(self):
        return [
            {
                'name': 'Default',
                'key': 'default',
                'description': 'Default policy set',
                'policies': [
                    {
                    'name': 'Fiscal',
                    'key': 'fiscal',
                    'description': 'Fiscal policy assumptions',
                    'policies':
                        [
                            {'key': 'operations_maintenance_costs', 'name':
                                'Annual Fiscal Operations and Maintenance Cost Assumptions', 'policies':
                                [{'key': 'urban', 'name': 'Urban Operations and Maintenance Cost Assumptions',
                                  'values': {'single_family_large_lot': 220, 'single_family_small_lot': 220,
                                             'single_family_attached': 190, 'multifamily': 164}},
                                 {'key': 'compact_refill', 'name': 'Compact Refill Operations and Maintenance Cost Assumptions',
                                  'values': {'single_family_large_lot': 213, 'single_family_small_lot': 213,
                                             'single_family_attached': 187, 'multifamily': 160}},
                                 {'key': 'compact_greenfield', 'name': 'Compact Greenfield Operations and Maintenance Cost Assumptions',
                                  'values': {'single_family_large_lot': 223, 'single_family_small_lot': 223,
                                             'single_family_attached': 196, 'multifamily': 167}},
                                 {'key': 'standard', 'name': 'Standard Operations and Maintenance Cost Assumptions',
                                  'values': {'single_family_large_lot': 249, 'single_family_small_lot': 249,
                                             'single_family_attached': 218, 'multifamily': 186}}]
                            },

                            {'key': 'revenue', 'name':
                                'Revenue Assumptions', 'policies':
                                [{'key': 'urban', 'name': 'Urban Revenue',
                                  'values': {'single_family_large_lot': 7299, 'single_family_small_lot': 5763,
                                             'single_family_attached': 4936, 'multifamily': 3528}},
                                 {'key': 'compact_refill', 'name': 'Compact Refill Revenue Assumptions',
                                  'values': {'single_family_large_lot': 7881, 'single_family_small_lot': 6216,
                                             'single_family_attached': 5319, 'multifamily': 3799}},
                                 {'key': 'compact_greenfield', 'name': 'Compact Greenfield Revenue Assumptions',
                                  'values': {'single_family_large_lot': 6768, 'single_family_small_lot': 5349,
                                             'single_family_attached': 4593, 'multifamily': 3276}},
                                 {'key': 'standard', 'name': 'Standard Revenue Assumptions',
                                  'values': {'single_family_large_lot': 5253, 'single_family_small_lot': 4160,
                                             'single_family_attached': 3575, 'multifamily': 2573}}]
                            },

                            {'key': 'capital_costs', 'name':
                                'Capital Cost Assumptions', 'policies':
                                [{'key': 'urban', 'name': 'Urban Capital Cost Assumptions',
                                  'values': {'single_family_large_lot': 5711, 'single_family_small_lot': 5711,
                                             'single_family_attached': 5711, 'multifamily': 4587}},
                                 {'key': 'compact_refill', 'name': 'Compact Refill Capital Cost Assumptions',
                                  'values': {'single_family_large_lot': 5541, 'single_family_small_lot': 4868,
                                             'single_family_attached': 5016, 'multifamily': 4518}},
                                 {'key': 'compact_greenfield', 'name': 'Compact Greenfield Capital Cost Assumptions',
                                  'values': {'single_family_large_lot': 9600, 'single_family_small_lot': 9244,
                                             'single_family_attached': 9127, 'multifamily': 7379}},
                                 {'key': 'standard', 'name': 'Standard Capital Cost Assumptions',
                                  'values': {'single_family_large_lot': 14102, 'single_family_small_lot': 13356,
                                             'single_family_attached': 12740, 'multifamily': 11044}}]
                            }

                        ]
                    }
                ]
            }
        ]

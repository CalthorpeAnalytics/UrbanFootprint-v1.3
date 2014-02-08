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
from footprint.initialization.fixture import PolicyFixture
from footprint.initialization.fixtures.client.default.default_mixin import DefaultMixin
from footprint.utils.range import Range

__author__ = 'calthorpe'


class DefaultPolicyFixture(DefaultMixin, PolicyFixture):

    def policy_sets(self):
        return [
            {
                'name': 'Trend',
                'key': 'oldstandard',
                'description': 'Automobile oriented development policies',
                'policies':
                    [
                        {'key': 'transit', 'name': 'Transit', 'policies':
                            [{'key': 'transit_speed', 'name': 'Transit Speed',
                              'values': ['fast', 'leisurely', 'sluggish']},
                             {'key': 'transit_dwell', 'name': 'Transit Dwell',
                              'values': ['low', 'moderate', 'forever']},
                             {'key': 'transit_abundance', 'name': 'Transit Abundance',
                              'values': ['high', 'medium', 'dismal']}]
                        },
                        {'key': 'health', 'name': 'Health', 'policies':
                            [{'key': 'diseases', 'name': 'Diseases',
                              'values': ['elephantitus', 'leperacy', 'hotdog finger']},
                             {'key': 'decibels', 'name': 'Decibels', 'values': Range(0, 1000000)}]
                        }
                    ]
            },
            {
                'name': 'Smart Growth',
                'key': 'fastfurious',
                'description': 'Transit focuesd policies in a better than revenue constrained environment',
                'policies':
                    [
                        {'key': 'transit', 'name': 'Transit', 'policies':
                            [{'key': 'transit_speed', 'name': 'Transit Speed',
                              'values': ['fast', 'leisurely', 'sluggish']},
                             {'key': 'transit_dwell', 'name': 'Transit Dwell',
                              'values': ['low', 'moderate', 'forever']},
                             {'key': 'transit_abundance', 'name': 'Transit Abundance',
                              'values': ['high', 'medium', 'dismal']}]
                        },
                        {'key': 'energy', 'name': 'Energy', 'policies':
                            [{'key': 'source', 'name': 'Energy Source', 'values': ['treadmills', 'atomic', 'solar']},
                             {'key': 'potential', 'name': 'Energy Potential', 'values': Range(0, 1)}]
                        }
                    ]
            }
        ]

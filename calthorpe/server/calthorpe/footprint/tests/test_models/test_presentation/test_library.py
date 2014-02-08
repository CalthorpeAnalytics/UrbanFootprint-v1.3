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

from django.utils import unittest
from footprint.tests.data_provider import DataProvider

__author__ = 'calthorpe'

class TestLibrary(unittest.TestCase):
    """
        Test the ability to add, remove and sort items in a Library instance
    """

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_full_library(self):
        """
            Create a library whose config_entity combines sibling Scenarios and all their ancestral media
        :return:
        """
        library = DataProvider().joint_library()
        for attribute, queryset in {
            'presentationmedium_set':library.presentationmedium_set.all(),
            'media':library.media.all(),
            'db_entities':library.db_entities()}.items():
            assert(
                map(lambda instance: instance.pk, library.sorted(queryset, attribute)),
                map(lambda instance: instance.pk, queryset.all())
            )


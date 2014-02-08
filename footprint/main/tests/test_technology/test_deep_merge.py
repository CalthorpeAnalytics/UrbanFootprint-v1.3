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
import unittest
from nose import with_setup
from nose.tools import assert_equal
from footprint.main.lib.functions import deep_merge

__author__ = 'calthorpe_associates'

class TestFunctions(unittest.TestCase):
    def setup(self):
        pass

    def teardown(self):
        pass

    @with_setup(setup, teardown)
    def test(self):
        result = deep_merge({1:{1:1}, 'a':{'b':{'b':'b'}}}, {1:{2:2}, 2:2}, {3:3, 'a':{'b':{'c':'c'}}})
        assert_equal(result, {1:{1:1, 2:2}, 2:2, 3:3, 'a':{'b':{'b':'b', 'c':'c'}}})

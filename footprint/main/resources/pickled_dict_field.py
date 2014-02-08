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
import string
from tastypie.fields import DictField, NOT_PROVIDED, ApiField
from footprint.main.lib.functions import map_dict_to_dict, deep_copy_dict_structure, deep_copy

__author__ = 'calthorpe_associates'

class ObjectField(ApiField):
    """
    Handles any object by turning it into a dict by recursively using each object's __dict__ attribute
    Arrays are left as arrays
    Since class data is removed a reference instance would be needed to rehydrate it
    """
    dehydrated_type = 'dict'
    help_text = "A dictionary of data. Ex: {'price': 26.73, 'name': 'Daniel'}"

    def convert(self, value):
        if value is None:
            return None

        return deep_copy(value, True)

class PickledObjField(ObjectField):
    """
        For read-only configurations, dehydration of arbitrary object graphs. Hydration isn't possible without having a reference instance to know the classes
    """

    def dehydrate(self, bundle):
        """
            Handles the object dehydration
        :param bundle:
        :return:
        """

        # Deep copy the structure to create new dict instance so we don't mutilate the source
        obj = super(PickledObjField, self).dehydrate(bundle)
        return deep_copy(obj, True)


class PickledDictField(ApiField):

    def dehydrate(self, bundle):
        """
        :param bundle:
        :return:
        """

        # Deep copy the structure to create new dict instance so we don't mutilate the source
        try:
            return deep_copy(super(PickledDictField, self).dehydrate(bundle))
        except:
            setattr(bundle.obj, self.attribute, None) # value got deformed--clear it
            return deep_copy(super(PickledDictField, self).dehydrate(bundle))

    def hydrate(self, bundle):
        """
            Hydrates a dict of resource URI to the corresponding instances by resolving the URIs. Like dehydrate_selections, this could be generalized
        :param bundle:
        :return:
        """
        value = super(PickledDictField, self).hydrate(bundle)
        return value


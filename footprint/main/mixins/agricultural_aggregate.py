# This Python file uses the following encoding: utf-8

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
from footprint.main.mixins.built_form_aggregate import BuiltFormAggregate

__author__ = 'calthorpe_associates'

class AgricultureAttributeAggregate(BuiltFormAggregate):
    """
    An abstract class that describes a high-level built form that has a
    :model:`built_forms.building_attribute_set.BuildingAttributeSet`, defines methods to aggregate attributes
    the classes :model:`built_forms.buildingtype.BuildingType` and :model:`built_forms.placetype.Placetype`
    according to the mix of their components.
    """
    class Meta:
        abstract = True
        app_label = 'main'

    def aggregate_agriculture_attribute_set(self):
        """
        Grabs the component buildings of the BuildingAggregate and does a weighted average of their core attributes,
        before passing the building_attribute_set to the calculate_derived_fields() method.
        """

        if not self.agriculture_attribute_set:
            return

        AG_AGGREGATE_FIELDS = [
            'crop_yield', 'unit_price', 'cost', 'water_consumption', 'labor_input', 'truck_trips'
        ]

        for attribute in AG_AGGREGATE_FIELDS:
            value = self.aggregate_attribute('agriculture_attribute_set', attribute)
            setattr(self.agriculture_attribute_set, attribute, value)
        self.agriculture_attribute_set.save()
        self.save()
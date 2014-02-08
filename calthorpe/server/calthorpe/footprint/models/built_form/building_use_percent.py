# coding=utf-8
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
from django.db import models

from footprint.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.mixins.percent import Percent
from footprint.models.constants import Constants
from footprint.models.keys.keys import Keys


__author__ = 'calthorpe'


class BuildingUsePercent(Percent):
    """
    Describes the percent of :model:`footprint.BuildingUseDefinition` present in a particular
    :model:`footprint.BuildingAttributeSet`.
    """
    objects = GeoInheritanceManager()

    building_attributes = models.ForeignKey('BuildingAttributeSet')
    building_use_definition = models.ForeignKey('BuildingUseDefinition')

    vacancy_rate = models.DecimalField(max_digits=4, decimal_places=3, default=Constants.VACANCY_RATE)
    household_size = models.DecimalField(max_digits=5, decimal_places=3, null=True)

    # describes the ratio : use areas / (common areas + use areas)
    efficiency = models.DecimalField(max_digits=6, decimal_places=4, default=.85)

    # describes the number of square feet per unit ( dwelling unit or employee ) of the building
    square_feet_per_unit = models.DecimalField(max_digits=11, decimal_places=3, null=True)

    ## derived attributes
    # area measured in acres
    floor_area_ratio = models.DecimalField(max_digits=12, decimal_places=10, null=True)
    unit_density = models.DecimalField(max_digits=16, decimal_places=10, null=True)

    # area measured in square feet
    gross_built_up_area = models.DecimalField(max_digits=13, decimal_places=3, null=True)
    net_built_up_area = models.DecimalField(max_digits=13, decimal_places=3, null=True)

    class Meta(object):
        app_label = 'footprint'

    def calculate_derived_attributes(self):
        """
        Calculates floor_area_ratio, gross_built_up_area, net_built_up_area, and use_density based on the
        inputs self.built_form.total_far, self.built_form.gross_net_ratio, self.percent, self.efficiency, and
        either self.square_feet_per_unit or self.built_form.residential_average_lot_size (the latter for detached
        residential building_use_definitions).
        """

        if not self.floor_area_ratio:
            parcel_far = self.building_attributes.total_far  # / self.building_attributes.gross_net_ratio
            self.floor_area_ratio = self.percent * parcel_far
        self.gross_built_up_area = self.floor_area_ratio * Constants.SQUARE_FEET_PER_ACRE
        self.net_built_up_area = self.gross_built_up_area * self.efficiency
        percent_of_parcel_acres = self.percent  # / self.building_attributes.gross_net_ratio

        if self.building_use_definition.name in Keys.DETACHED_RESIDENTIAL and self.building_attributes.residential_average_lot_size:
            residential_lots_per_acre = Constants.SQUARE_FEET_PER_ACRE / self.building_attributes.residential_average_lot_size
            self.unit_density = percent_of_parcel_acres * residential_lots_per_acre
        else:
            self.unit_density = self.net_built_up_area / self.square_feet_per_unit

        self.save()
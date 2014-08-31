__author__ = 'calthorpe_associates'


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

from footprint.main.managers.geo_inheritance_manager import GeoInheritanceManager
from django.contrib.gis.db import models


class StreetAttributeSet(models.Model):
    """
    Attributes of a :models:`main.Building`, :models:`main.BuildingType`, or :models:`main.Placetype`,
    including a reference to its uses through :model:`built_form.building_use_percent.BuildingUsePercent`.
    """
    objects = GeoInheritanceManager()

    class Meta(object):
        abstract = False
        app_label = 'main'

    def attributes(self):
        return "building"

    lane_width = models.DecimalField(max_digits=8, decimal_places=4, default=0)
    number_of_lanes = models.DecimalField(max_digits=8, decimal_places=4, default=0)
    block_size = models.DecimalField(max_digits=8, decimal_places=4, default=0)




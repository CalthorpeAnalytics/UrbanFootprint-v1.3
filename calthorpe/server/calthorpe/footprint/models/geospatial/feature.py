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
from django.contrib.gis.db.models import GeoManager
from footprint.mixins.geographic import Geographic
from footprint.mixins.timestamps import Timestamps

__author__ = 'calthorpe'

class Feature(Timestamps, Geographic):
    """
        A mixin model class that references a Geography instance. The abstract Geography class and its subclasses
        represent geography authorities, so that any shared geographies like regional parcels have one authoritive
        locations. Derived classes and their instances, such as the ConfigEntityGeography derivative classes use the
        Geographic mixin to reference the authoritative geographies of the Geography class hierarchy
    """

    # Base manager inherited by subclasses
    objects = GeoManager()

    class Meta(object):
        abstract = True
        app_label='footprint'
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
from picklefield import PickledObjectField
from django.contrib.gis.db import models
from footprint.mixins.geographic import Geographic


__author__ = 'calthorpe'

class GeoJsonFeature(Geographic):
    """
        Represents a geojson feature, including a geometry and properties that are stored in a dictionary. This class is dynamically subclassed so that there is one subclass per geometry table in the database. In other words, when geojson is imported a subclass is created that is in turn used to create a new table
    """
    objects = models.GeoManager()

    geometry = models.GeometryField()
    # GeoJson Features may optionally associate with an official Geography, such as a parcel
    properties = PickledObjectField()

    class Meta(object):
        abstract = True


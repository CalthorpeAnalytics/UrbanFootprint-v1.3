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
from django.contrib.gis.db import models

__author__ = 'calthorpe_associates'


class Geography(models.Model):
    """
        Represents a geographic shape such as a parcel, grid cell, line, etc. Other classes having features should
        associate to subclasses of this subclass it.
    """
    objects = models.GeoManager()
    geometry = models.GeometryField()
    # An identifier that uniquely identifies the source table that provided these geographies.
    source_table_id = models.IntegerField(null=False, db_index=True)
    # An identifier that uniquely a row from the source table, usually its id
    source_id = models.IntegerField(null=False, db_index=True, max_length=200)

    class Meta(object):
        abstract = True,
        app_label = 'main'


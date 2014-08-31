from footprint.main.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.main.models.geospatial.feature import Feature

__author__ = 'calthorpe_associates'
# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
#
# Copyright (C) 2014 Calthorpe Associates
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
from django.db import models

class CensusBlockgroup(Feature):
    objects = GeoInheritanceManager()
    blockgroup = models.CharField(max_length=20)

    # Used to create census_track ForeignKey
    tract = models.CharField(max_length=20)

    @classmethod
    def related_fields(cls):
        return dict(built_forms=dict(
            single=True,
            related_class_name='footprint.main.models.built_form',
            source_field='key',
            source_class_join_field_name='built_form'))

    class Meta:
        abstract = True
        app_label = 'main'

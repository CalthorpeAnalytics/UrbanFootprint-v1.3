# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
#
# Copyright (C) 2013 Calthorpe Associates
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com

from django.db import models
from footprint.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.mixins.geographic import Geographic

class CensusBlock(Geographic):

    objects = GeoInheritanceManager()
    block = models.CharField(max_length=20)

    @classmethod
    def dynamic_fields(cls, **db_entity_setups):
        return dict(census_blockgroup=models.ForeignKey(db_entity_setups['census_blockgroup']['feature_class'])
    )

    class Meta:
        abstract = True
        app_label = 'footprint'

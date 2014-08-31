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


from model_utils.managers import InheritanceManager
from footprint.main.models.geospatial.db_entity import DbEntity
from django.contrib.gis.db import models

__author__ = 'calthorpe'


class EnvironmentalConstraintPercent(models.Model):

    db_entity = models.ForeignKey(DbEntity)
    analysis_tool = models.ForeignKey('EnvironmentalConstraintUpdaterTool', null=False)
    percent = models.DecimalField(max_digits=14, decimal_places=8, default=1, null=True)
    priority = models.IntegerField(default=1, null=True)

    objects = InheritanceManager()

    class Meta(object):
        app_label = 'main'
        abstract = False


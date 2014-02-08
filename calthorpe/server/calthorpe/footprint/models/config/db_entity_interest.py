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
from picklefield import PickledObjectField
import sys
from footprint.lib.functions import map_dict, map_item_or_items_or_dict_values
from footprint.managers.config.db_entity_interest_manager import DbEntityInterestManager
from footprint.models.geospatial.db_entity import DbEntity
from footprint.models.config.interest import Interest

__author__ = 'calthorpe'

class DbEntityInterest(models.Model):
    objects = DbEntityInterestManager()

    # A class name is used to avoid circular dependency
    config_entity = models.ForeignKey('ConfigEntity', null=False)
    db_entity = models.ForeignKey(DbEntity, null=False)
    interest = models.ForeignKey(Interest, null=False)

    def __unicode__(self):
        return "ConfigEntity:{0}, DbEntity:{1}, Interest:{2}".format(self.config_entity, self.db_entity, self.interest)
    class Meta(object):
        app_label = 'footprint'



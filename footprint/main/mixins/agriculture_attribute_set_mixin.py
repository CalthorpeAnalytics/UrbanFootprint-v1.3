#coding=utf-8
__author__ = 'calthorpe_associates'

# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
#
# Copyright (C) 2012 Calthorpe Associates
#
# This program is free software: you can redistribute it and/or modify it under the terms of the
 # GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.


from django.contrib.gis.db import models

from footprint.main.models.built_form.agriculture.agriculture_attribute_set import AgricultureAttributeSet


class AgricultureAttributeSetMixin(models.Model):
    class Meta:
        abstract = True
        app_label = 'main'

    agriculture_attribute_set = models.ForeignKey(AgricultureAttributeSet, null=True)



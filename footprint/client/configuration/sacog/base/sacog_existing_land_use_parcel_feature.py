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
from footprint.main.models.base.primary_parcel_feature import PrimaryParcelFeature

__author__ = 'calthorpe_associates'


class SacogExistingLandUseParcelFeature(PrimaryParcelFeature):

    census_blockgroup = models.CharField(max_length=100, null=True, blank=True)
    census_block= models.CharField(max_length=100, null=True, blank=True)
    land_use = models.CharField(max_length=100, null=True, blank=True)
    acres = models.DecimalField(max_digits=14, decimal_places=4)
    du = models.DecimalField(max_digits=14, decimal_places=4)
    jurisdiction= models.CharField(max_length=100, null=True, blank=True)
    notes = models.CharField(max_length=100, null=True, blank=True)
    emp = models.DecimalField(max_digits=14, decimal_places=4)
    ret = models.DecimalField(max_digits=14, decimal_places=4)
    off = models.DecimalField(max_digits=14, decimal_places=4)
    pub = models.DecimalField(max_digits=14, decimal_places=4)
    ind = models.DecimalField(max_digits=14, decimal_places=4)
    other = models.DecimalField(max_digits=14, decimal_places=4)
    assessor= models.CharField(max_length=100, null=True, blank=True)
    gp = models.CharField(max_length=100, null=True, blank=True)
    gluc = models.CharField(max_length=100, null=True, blank=True)


    class Meta(object):
        abstract = True
        app_label = 'main'

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
from footprint.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.models.built_form.client_land_use_definition import ClientLandUseDefinition

__author__ = 'calthorpe'

from django.db import models

class SacogLandUseDefinition(ClientLandUseDefinition):
    objects = GeoInheritanceManager()

    land_use = models.CharField(max_length=100, null=True, blank=True)
    min_du_ac = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    max_du_ac = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    max_emp_ac = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    rural_flag = models.BooleanField(default=False)
    detached_flag = models.BooleanField(default=False)
    attached_flag = models.BooleanField(default=False)

    pct_ret_rest = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    pct_ret_ret = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    pct_ret_svc = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    pct_off_gov = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    pct_off_off = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    pct_off_svc = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    pct_off_med = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    pct_ind = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    pct_pub_edu = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    pct_pub_med = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    pct_pub_gov = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    pct_other = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    class Meta(object):
        abstract = False
        app_label = 'footprint'

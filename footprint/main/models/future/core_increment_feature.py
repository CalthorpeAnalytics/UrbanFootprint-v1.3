# coding=utf-8
# UrbanFootprint-California (v1.0) Land Use Scenario Development and Modeling System.
#
# Copyright (C) 2012 Calthorpe Associates
#
# This program is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation version 3 of the License.
#
# This program is distributed in the hope that it will be useful but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not see <http://www.gnu.org/licenses/>.
#
# Contact: Joe DiStefano (joed@calthorpe.com) Calthorpe Associates.
# Firm contact: 2095 Rose Street Suite 201 Berkeley CA 94709.
# Phone: (510) 548-6800. Web: www.calthorpe.com
from django.db import models
from footprint.main.models.geospatial.feature import Feature, UpdatingFeature

__author__ = 'calthorpe_associates'


class CoreIncrementFeature(UpdatingFeature):
    api_include = ['built_form_key', 'land_development_category', 'refill_flag', 'pop', 'hh', 'du', 'du_detsf', 'du_attsf', 'du_mf', 'emp', 'emp_ret', 'emp_off', 'emp_pub', 'emp_ind', 'emp_ag', 'emp_military']
    built_form_key = models.CharField(max_length=100, default=None, null=True)
    land_development_category = models.CharField(max_length=20, default=None, null=True)
    refill_flag = models.IntegerField(null=True)

    pop = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    hh = models.DecimalField(max_digits=14, decimal_places=4, default=0)

    du = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    du_detsf = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    du_detsf_ll = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    du_detsf_sl = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    du_attsf = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    du_mf = models.DecimalField(max_digits=14, decimal_places=4, default=0)

    emp = models.DecimalField(max_digits=14, decimal_places=4, default=0)

    emp_ret = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    emp_off = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    emp_pub = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    emp_ind = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    emp_ag = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    emp_military = models.DecimalField(max_digits=14, decimal_places=4, default=0)

    emp_retail_services = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    emp_restaurant = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    emp_accommodation = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    emp_arts_entertainment = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    emp_other_services = models.DecimalField(max_digits=14, decimal_places=4, default=0)

    emp_office_services = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    emp_education = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    emp_public_admin = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    emp_medical_services = models.DecimalField(max_digits=14, decimal_places=4, default=0)

    emp_wholesale = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    emp_transport_warehousing = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    emp_manufacturing = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    emp_utilities = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    emp_construction = models.DecimalField(max_digits=14, decimal_places=4, default=0)

    emp_agriculture = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    emp_extraction = models.DecimalField(max_digits=14, decimal_places=4, default=0)

    class Meta(object):
        abstract = True
        app_label = 'main'

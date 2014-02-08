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
from footprint.models.geospatial.feature import Feature

__author__ = 'calthorpe'


class CoreIncrementFeature(Feature):
    pop = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    hh = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    du = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    emp = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    du_detsf = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    du_detsf_ll = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    du_detsf_sl = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    du_attsf = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    du_mf = models.DecimalField(max_digits=14, decimal_places=4, default=0)

    emp = models.DecimalField(max_digits=14, decimal_places=4, default=0)

    emp_ret = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    emp_retail_services = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    emp_restaurant = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    emp_accommodation = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    emp_arts_entertainment = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    emp_other_services = models.DecimalField(max_digits=14, decimal_places=4, default=0)

    emp_off = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    emp_office_services = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    emp_education = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    emp_public_admin = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    emp_medical_services = models.DecimalField(max_digits=14, decimal_places=4, default=0)

    emp_ind = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    emp_wholesale = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    emp_transport_warehousing = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    emp_manufacturing = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    emp_utilities = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    emp_construction = models.DecimalField(max_digits=14, decimal_places=4, default=0)

    emp_ag = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    emp_agriculture = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    emp_extraction = models.DecimalField(max_digits=14, decimal_places=4, default=0)

    emp_military = models.DecimalField(max_digits=14, decimal_places=4, default=0)

    #    urban_ldc = models.IntegerField()      These are not currently in the flat built form table...need to add them either this release or soon after
    #    compact_ldc = models.IntegerField()
    #    standard_ldc = models.IntegerField()
    refill = models.IntegerField(null=True)

    class Meta(object):
        abstract = True
        app_label = 'footprint'


class TemplateCoreIncrementFeature(CoreIncrementFeature):
    """
        Template subclass so that south generates migrations that we can apply to the dynamically generated subclasses
    """

    class Meta(object):
        app_label = 'footprint'
        abstract = False

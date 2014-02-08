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
from footprint.initialization.fixtures.client.sacog.built_form.sacog_land_use_definition import SacogLandUseDefinition
from footprint.models import Parcel
from footprint.models.base.primary_parcel_feature import PrimaryParcelFeature

__author__ = 'calthorpe'


class SacogExistingLandUseParcelFeature(PrimaryParcelFeature):
    @classmethod
    def geography_type(cls):
        return Parcel

    # these are fields used for the base updating, and are edited directly by the user
    dev_pct = models.DecimalField(max_digits=6, decimal_places=5, default=1)
    density_pct = models.DecimalField(max_digits=6, decimal_places=5, default=1)

    land_use_definition = models.ForeignKey(SacogLandUseDefinition, null=True)

    landuse12 = models.CharField(max_length=100, null=True, blank=True)
    # geom_id = models.IntegerField(null=True)
    plcshpid = models.IntegerField(null=False)
    # wkb_geometry geometry,

    # Add These for viewing
    #geography.source_id
    jurisdiction = models.CharField(max_length=100, null=True, blank=True)

    # View
    acres = models.DecimalField(max_digits=10, decimal_places=4)

    # Calculated but overridable
    max_du_ac = models.DecimalField(max_digits=10, decimal_places=3)
    # Calculated but overridable
    max_emp_ac = models.DecimalField(max_digits=10, decimal_places=3)
    # View
    du12 = models.DecimalField(max_digits=10, decimal_places=3) #
    # View
    emp12 = models.DecimalField(max_digits=10, decimal_places=3) #

    ret_rest = models.DecimalField(max_digits=10, decimal_places=3)
    ret_ret = models.DecimalField(max_digits=10, decimal_places=3)
    ret_svc = models.DecimalField(max_digits=10, decimal_places=3)
    off_off = models.DecimalField(max_digits=10, decimal_places=3)
    off_gov = models.DecimalField(max_digits=10, decimal_places=3)
    off_svc = models.DecimalField(max_digits=10, decimal_places=3)
    pub_gov = models.DecimalField(max_digits=10, decimal_places=3)
    pub_edu = models.DecimalField(max_digits=10, decimal_places=3)
    off_med = models.DecimalField(max_digits=10, decimal_places=3)
    pub_med = models.DecimalField(max_digits=10, decimal_places=3)
    ind = models.DecimalField(max_digits=10, decimal_places=3)
    other = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    #
    # sf_flag = models.CharField(max_length=100, null=True, blank=True)
    # mf_flag = models.CharField(max_length=100, null=True, blank=True)
    # block_positive_du_flag = models.CharField(max_length=100, null=True, blank=True)
    # block_negative_du_flag = models.CharField(max_length=100, null=True, blank=True)
    # ret_flag = models.CharField(max_length=100, null=True, blank=True)
    # off_flag = models.CharField(max_length=100, null=True, blank=True)
    # pub_flag = models.CharField(max_length=100, null=True, blank=True)
    # med_flag = models.CharField(max_length=100, null=True, blank=True)
    # ind_flag = models.CharField(max_length=100, null=True, blank=True)

    class Meta(object):
        abstract = True
        app_label = 'footprint'


class TemplateSacogExistingLandUseParcelFeature(SacogExistingLandUseParcelFeature):
    """
        Template subclass so that south generates migrations that we can apply to the dynamically generated subclasses
    """

    class Meta(object):
        app_label = 'footprint'
        abstract = False

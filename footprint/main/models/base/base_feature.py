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

from footprint.main.models.geospatial.feature import PaintingFeature
from footprint.main.models.keys.keys import Keys


__author__ = 'calthorpe_associates'


class BaseFeature(PaintingFeature):

    built_form_key = models.CharField(max_length=250, null=True, blank=True, default=None, db_column='built_form')
    region_lu_code = models.CharField(max_length=250, null=True, blank=True, default=None)
    intersection_density_sqmi = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    intersection_count = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    acres_gross = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    sqft_parcel = models.DecimalField(max_digits=14, decimal_places=4)
    acres_parcel = models.DecimalField(max_digits=14, decimal_places=4)
    acres_parcel_res = models.DecimalField(max_digits=14, decimal_places=4)
    acres_parcel_res_detsf = models.DecimalField(max_digits=14, decimal_places=4)
    acres_parcel_res_detsf_sl = models.DecimalField(max_digits=14, decimal_places=4)
    acres_parcel_res_detsf_ll = models.DecimalField(max_digits=14, decimal_places=4)
    acres_parcel_res_attsf = models.DecimalField(max_digits=14, decimal_places=4)
    acres_parcel_res_mf = models.DecimalField(max_digits=14, decimal_places=4)
    acres_parcel_emp = models.DecimalField(max_digits=14, decimal_places=4)
    acres_parcel_emp_off = models.DecimalField(max_digits=14, decimal_places=4)
    acres_parcel_emp_ret = models.DecimalField(max_digits=14, decimal_places=4)
    acres_parcel_emp_ind = models.DecimalField(max_digits=14, decimal_places=4)
    acres_parcel_emp_ag = models.DecimalField(max_digits=14, decimal_places=4)
    acres_parcel_emp_mixed = models.DecimalField(max_digits=14, decimal_places=4)
    acres_parcel_emp_military = models.DecimalField(max_digits=14, decimal_places=4)
    acres_parcel_mixed = models.DecimalField(max_digits=14, decimal_places=4)
    acres_parcel_mixed_w_off = models.DecimalField(max_digits=14, decimal_places=4)
    acres_parcel_mixed_no_off = models.DecimalField(max_digits=14, decimal_places=4)
    acres_parcel_no_use = models.DecimalField(max_digits=14, decimal_places=4)

    pop = models.DecimalField(max_digits=14, decimal_places=4)
    hh = models.DecimalField(max_digits=14, decimal_places=4)

    du = models.DecimalField(max_digits=14, decimal_places=4)
    du_detsf = models.DecimalField(max_digits=14, decimal_places=4)
    du_detsf_sl = models.DecimalField(max_digits=14, decimal_places=4)
    du_detsf_ll = models.DecimalField(max_digits=14, decimal_places=4)
    du_attsf = models.DecimalField(max_digits=14, decimal_places=4)
    du_mf = models.DecimalField(max_digits=14, decimal_places=4)
    du_mf2to4 = models.DecimalField(max_digits=14, decimal_places=4)
    du_mf5p = models.DecimalField(max_digits=14, decimal_places=4)

    emp = models.DecimalField(max_digits=14, decimal_places=4)

    emp_ret = models.DecimalField(max_digits=14, decimal_places=4)

    emp_retail_services = models.DecimalField(max_digits=14, decimal_places=4)
    emp_restaurant = models.DecimalField(max_digits=14, decimal_places=4)
    emp_accommodation = models.DecimalField(max_digits=14, decimal_places=4)
    emp_arts_entertainment = models.DecimalField(max_digits=14, decimal_places=4)
    emp_other_services = models.DecimalField(max_digits=14, decimal_places=4)

    emp_off = models.DecimalField(max_digits=14, decimal_places=4)

    emp_office_services = models.DecimalField(max_digits=14, decimal_places=4)
    emp_public_admin = models.DecimalField(max_digits=14, decimal_places=4)
    emp_education = models.DecimalField(max_digits=14, decimal_places=4)
    emp_medical_services = models.DecimalField(max_digits=14, decimal_places=4)

    emp_ind = models.DecimalField(max_digits=14, decimal_places=4)

    emp_manufacturing = models.DecimalField(max_digits=14, decimal_places=4)
    emp_wholesale = models.DecimalField(max_digits=14, decimal_places=4)
    emp_transport_warehousing = models.DecimalField(max_digits=14, decimal_places=4)
    emp_utilities = models.DecimalField(max_digits=14, decimal_places=4)
    emp_construction = models.DecimalField(max_digits=14, decimal_places=4)

    emp_ag = models.DecimalField(max_digits=14, decimal_places=4)
    emp_agriculture = models.DecimalField(max_digits=14, decimal_places=4)
    emp_extraction = models.DecimalField(max_digits=14, decimal_places=4)

    emp_military = models.DecimalField(max_digits=14, decimal_places=4)

    bldg_sqft_detsf_sl = models.DecimalField(max_digits=14, decimal_places=4)
    bldg_sqft_detsf_ll = models.DecimalField(max_digits=14, decimal_places=4)
    bldg_sqft_attsf = models.DecimalField(max_digits=14, decimal_places=4)
    bldg_sqft_mf = models.DecimalField(max_digits=14, decimal_places=4)

    bldg_sqft_retail_services = models.DecimalField(max_digits=14, decimal_places=4)
    bldg_sqft_restaurant = models.DecimalField(max_digits=14, decimal_places=4)
    bldg_sqft_accommodation = models.DecimalField(max_digits=14, decimal_places=4)
    bldg_sqft_arts_entertainment = models.DecimalField(max_digits=14, decimal_places=4)
    bldg_sqft_other_services = models.DecimalField(max_digits=14, decimal_places=4)
    bldg_sqft_office_services = models.DecimalField(max_digits=14, decimal_places=4)
    bldg_sqft_public_admin = models.DecimalField(max_digits=14, decimal_places=4)
    bldg_sqft_education = models.DecimalField(max_digits=14, decimal_places=4)
    bldg_sqft_medical_services = models.DecimalField(max_digits=14, decimal_places=4)
    bldg_sqft_wholesale = models.DecimalField(max_digits=14, decimal_places=4)
    bldg_sqft_transport_warehousing = models.DecimalField(max_digits=14, decimal_places=4)

    residential_irrigated_sqft = models.DecimalField(max_digits=14, decimal_places=4)
    commercial_irrigated_sqft = models.DecimalField(max_digits=14, decimal_places=4)

    class Meta(object):
        abstract = True
        app_label = 'main'

    def update_built_form_id(self):
        old_id = self.built_form_id

        buildingtype = Keys.BUILDINGTYPE_SOURCE_ID_LOOKUP['by_source_id'].get(
            self.built_form_id or None)
        id = Keys.BUILDINGTYPE_SOURCE_ID_LOOKUP['by_name'].get(buildingtype or None)

        if id:
            self.built_form_id = id['fp_id']
            self.save()
        else:
            warning = "translation-only type : built_form_id {id}".format(id=old_id)
            print warning


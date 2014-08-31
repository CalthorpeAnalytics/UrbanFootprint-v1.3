# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
#
# Copyright (C) 2014 Calthorpe Associates
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com

from django.db import models
from footprint.main.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.main.models.geospatial.feature import Feature


class CensusBlock(Feature):

    objects = GeoInheritanceManager()
    block = models.CharField(max_length=20)
    blockgroup = models.CharField(max_length=20)
    tract = models.CharField(max_length=20)
    du_attsf_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    du_mf2to4_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    du_mf5p_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    hh_own_occ_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    hh_rent_occ_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    hh_inc_00_10_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    hh_inc_10_20_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    hh_inc_20_30_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    hh_inc_30_40_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    hh_inc_40_50_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    hh_inc_50_60_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    hh_inc_60_75_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    hh_inc_75_100_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    hh_inc_100_125_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    hh_inc_125_150_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    hh_inc_150_200_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    hh_inc_200p_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    hh_agg_inc_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    hh_agg_veh_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    pop_female_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    pop_male_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    pop_age0_4_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    pop_age5_9_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    pop_age10_14_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    pop_age15_17_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    pop_age18_19_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    pop_age20_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    pop_age21_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    pop_age22_24_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    pop_age25_29_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    pop_age30_39_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    pop_age40_49_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    pop_age50_64_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    pop_age65_up_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    pop_age16_up_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    pop_age25_up_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    pop_female_age20_64_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    pop_male_age20_64_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    pop_hs_not_comp_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    pop_hs_diploma_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    pop_assoc_some_coll_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    pop_coll_degree_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    pop_grad_degree_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    pop_employed_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    pop_unemployed_rate = models.DecimalField(max_digits=14, decimal_places=6, default=0)

    class Meta:
        abstract = True
        app_label = 'main'

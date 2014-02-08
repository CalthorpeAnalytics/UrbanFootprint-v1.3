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
import psycopg2

from footprint.main.lib.functions import map_to_2d_dict, first
from uf_tools import executeSQL_now

__author__ = 'calthorpe_associates'

# Table-level calls for the model classes
from django.db.models.aggregates import Sum, Avg
from django.db import models


# class CoreGridManager(models.Manager):
#
#     def placetype_notnull(self):
#         return self.filter(placetype_id__isnull=False)
#
#     def sum_dwelling_units_and_employment(self):
#         result = self.aggregate(Sum('pop'), Sum('du'), Sum('emp'))
#         return map(lambda key: result[key], ['pop__sum', 'du__sum', 'emp__sum'])
#
#     def sum_population(self):
#         return self.placetype_notnull().aggregate(Sum('pop')).values
#
#     def sum_acres_parcel(self):
#         return self.placetype_notnull().aggregate(Sum('acres_parcel')).values
#
#     def avg_gross_residential_density(self):
#         return self.placetype_notnull().filter(gross_res_dens__gt=0).aggregate(Avg('gross_res_dens')).values
#
#     def avg_gross_employment_density(self):
#         return self.placetype_notnull().filter(gross_emp_dens__gt=0).aggregate(Avg('gross_emp_dens')).values
#
#     def avg_net_residential_density(self):
#         return self.placetype_notnull().filter(net_res_dens__gt=0).aggregate(Avg('net_res_dens')).values
#
#     def avg_net_employment_density(self):
#         return self.placetype_notnull().filter(net_emp_dens__gt=0).aggregate(Avg('net_emp_dens')).values
#
# class HorizDevelopableManager(models.Manager):
#
#     def placetype_notnull(self):
#         return self.filter(placetype_id__isnull=False)
#
#     def sum_dwelling_units_and_employment(self):
#         result = self.placetype_notnull().aggregate(Sum('pop_res_hz'), Sum('du_hz'), Sum('emp_hz'))
#         return map(lambda key: result[key], ['pop_res_hz__sum', 'du_hz__sum', 'emp_hz__sum'])
#
#     def sum_new_units(self):
#         result =  self.placetype_notnull().aggregate(Sum('du_detsf_ll_hz'), Sum('du_detsf_sl_hz'), Sum('du_attsf_hz'), Sum('du_mf_hz'))
#         return map(lambda key: result[key], ['du_detsf_ll_hz__sum', 'du_detsf_sl_hz__sum', 'du_attsf_hz__sum', 'du_mf_hz__sum'])
#
#     def sum_new_jobs(self):
#         result = self.placetype_notnull().aggregate(Sum('emp_ret_hz'), Sum('emp_off_hz'), Sum('emp_educ_hz'), Sum('emp_ind_hz'), Sum('emp_manuf_hz'))
#         return [result['emp_ret_hz__sum'], result['emp_off_hz__sum']+result['emp_educ_hz__sum'], result['emp_ind_hz__sum']+result['emp_manuf_hz__sum']]
#
#
# class IncrementManager(models.Manager):
#
#     def init(self, scenario):
#         self.scenario = scenario
#
#     def sum_dwelling_units_and_employment(self):
#         result = self.aggregate(Sum('pop_inc'), Sum('du_inc'), Sum('emp_inc'))
#         return map(lambda key: result[key], ['pop_inc__sum', 'du_inc__sum', 'emp_inc__sum'])
#
#     def placetype_notnull(self):
#         return self.filter(placetype_id__isnull=False)
#
#     def sum_new_units(self):
#         result =  self.aggregate(Sum('du_detsf_ll_inc'), Sum('du_detsf_sl_inc'), Sum('du_attsf_inc'), Sum('du_mf_inc'))
#         return map(lambda key: result[key], ['du_detsf_ll_inc__sum', 'du_detsf_sl_inc__sum', 'du_attsf_inc__sum', 'du_mf_inc__sum'])
#
#     def sum_new_jobs(self):
#         result = self.aggregate(Sum('emp_ret_inc'), Sum('emp_off_inc'), Sum('emp_ind_inc'))
#         return [result['emp_ret_inc__sum'], result['emp_off_inc__sum'], result['emp_ind_inc__sum']]
#
#     def sum_new_residential_by_ldc(self):
#         return self.sum_new_by_ldc('du_inc')
#
#     def sum_new_employment_by_ldc(self):
#         return self.sum_new_by_ldc('emp_inc')
#
#     def sum_new_units_join_base(self, where):
#         result = self.aggregate(Sum('du_inc'))
#         return [result['du_inc__sum']]
#
#     def sum_transit_corridor_du_increment(self):
#         return self.query_increment("du", 'transit_corridor')
#
#     def sum_transit_corridor_emp_increment(self):
#         return self.query_increment("emp", 'transit_corridor')
#
#     def sum_hsr_station_du_increment(self):
#         return self.query_increment("du", 'hsr_station')
#
#     def sum_hsr_station_emp_increment(self):
#         return self.query_increment("emp", 'hsr_station')
#
#     def sum_new_by_ldc(self, sum_column):
#         densities = ['urban_ldc', 'compact_ldc', 'standard_ldc']
#         results = filter(
#             # Get all results with one of the densities true
#             lambda result: first(lambda density: result.get(density, None), densities) and result['refill'] in [0, 1],
#             self.values(*(densities + ['refill'])).annotate(Sum(sum_column)))
#         # Map the results by density and then refill
#         dictionary = map_to_2d_dict(
#             lambda result: 'refill' if result['refill'] == 1 else 'greenfield',
#             lambda result: [first(lambda key: result.get(key, None), densities), result["{0}__sum".format(sum_column)]],
#             results
#         )
#         # Fill missing values
#         for type in ['refill', 'greenfield']:
#             if not dictionary.get(type, None):
#                 dictionary[type] = {}
#             for density in densities:
#                 if not dictionary[type].get(density, None):
#                     dictionary[type][density] = 0
#         return dictionary
#
#     def query_increment(self, column_prefix, transit_column):
#         formatted_transit_column = 'base_grid__{0}'.format(transit_column)
#         formatted_sum_column = '{0}_inc'.format(column_prefix)
#         results = self.values(formatted_transit_column).order_by(formatted_transit_column).annotate(Sum(formatted_sum_column))
#
#         # The first row is the non-null result, the second is the null result
#         return map(lambda result: result["{0}__sum".format(formatted_sum_column)], results)
#
# class BaseYearGridManager(models.Manager):
#     pass
#
# class DevelopableAcresManager(models.Manager):
#     pass

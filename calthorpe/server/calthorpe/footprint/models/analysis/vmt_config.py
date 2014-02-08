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
__author__ = 'calthorpe'

class VMTConfig(models.Model):

    class Meta(object):
        app_label = 'footprint'

    output_table = models.CharField(max_length = 100) #Sacog_vmt_output_oct25
    #input_reference_grid = models.CharField(max_length = 100)# grid150m_sacog_loaded_adjmts
    taz_grid = models.CharField(max_length = 100) #sacog_taz_grid150m_0911
    taz_trip_lengths = models.CharField(max_length = 100) #sacmet_base
    districts_trip_lengths = models.CharField(max_length = 100) #sacmet_districts
    intersection_count_grid = models.CharField(max_length = 100) #sacog_intersection_count_grid150m_0911
    emp_1mile_buffer_grid = models.CharField(max_length = 100) # sacog_emp_precalc_0911
    transit_distances_grid = models.CharField(max_length = 100) #sacog_transit_2005_distances_0911
    variable_buffers_grid = models.CharField(max_length = 100) #sacog_buffers_variable_0911
    quarter_mile_buffer_grid = models.CharField(max_length = 100) # sacog_quarter_mile_buffer_0911

    def __unicode__(self):
        return unicode("VMT config for %s" % self.scenario)

    class Meta(object):
        verbose_name = "VMT Configuration"
        verbose_name_plural = "VMT Configurations"


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
from footprint.models.geospatial.feature import Feature

__author__ = 'calthorpe'
from django.db import models

class EnergyWaterFeature(Feature):

    #    # These values are interpreted as percents: 30 => 30%
    ResEnrgyNewConst = models.DecimalField("New construction - Percentage reduction from baseline rates by a horizon year", max_digits=5, decimal_places=2, default=30)
    ResEnrgyRetro    = models.DecimalField("Retrofits - Year-upon-year percentage reduction.", max_digits=3, decimal_places=2, default=0.5)    #Retrofits - Year-upon-year percentage reduction.
    ResEnrgyReplcmt  = models.DecimalField("Replacement - Reset of some percentage of existing units to new standards.", max_digits=3, decimal_places=2, default=0.6)    #Replacement - Reset of some percentage of existing units to new standards.
    #    #Commercial Energy (Electricity & Gas) ---------------------------------------------
    ComEnrgyNewConst = models.DecimalField("New construction - Percentage reduction from baseline rates by a horizon year.", max_digits=5, decimal_places=2, default=30)     #New construction - Percentage reduction from baseline rates by a horizon year.
    ComEnrgyRetro	 = models.DecimalField("Retrofits - Year-upon-year - percentage reduction.", max_digits=3, decimal_places=2, default=0.8 )   #Retrofits - Year-upon-year - percentage reduction.
    ComEnrgyReplcmt  = models.DecimalField("Replacement - Reset of some percentage of existing units to new standards.", max_digits=3, decimal_places=2, default=1.0 )    #Replacement - Reset of some percentage of existing units to new standards.
    #    #Residential Water (Indoor & Outdoor) ----------------------------------------------
    ResWatrNewConst = models.DecimalField("Residential New construction",  max_digits=5, decimal_places=2, default=30 )     #New construction
    ResWatrRetro	= models.DecimalField("Residential Retrofits", max_digits=3, decimal_places=2, default=0.05 )   #Retrofits
    ResWatrReplcmt  = models.DecimalField("Residential Replacement", max_digits=3, decimal_places=2, default=0.06 )  #Replacement
    #    #Commercial & Industrial Water (Indoor & Outdoor) ----------------------------------
    ComIndWatrNewConst = models.DecimalField("Commercial New construction", max_digits=5, decimal_places=2, default=30 )   #New construction
    ComIndWatrRetro    = models.DecimalField("Commercial Retrofits", max_digits=3, decimal_places=2, default=0.08 ) #Retrofits
    ComIndWatrReplcmt  = models.DecimalField("Commercial Replacement", max_digits=3, decimal_places=2, default=0.2 ) #Replacement
    #
    #    #Additional Parameters -------------------------------------------------------------
    #
    ##    YearsBasetoHoriz = 45         #Number of years between base and horizon years
    #
    Water_GPCD_SF =	models.IntegerField("Indoor per-capita single family gallons per day", default=80)            #Indoor per-capita single family gallons per day
    Water_GPCD_MF = models.IntegerField("Indoor per-capita multifamily gallons per day", default=70)          #Indoor per-capita multifamily gallons per day:
    Water_GPED_Retail = models.IntegerField("Indoor per-employee gallons per day, Retail", default=100)       #Indoor per-employee gallons per day, Retail
    Water_GPED_Office = models.IntegerField("Indoor per-employee gallons per day, Office", default=50)      #Indoor per-employee gallons per day, Office
    Water_GPED_Industrial = models.IntegerField("Indoor per-employee gallons per day, Industrial", default=100)   #Indoor per-employee gallons per day, Industrial
    Water_GPED_School = models.IntegerField("Indoor per-employee gallons per day, School", default=86)        #Indoor per-employee gallons per day, School

    #    #Industrial energy intensity: Annual Energy use per Employee
    ann_ind_elec_peremp = models.FloatField("Annual Industrial Energy Use per Employee: kwh", default=27675.45)         #kwh
    ann_ind_gas_peremp = models.FloatField("Annual Industrial Energy Use per Employee: thm", default=767.56)            #thm

    def __unicode__(self):
        return unicode("Energy & Water Policy config for %s" % self.scenario.name)

    class Meta(object):
        abstract = True
        app_label = 'footprint'

class TemplateEnergyWaterFeature(EnergyWaterFeature):
    """
        Template subclass so that south generates migrations that we can apply to the dynamically generated subclasses
    """
    class Meta(object):
        app_label = 'footprint'
        abstract = False

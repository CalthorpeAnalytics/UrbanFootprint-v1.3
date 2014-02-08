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
from footprint.main.models.config.scenario import Scenario

__author__ = 'calthorpe_associates'

class DialUp(models.Model):
    scenario = models.OneToOneField(Scenario, primary_key=True)

    single_family_detached = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    single_family_attached = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    multi_family = models.DecimalField(max_digits=3, decimal_places=2, default=0)

    office_employment = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    retail_employment = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    industrial_employment = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    def __unicode__(self):
        return unicode("Global Dialup config for %s" % self.scenario.name)

    class Meta:
        app_label='main'


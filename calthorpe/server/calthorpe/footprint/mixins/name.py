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
__author__ = 'calthorpe'

from django.db import models

class Name(models.Model):
    """
        Mixin applied to classes whose instances are named. Name is a human-friendly name designed for internationalization.
        Keys, by contrast, serve as ids to resolve database tables.
    """
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return "name:{0}, description:{1}".format(self.name, self.description)

    class Meta:
        abstract = True


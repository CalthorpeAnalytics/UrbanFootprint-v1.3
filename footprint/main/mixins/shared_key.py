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

__author__ = 'calthorpe_associates'

class SharedKey(models.Model):
    """
        Mixin applied to classes that use a alpha-numeric key for naming database tables. Keys must not contain spaces. They represent a human-readable identifier used to lookup by predefined constants. Unlike the Key mixin, this key field has no unique constraint. It is useful when multiple versions of something are available, such as multiple DbEntities, and they should be selected between.
    """
    key = models.CharField(max_length=50, null=False, blank=False)

    @classmethod
    def unique_key(cls):
        """
            Indicates to mixers that the key need not be unique
        :return:
        """
        return False

    def __unicode__(self):
        return "key:{0}".format(self.key)

    class Meta:
        abstract = True


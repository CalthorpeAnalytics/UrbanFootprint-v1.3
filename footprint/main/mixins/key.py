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

class Key(models.Model):
    """
        Mixin applied to classes that use a alpha-numeric key for naming database tables. Keys must not contain spaces.
        They represent a human-readable identifier used to test whether instances should be gotten or created.
        There is a unique constraint on the key. Use SharedKey for model classes that need multiple instances to share
        a key.
    """
    key = models.CharField(max_length=120, null=False, blank=False, unique=True)

    def __unicode__(self):
        return "key:{0}".format(self.key)

    @classmethod
    def unique_key(cls):
        """
            Indicates to mixers that the key must be unique.
        :return:
        """
        return True

    class Meta:
        abstract = True
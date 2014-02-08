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
from footprint.utils.utils import resolve_model

__author__ = 'calthorpe'

class ScopedKey(models.Model):
    """
        This is just like the Key mixin but it doesn't enforce a unique constraint on the key in the database. The key/scope should be unique per config_entity scope, however, and enforced in code.
    """
    key = models.CharField(max_length=120, null=False, blank=False, unique=False)

    # Represents the scope of the key. It should be a ConfigEntity key or something similar
    scope = models.CharField(max_length=120, null=False, blank=False, unique=False)

    def __unicode__(self):
        return "key:{0}, scope:{1}".format(self.key, self.scope)

    @property
    def class_scope(self):
        """
            Resolve the actual model class, since it's non-trivial to store in the database
        :return:
        """
        return resolve_model('footprint.{0}'.format(self.scope))

    def __unicode__(self):
        return "key:{0}".format(self.key)

    @classmethod
    def unique_key(cls):
        """
            Indicates to mixers that the key must be unique in the scope it pertains to.
        :return:
        """
        return True

    class Meta:
        abstract = True


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

from footprint.main.models.config.policy_set import PolicySet

__author__ = 'calthorpe_associates'

from django.contrib.gis.db import models

class PolicySets(models.Model):
    """
        Represents a collection of PolicySets where a default may be specified
    """
    policy_sets = models.ManyToManyField(PolicySet)

    def add_policy_sets(self, *policy_sets):
        """
            Adds one or more PolicySets to the instance's collection. If the instance has not yet overriden its parents' sets, the parents sets will be adopted and then the given built_form_sets will be added. PolicySets matching that of the parent (if the parent's are adopted) will be ignored
        :return: The computed results after adding the given items
        """
        self._add('policy_sets', *policy_sets)

    def remove_policy_sets(self, *policy_sets):
        """
            Removes the given policy_sets from the instances collection. These may be either items inherited from an ancestor or the instance's own items
        :param policy_sets:
        :return: The computed results after removing the given items
        """
        self._remove('policy_sets', *policy_sets)

    class Meta:
        abstract = True


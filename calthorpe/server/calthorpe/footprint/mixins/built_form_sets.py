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
from footprint.models.built_form.built_form_set import BuiltFormSet
from django.contrib.gis.db import models
__author__ = 'calthorpe'

class BuiltFormSets(models.Model):
    """
        Represents a collection of BuiltFormSets where a default may be specified
    """
    built_form_sets = models.ManyToManyField(BuiltFormSet)

    def add_built_form_sets(self, *built_form_sets):
        """
            Adds one or more BuiltFormSets to the instance's collection. If the instance has not yet overriden its parents' sets, the parents sets will be adopted and then the given built_form_sets will be added
        :return: The computed results after adding the given items
        """
        self._add('built_form_sets', *built_form_sets)

    def remove_built_form_sets(self, *built_form_sets):
        """
            Removes the given built_form_sets from the instances collection. These may be either items inherited from an ancestor or the instance's own items
        :param built_form_sets:
        :return: The computed results after removing the given items
        """
        self._remove('built_form_sets', *built_form_sets)

    class Meta:
        abstract = True

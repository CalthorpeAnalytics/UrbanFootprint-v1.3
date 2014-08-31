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
from datetime import datetime
from footprint.main.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.main.mixins.percent import Percent
from footprint.main.models.built_form.built_form import BuiltForm
from footprint.main.models.built_form.placetype_component import PlacetypeComponent
from django.db import models

__author__ = 'calthorpe_associates'

class PlacetypeComponentPercent(Percent):
    """
        Many-to-many "through" class adds a percent field
    """
    objects = GeoInheritanceManager()
    placetype_component = models.ForeignKey(PlacetypeComponent, null=True)
    placetype = models.ForeignKey('Placetype')

    @property
    def component_class(self):
        return self.placetype_component.subclassed_built_form.__class__.__name__
    @property
    def container_class(self):
        return self.placetype.subclassed_built_form.__class__.__name__

    class Meta(object):
        app_label = 'main'

    def component(self):
        return BuiltForm.resolve_built_form(self.placetype_component)

    def aggregate(self):
        return BuiltForm.resolve_built_form(self.placetype)


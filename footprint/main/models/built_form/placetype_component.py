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
from footprint.main.models.built_form.primary_component import PrimaryComponent
from footprint.main.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.main.models.built_form.built_form import BuiltForm
from footprint.main.mixins.built_form_aggregate import BuiltFormAggregate
from footprint.main.mixins.name import Name
import logging

logger = logging.getLogger(__name__)

__author__ = 'calthorpe_associates'

class PlacetypeComponentCategory(Name):
    contributes_to_net = models.BooleanField()
    objects = GeoInheritanceManager()

    class Meta(object):
        app_label = 'main'


class PlacetypeComponent(BuiltForm, BuiltFormAggregate):
    """
        PlacetypeComponent represents a mix of PrimaryComponents, such as a "Rural Community College" or a "Boulevard"
    """
    objects = GeoInheritanceManager()
    primary_components = models.ManyToManyField(PrimaryComponent, through='PrimaryComponentPercent')
    component_category = models.ForeignKey(PlacetypeComponentCategory)

    def get_component_field(self):
        return self.__class__.primary_components

    class Meta(object):
        app_label = 'main'

    def calculate_gross_net_ratio(self):
        return 1

    def get_aggregate_field(self):
        return self.placetype_set

    def get_aggregate_built_forms(self):
        return self.placetype_set.all()

    def get_percent_set(self):
        return self.primarycomponentpercent_set

# coding=utf-8
from footprint.mixins.name import Name

__author__ = 'calthorpe'
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
from django.db.models.signals import post_save

from footprint.models.built_form.primary_component import PrimaryComponent
#from calthorpe.footprint.utils.subclasses import receiver_subclasses
from footprint.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.mixins.building_aggregate import BuildingAttributeAggregate

from built_form import on_collection_modify, BuiltForm

class PlacetypeComponentCategory(Name):
    contributes_to_net = models.BooleanField()
    objects = GeoInheritanceManager()

    class Meta(object):
        app_label = 'footprint'


class PlacetypeComponent(BuildingAttributeAggregate, BuiltForm):
    """
        PlacetypeComponent represents a mix of PrimaryComponents, such as a "Rural Community College" or a "Boulevard"
    """
    objects = GeoInheritanceManager()
    primary_components = models.ManyToManyField(PrimaryComponent, through='PrimaryComponentPercent')
    component_category = models.ForeignKey(PlacetypeComponentCategory)

    def get_component_field(self):
        return self.__class__.primary_components

    class Meta(object):
        app_label = 'footprint'

    def calculate_gross_net_ratio(self):
        return 1

    def get_parent_field(self):
        return self.placetype_set


def on_instance_modify(sender, **kwargs):
    instance = kwargs['instance']
    for parent_object in instance.get_parent_field().all():
        parent_object.aggregate_built_form_attributes()


post_save.connect(on_collection_modify, sender=PlacetypeComponent.primary_components.through)
post_save.connect(on_instance_modify, sender=PlacetypeComponent)

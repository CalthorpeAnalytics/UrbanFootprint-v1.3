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
from django.db.models.signals import post_save
#from calthorpe.main.utils.subclasses import receiver_subclasses
from footprint.main.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.main.models.built_form.building_component import BuildingComponent
from footprint.main.mixins.building_aggregate import BuildingAttributeAggregate
from footprint.main.mixins.building_attributes import BuildingAttributes

from footprint.main.models.built_form.placetype_component import PlacetypeComponent
from footprint.main.models.built_form.building import Building
from footprint.main.models.built_form.buildingtype_category import BuildingtypeCategory

__author__ = 'calthorpe_associates'

#@receiver_subclasses(post_save, ConfigEntity, "config_entity_post_save")
from built_form import on_collection_modify

class BuildingType(BuildingComponent, BuildingAttributeAggregate, PlacetypeComponent, BuildingAttributes):
    """
        BuildingType represents a mix of template building, such as a Rural Community College
    """
    objects = GeoInheritanceManager()

    buildings = models.ManyToManyField(Building, through='BuildingPercent')
    category = models.ForeignKey(BuildingtypeCategory, null=True)

    def __init__(self, *args, **kwargs):
        super(BuildingType, self).__init__(*args, **kwargs)

    def get_component_field(self):
        return self.__class__.buildings

    class Meta(object):
        app_label = 'main'

    def get_parent_field(self):
        return self.placetype_set

def on_instance_modify(sender, **kwargs):
    instance = kwargs['instance']
    for parent_object in instance.get_parent_field().all():
        parent_object.aggregate_built_form_attributes()

post_save.connect(on_collection_modify, sender=BuildingType.buildings.through)
post_save.connect(on_instance_modify, sender=BuildingType)

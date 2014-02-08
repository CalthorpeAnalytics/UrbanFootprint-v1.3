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
from django.db.models.signals import post_save
from django.db.models import Sum
from footprint.main.managers.geo_inheritance_manager import GeoInheritanceManager


from footprint.main.models.built_form.built_form import BuiltForm


class Building(BuiltForm, BuildingComponent):
    """
        Building represents a template building, such as a Rural Community College
    """
    objects = GeoInheritanceManager()

    class Meta(object):
    # This is not abstract so that django can form a many-to-many relationship with it in built_form_set
        app_label = 'main'

    def get_parent_field(self):
        return self.buildingtype_set

def on_instance_modify(sender, **kwargs):
    instance = kwargs['instance']
    for parent_object in instance.get_parent_field().all():
        if parent_object.buildingpercent_set.all().aggregate(Sum('percent')) > .95:
            parent_object.aggregate_built_form_attributes()
        else:
            pass

post_save.connect(on_instance_modify, sender=Building)

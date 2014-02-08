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
from django.db.models.fields.related import ForeignKey

from footprint.main.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.main.mixins.name import Name
from footprint.main.models.presentation.presentation_medium import PresentationMedium
from footprint.main.models.tag import Tag

__author__ = 'calthorpe_associates'

class Layer(PresentationMedium, Name):

    """
        Relational data configured for display as a map layer
    """
    objects = GeoInheritanceManager()

    # Reference to the origin of this layer if it was cloned
    origin_instance = ForeignKey('Layer', null=True)
    # Indicates along with the origin_intance that the Layer is created from the origin_instance's selection
    create_from_selection = models.BooleanField(default=False)

    def update_tags(self):
        """
            Tag an untagged layer with the default tag, based on its config_entity and db_entity
        """
        if not len(self.tags.all()) > 0:
            # Tag the layer with defaults
            self.tags.add(*[
                Tag.objects.update_or_create(
                    tag=self.presentation.config_entity.db_entity_owner(self.db_entity_interest.db_entity).key)[0]
            ])

    class Meta(object):
        app_label = 'main'



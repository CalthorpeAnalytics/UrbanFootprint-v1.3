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
from model_utils.managers import InheritanceManager
from picklefield import PickledObjectField
from footprint.main.lib.functions import first
from footprint.main.mixins.deletable import Deletable
from footprint.main.mixins.name import Name
from footprint.main.mixins.scoped_key import ScopedKey
from footprint.main.models.config.config_entity import ConfigEntity

__author__ = 'calthorpe_associates'

class Presentation(Name, ScopedKey, Deletable):
    """
        Creates a presentation, such as a map, result page, or report specifc to a ConfigEntity.
        The presentation is concerned with the visualization of the properties of the ConfigEntity.
    """

    # Presentations have sublasses--enable subclass querying
    objects = InheritanceManager()

    # Stores a serialized instance of a Configuration
    configuration = PickledObjectField(null=True)

    @property
    def presentation_media(self):
        raise "Must overload this in subclass"

    config_entity = models.ForeignKey('ConfigEntity', null=False)
    @property
    def subclassed_config_entity(self):
        """
            Resolves the config_entity to its subclass version. This garbage should all be done elegantly by Django,
            maybe in the newest version. Otherwise refactor to generalize
        :return:
        """
        return ConfigEntity._subclassed_config_entity(self.config_entity)

    def db_entities(self):
        """
            Returns all DbEntities associated to the presentation via PresentationMedia instance. This will always be
            a subset of the config_entity.computed_db_entities(). Since the PresentationMedia's db_entity_key implies
            the DbEntity that is selected among two or more of the same key, only one DbEntity per key is returned,
            the selected or only one
        :return:
        """
        return self.config_entity().computed_db_entities().filter(key__in=
            map(lambda presentation_media: presentation_media.db_entity_key,
                self.presentationmedium_set.exclude(db_entity_key__isnull=True)))

    def __unicode__(self):
        return "{0}, {1}".format(Name.__unicode__(self), ScopedKey.__unicode__(self))

    class Meta(object):
        app_label = 'main'


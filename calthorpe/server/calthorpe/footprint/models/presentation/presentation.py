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
from footprint.lib.functions import first
from footprint.mixins.name import Name
from footprint.mixins.scoped_key import ScopedKey
from footprint.models import Scenario, ConfigEntity
from footprint.models.presentation.medium import Medium

__author__ = 'calthorpe'

class Presentation(Name, ScopedKey):
    """
        Creates a presentation, such as a map, result page, or report specifc to a ConfigEntity.
        The presentation is concerned with the visualization of the properties of the ConfigEntity.
    """

    # Presentations have sublasses--enable subclass querying
    objects = InheritanceManager()

    media = models.ManyToManyField(Medium, through='PresentationMedium')

    # Stores a serialized instance of a Configuration
    configuration = PickledObjectField(null=True)

    config_entity = models.ForeignKey('ConfigEntity', null=False)
    @property
    def subclassed_config_entity(self):
        """
            Resolves the config_entity to its subclass version. This garbage should all be done elegantly by Django,
            maybe in the newest version. Otherwise refactor to generalize
        :return:
        """
        config_entity = ConfigEntity.objects.filter(id=self.config_entity.id).select_subclasses()[0]
        return self.resolve_scenario(config_entity) if isinstance(config_entity, Scenario) else config_entity

    @staticmethod
    def resolve_scenario(scenario):
        for scenario_type in ['basescenario', 'futurescenario']:
            if hasattr(scenario, scenario_type):
                return getattr(scenario, scenario_type)
        return scenario

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
        app_label = 'footprint'


    # TODO this stuff could be used for standard sorting
    # def __init__(self,  *args, **kwargs):
    #     super(LayerLibrary, self).__init__(*args, **kwargs)
    #     # Default the SortType for each collection if not passed in
    #     for collection_attribute, sort_key in {
    #         'media':Keys.SORT_TYPE_KEY,
    #         'presentationmedium_set':Keys.SORT_TYPE_PRESENTATION_MEDIA_DB_ENTITY_KEY,
    #         'db_entities':Keys.SORT_TYPE_KEY}.items():
    #
    #         if self.sort_types.get(collection_attribute, None):
    #             self.sort_types[collection_attribute] = SortType.objects.get(key=sort_key)
    #
    # def sorted_presentation_media(self, sort_type=None, **kwargs):
    #     """
    #         Sorts the PresentationMedia, the through class for Media. This is useful if you want to sort by and expose attributes such as the db_entity_key's DbEntity of the PresentationMedia
    #     :param sort_type: A SortType instance. Defaults to self.sort_type
    #     :return:
    #     """
    #     self.sorted(self.presentationmedium_set.filter(**kwargs), 'presentationmedium_set', sort_type)
    #
    # def sorted_media(self, sort_type=None, **kwargs):
    #     """
    #         Sorts the Media
    #     :param sort_type: A SortType instance. Defaults to self.sort_type
    #     :return:
    #     """
    #     self.sorted(self.media.filter(**kwargs), 'media', sort_type)
    #
    # def sorted_db_entities(self, sort_type=None, **kwargs):
    #     """
    #         Sorts the DbEntities of the PresentationMedia, for the PresentationMedia that associate to DbEntities
    #     :param sort_type: A SortType instance. Defaults to self.sort_type
    #     :return:
    #     """
    #     self.sorted(self.db_entities().filter(**kwargs), 'db_entities', sort_type)
    #
    # def sorted(self, queryset, attribute, sort_type=None):
    #     """
    #         Return all the PresentationMedia of the Library sorted by the sort_type of the given attribute
    #
    #     :param queryset: The QuerySet of the collection being sorted
    #     :param attribute: The attribute name of the collection, used to look up its SortType
    #     :param sort_type: Optionally overrides the stored SortType for the queryset
    #     :return: The QuerySet sorted using order_by based on the SortType
    #     """
    #     sort_type = sort_type or self.sort_types[attribute]
    #     return queryset.order_by(sort_type.order_by) if sort_type.order_by else queryset.all()
    #


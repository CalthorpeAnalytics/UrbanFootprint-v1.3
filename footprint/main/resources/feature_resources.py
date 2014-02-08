# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
#
# Copyright (C) 2013 Calthorpe Associates
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
from django.db import models
from inflection import singularize

from tastypie import fields
from tastypie.models import ApiKey
from footprint.main.lib.functions import map_dict_to_dict, map_dict_value
from footprint.main.models import Layer
from footprint.main.models.presentation.layer_selection import get_or_create_dynamic_layer_selection_class_and_table
from footprint.main.resources.config_entity_resources import ConfigEntityResource
from footprint.main.resources.footprint_resource import FootprintResource
from footprint.main.resources.mixins.dynamic_resource import DynamicResource
from footprint.main.utils.dynamic_subclassing import get_dynamic_resource_class
from footprint.main.utils.subclasses import match_subclasses
from footprint.main.utils.utils import get_one_or
from tastypie.constants import ALL_WITH_RELATIONS, ALL
from footprint.main.models.geospatial.feature_class_creator import FeatureClassCreator

class FeatureResource(DynamicResource):
    # Dehydrate the class config_entity into each instance. This is useful for Api consumers since the
    # feature id alone is not distinct when using an abstract Feature class
    # readonly=True so that we never hydrate this, which takes a long time. We always resolve the config entity by id
    # in create_subclass below.
    config_entity = fields.ToOneField(ConfigEntityResource, 'config_entity', full=False, readonly=True)

    def resolve_feature_class(self, config_entity, layer):
        return config_entity.feature_class_of_db_entity_key(layer.db_entity_key) if \
            layer else \
            config_entity.feature_class_of_base_class(self._meta.queryset.model)

    def create_subclass(self, params, **kwargs):
        """
            Subclass this class to create a resource class specific to the config_entity.
        :param params.layer__id: The layer id. Optional. Used to resolve the Feature/FeatureResource subclasses if we are in FeatureResource (not in a subclass)
        :return: The subclassed resource class
        """

        # Get the ConfigEntity subclass instance based on the parameter
        config_entity = self.resolve_config_entity(params)
        layer = params.get('layer__id', None) and self.resolve_layer(params)
        db_entity = layer.db_entity_interest.db_entity if layer else None

        # Use the abstract resource class queryset model or given db_entity_key to fetch the feature subclass
        feature_class = self.resolve_feature_class(config_entity, layer)
        return self.resolve_feature_resource_class(feature_class, db_entity)

    def resolve_feature_resource_class(self, feature_class, db_entity=None):
        """
            Resolve the FeatureResource subclass based on the given Feature subclass
            If self is already a subclass, just return self
            Else, return a preconfigured subclass or one dynamically created. The latter will probably be the only way in the future.
        :param db_entity: Optionally passed to configure a dynamic FeatureResource subclass
        :return: An instance
        """
        # If not already subclassed
        if self.__class__ == FeatureResource:
            descriptors = FeatureClassCreator(feature_class.config_entity, db_entity).related_descriptors() if db_entity else {}
            return self.__class__.resolve_resource_class(feature_class, descriptors)
        return self

    def dynamic_resource_class(self, params, feature_class):
        return get_dynamic_resource_class(self.__class__, feature_class)

    def search_params(self, params):
        """
            The user may optionally specify a layer_selection__id instead of feature ids when querying for features.
            This prevents huge feature id lists in the URL.
        :param params
        :return:
        """
        if params.get('layer__id'):
            layer_selection = self.resolve_layer_selection(params)
            return dict(id__in=','.join(map(lambda feature: unicode(feature.id), layer_selection.selected_features)))
        else:
            return params

    def remove_params(self, params):
        """
            layer_selection__id is converted to id__in for feature ids. The former must be removed during the
            wrapping of the resource if footprint_resource
        :param params:
        :return:
        """
        return ['layer_selection__id', 'config_entity__id', 'layer__id']

    def resolve_config_entity(self, params):
        if params.get('config_entity__id', None):
            return super(FeatureResource, self).resolve_config_entity(params)
        elif params.get('layer__id', None):
            layer = self.resolve_layer(params)
            # This hack gets us the right ConfigEntity subclass version of the instance
            return super(FeatureResource, self).resolve_config_entity(dict(config_entity__id=layer.presentation.config_entity.id))
        else:
            raise Exception("Expected config_entity__id or layer__id to be specified")

    def resolve_layer(self, params):
        return Layer.objects.get(id=params['layer__id'])

    def resolve_layer_selection(self, params):
        layer = self.resolve_layer(params)
        layer_selection_class = get_or_create_dynamic_layer_selection_class_and_table(layer, False)
        return layer_selection_class.objects.get(user=self.resolve_user(params))

    def post_save(self, request, **kwargs):
        params = request.GET
        user_id = ApiKey.objects.get(key=params['api_key']).user_id
        feature_class = self._meta.queryset.model
        feature_class.post_save(user_id)

    class Meta(DynamicResource.Meta):
        always_return_data = True
        abstract = True
        #fields = ['id']
        excludes = ['created', 'wkb_geometry']
        filtering = {
            # Accept the django query id__in
            "id": ALL
        }
        resource_name = 'feature'



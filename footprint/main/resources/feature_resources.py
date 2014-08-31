# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
#
# Copyright (C) 2014 Calthorpe Associates
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
import string

from django.db.models.query import ValuesQuerySet
from tastypie import fields
from tastypie.constants import ALL
from footprint.main.mixins.timestamps import Timestamps
from footprint.main.models import Layer
from footprint.main.lib.functions import map_dict_to_dict, map_to_dict
from footprint.main.models.geospatial.feature import PaintingFeature
from footprint.main.models.presentation.layer_selection import get_or_create_dynamic_layer_selection_class_and_table
from footprint.main.resources.config_entity_resources import ConfigEntityResource
from footprint.main.resources.mixins.dynamic_resource import DynamicResource
from footprint.main.models.geospatial.feature_class_creator import FeatureClassCreator
import logging

logger = logging.getLogger(__name__)

class FeatureResource(DynamicResource):
    # Dehydrate the class config_entity into each instance. This is useful for Api consumers since the
    # feature id alone is not distinct when using an abstract Feature class
    # readonly=True so that we never hydrate this, which takes a long time. We always resolve the config entity by id
    # in create_subclass below.
    config_entity = fields.ToOneField(ConfigEntityResource, 'config_entity', full=False, readonly=True)

    def hydrate(self, bundle):
        """
            Never allow the PaintedFeature created field to be hydrated from the user
        """
        if 'created' in bundle.data:
            del bundle.data['created']
        if 'updated' in bundle.data:
            del bundle.data['updated']
        return bundle

    class Meta(DynamicResource.Meta):
        always_return_data = True
        abstract = True
        excludes = ['wkb_geometry']
        filtering = {
            # Accept the django query id__in
            "id": ALL
        }
        resource_name = 'feature'


    def resolve_model_class(self, config_entity=None, layer=None):
        """
            Resolves the model class of the dynamic resource class. In this case it's a Feature subclass
        """
        return config_entity.db_entity_feature_class(layer.db_entity_key) if \
            layer else \
            config_entity.feature_class_of_base_class(self._meta.queryset.model)

    def feature_resource_subclass(self, layer_selection, **kwargs):
        layer = layer_selection.layer
        config_entity = layer.presentation.config_entity.subclassed_config_entity
        db_entity = layer.db_entity_interest.db_entity if layer else None
        # Use the abstract resource class queryset model or given db_entity_key to fetch the feature subclass
        feature_class = self.resolve_model_class(config_entity=config_entity, layer=layer)
        # Resolve the FeatureResource subclass based on the given Feature subclass
        # If self is already a subclass, just return self
        # Else, return a preconfigured subclass or one dynamically created. The latter will probably be the only way in the future.
        # If not already subclassed
        if self.__class__ == FeatureResource:
            descriptors = FeatureClassCreator(feature_class.config_entity,
                                              db_entity).related_descriptors() if db_entity else {}
            queryset = layer_selection.selected_features_or_values


            if not kwargs.get('query_may_be_empty') and queryset.count()==0:
                raise Exception("Unexpected empty queryset for layer_selection features")
            is_values_queryset = isinstance(queryset, ValuesQuerySet)
            if is_values_queryset:
                join_feature_class = layer_selection.create_join_feature_class() if is_values_queryset else feature_class
                # Force the queryset to our new class so that Tastypie can map the dict results to it
                queryset.model = join_feature_class
                return self.__class__.resolve_resource_class(
                    join_feature_class,
                    descriptors,
                    queryset=queryset,
                    base_resource_class=self.join_feature_resource_class(join_feature_class))
            else:
                abstract_feature_resource_class = PaintingFeatureResource if \
                    issubclass(feature_class, PaintingFeature) else \
                    self.__class__
                resource_class = abstract_feature_resource_class.resolve_resource_class(
                    feature_class,
                    descriptors,
                    queryset=queryset)
                logger.debug("Count of rows in query set: {0}".format(resource_class.Meta.queryset.count()))
                return resource_class
        return self

    def create_subclass(self, params, **kwargs):
        """
            Subclass this class to create a resource class specific to the config_entity.
        :param params.layer__id: The layer id. Optional. Used to resolve the Feature/FeatureResource subclasses if we are in FeatureResource (not in a subclass)
        :return: The subclassed resource class
        """

        # Get the ConfigEntity subclass instance based on the parameter
        layer_selection = self.resolve_layer_selection(params)

        return self.feature_resource_subclass(layer_selection, **kwargs)

    def join_feature_resource_class(self, join_feature_class):
        class JoinFeatureResource(FeatureResource):
            def full_dehydrate(self, bundle, for_list=False):
                # Convert the dict to the unmanaged join_feature_class instance
                field_name_lookup = map_to_dict(lambda field: [string.replace(field.name, '_x_', '__'), True], join_feature_class._meta.fields)
                # Map mapping fields
                dct = map_dict_to_dict(lambda key, value: [string.replace(key, '__', '_x_'), value] if
                    field_name_lookup.get(key) else
                    None,
                                       bundle.obj)
                obj = join_feature_class(**dct)
                new_bundle = self.build_bundle(obj=obj, request=bundle.request)
                return super(JoinFeatureResource, self).full_dehydrate(new_bundle, for_list)
        return JoinFeatureResource

    def search_params(self, params):
        """
            The user may optionally specify a layer_selection__id instead of feature ids when querying for features.
            This prevents huge feature id lists in the URL.
        :param params
        :return:
        """
        return params
        # if params.get('layer__id'):
        #     layer_selection = self.resolve_layer_selection(params)
        #     # TODO this should probably be a join to the layer_selection_features table instead
        #     return dict(id__in=','.join(map(lambda feature: unicode(feature.id), layer_selection.selected_features)))
        # else:
        #     return params

    def resolve_layer_selection(self, params):
        """
            Used to get that actual selected features, which is a short cut querying, so we don't have to query
            for potentially thousands of ids
        """
        layer = self.resolve_layer(params)
        layer_selection_class = get_or_create_dynamic_layer_selection_class_and_table(layer, False)
        return layer_selection_class.objects.get(user=self.resolve_user(params))

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
            return layer.presentation.config_entity.subclassed_config_entity
        else:
            raise Exception("Expected config_entity__id or layer__id to be specified")

    def resolve_layer(self, params):
        return Layer.objects.get(id=params['layer__id'])

class PaintingFeatureResource(FeatureResource):
    #TODO not used

    created = fields.DateField('created', readonly=True)
    created = fields.DateField('updated', readonly=True)
    def hydrate(self, bundle):
        """
            Never allow the PaintedFeature created field to be hydrated from the user
            I don't know why Tastypie sets created to null sometimes
        """
        if 'created' in bundle.data:
            del bundle.data['created']
        if 'updated' in bundle.data:
            del bundle.data['updated']
        return bundle

    class Meta(FeatureResource.Meta):
        always_return_data = True
        abstract = True
        excludes = ['wkb_geometry']
        filtering = {
            # Accept the django query id__in
            "id": ALL
        }
        resource_name = 'painting_feature'


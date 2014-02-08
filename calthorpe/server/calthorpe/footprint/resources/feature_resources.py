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

from tastypie import fields
from footprint.models import Layer
from footprint.models.presentation.layer_selection import create_dynamic_layer_selection_class_and_table
from footprint.resources.config_entity_resources import ConfigEntityResource
from footprint.resources.mixins.dynamic_resource import DynamicResource
from footprint.utils.dynamic_subclassing import get_dynamic_resource_class

class FeatureResource(DynamicResource):
    # Dehydrate the class config_entity into each instance. This is useful for Api consumers since the
    # feature id alone is not distinct when using an abstract Feature class
    config_entity = fields.ToOneField(ConfigEntityResource, 'config_entity', full=False)

    def create_subclass(self, params, config_entity=None, db_entity_key=None, **kwargs):
        """
            Subclass this class to create a resource class specific to the config_entity.
        :param params.config_entity: The config_entity id. This is required unless a config_entity is specified explicitly
        :param config_entity: Optional config_entity instance to use instead of the param when the config_entity instance
         has already been resolved
        :param db_entity_key: Optional. A second-tier abstract class like BaseFeatureResource will already
        specify this in self._meta.queryset.mode. If the caller is FeatureResource, then a db_entity_key must be passed
        in order to create the dynamic feature class. Example, passing Keys.DB_ABSTRACT_BASE_FEATURE will cause
        a BaseFeature subclass to be created based on the config_entity
        specified by passing config_entity.featurebase_class
        :return: The subclassed resource class
        """

        # Get the ConfigEntity subclass instance based on the parameter
        config_entity = self.resolve_config_entity(params)
        # Use the abstract resource class queryset model or given db_entity_key to fetch the feature subclass
        feature_class = config_entity.feature_class_of_db_entity(db_entity_key) if \
            db_entity_key else \
            config_entity.feature_class_of_base_class(self._meta.queryset.model)

        DynamicResourceClass = self.dynamic_resource_class(params, feature_class)
        return DynamicResourceClass

    def dynamic_resource_class(self, params, feature_class):
        return get_dynamic_resource_class(self.__class__, feature_class)

    def search_params(self, params):
        """
            The user may optionally specify a layer_selection__id instead of feature ids when querying for features.
            This prevents huge feature id lists in the URL.
        :param params
        :return:
        """
        if params.get('layer_selection__id'):
            layer_selection = self.resolve_layer_selection(params)
            return dict(id__in=','.join(map(lambda feature: unicode(feature.id), layer_selection.features.all())))
        else:
            return params

    def remove_params(self, params):
        """
            layer_selection__id is converted to id__in for feature ids. The former must be removed during the
            wrapping of the resource if footprint_resource
        :param params:
        :return:
        """
        return ['layer_selection__id', 'config_entity__id']

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
        layer_selection_class = create_dynamic_layer_selection_class_and_table(layer, False)
        return layer_selection_class.objects.get(id=params['layer_selection__id'])

    class Meta(DynamicResource.Meta):
        always_return_data = True
        abstract = True
        # By default we purposely limit the exposed fields to those of the abstract Feature class
        # Tastypie will otherwise show the fields of the subclass Feature class, which we can expose
        # by overriding this property in a subclass of FeatureResource
        fields = ['id', 'config_entity']
        excludes = ['created', 'wkb_geometry']
        filtering = {
            # Accept the django query id__in
            "id": ('in',),
        }



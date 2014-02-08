# UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System. #
# Copyright (C) 2013 Calthorpe Associates
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
from django.contrib.auth.models import User
from jsonify.templatetags.jsonify import jsonify
from tastypie import fields
from tastypie.constants import ALL_WITH_RELATIONS, ALL
from tastypie.contrib.gis.resources import GeometryApiField
from django.contrib.gis.geos import GEOSGeometry
from footprint.lib.functions import merge

from footprint.models import Layer, LayerLibrary
from footprint.models.presentation.layer_selection import LayerSelection, create_dynamic_layer_selection_class_and_table
from footprint.publishing import layer_publishing
from footprint.resources.feature_resources import FeatureResource
from footprint.resources.mixins.dynamic_resource import DynamicResource
from footprint.resources.mixins.mixins import ToManyFieldWithSubclasses
from footprint.resources.presentation_resources import PresentationMediumResource, PresentationResource
from footprint.resources.user_resource import UserResource
from footprint.utils.dynamic_subclassing import get_dynamic_resource_class


class LayerLibraryResource(PresentationResource):

    class Meta(PresentationResource.Meta):
        resource_name = 'layer_library'
        always_return_data = True
        queryset = LayerLibrary.objects.all()

class LayerResource(PresentationMediumResource):
    class Meta(PresentationMediumResource.Meta):
        resource_name = 'layer'
        always_return_data = True
        queryset = Layer.objects.all()
        filtering = {
            "id": ('exact',),
        }

class LayerSelectionResource(DynamicResource):
    """
        An abstract resource class that is subclassed by the resources.py wrapper to match a particular layer_id
    """

    # geojson property that causes sets the model property bounds, which is a special setter that sets the geography of the model
    bounds = GeometryApiField(null=True, blank=True, default=lambda:{})

    # The layer instance is not a LayerSelection field, but a property of the LayerSelection subclass
    user = fields.ToOneField(UserResource, 'user', readonly=True, full=False)
    query = fields.DictField()

    layer_lambda = lambda bundle: bundle.obj.__class__.layer
    selection_layer = fields.ToOneField(LayerResource, attribute=layer_lambda, readonly=True, full=False)

    def hydrate(self, bundle):
        """
            Clear the previous bounds or query if the other is sent
        :param bundle:
        :return:
        """
        if bundle.data['bounds']:
            bundle.data['query'] = None
            bundle.obj.query = None
        elif bundle.data['query']:
            bundle.data['bounds'] = None
            bundle.obj.bounds = None
        return bundle

    def hydrate_query(self, bundle):
        if bundle.data['query'] and len(bundle.data['query'].keys()) > 0:
            # This triggers the _query setter and sets query
            bundle.obj._query = bundle.data['query']

        return bundle

    def hydrate_bounds(self, bundle):
        """
            Convert the bounds from JSON to the GEOSGeometry format
            bounds is a python getter/setter that sets the geometry field and the features list
            by executing a geodjango query
        :param bundle
        :return:
        """
        if bundle.data['bounds'] and len(bundle.data['bounds'].keys()) > 0:
            try:
                bundle.obj.bounds = GEOSGeometry(jsonify(bundle.data['bounds']))
            except:
                # TODO log warning
                bundle.obj.bounds = GEOSGeometry('MULTIPOLYGON EMPTY')
        elif not bundle.data['query']:
            bundle.obj.bounds = GEOSGeometry('MULTIPOLYGON EMPTY')

        return bundle

    def create_subclass(self, params, **kwargs):
        """
            Subclasses the LayerSelectionResource instance's class for the given config_entity.
            This resource class can the return all LayerSelection instances for the given config_entity scope
        :param params.config_entity
        :return:
        """

        config_entity = self.resolve_config_entity(params)
        layer = self.resolve_layer(params)
        layer_selection_class = create_dynamic_layer_selection_class_and_table(layer)
        if kwargs.get('method', None) == 'PATCH':
            layer = Layer.objects.get(id=params['layer__id'])
            DynamicFeatureResourceClass = FeatureResource().create_subclass(merge(params, dict(config_entity__id=config_entity.id)), config_entity=config_entity, db_entity_key=layer.db_entity_key)
            features = fields.ToManyField(DynamicFeatureResourceClass, attribute='selected_features', readonly=True, null=True, full=False)
        else:
            features = ToManyFieldWithSubclasses(
                'footprint.resources.feature_resources.FeatureResource',
                attribute='selected_features',
                full=False,
                readonly=True,
                null=True)
        # Create a subclass of FeatureResource to wrap the Feature class of that represents the given db_entity_key
        return get_dynamic_resource_class(
            self.__class__,
            layer_selection_class,
            features = features
        )

    def search_params(self, params):
        """
        :param params
        :return:
        """
        user = User.objects.get(username=params['username'])
        return dict(user__id=user.id)

    def post_save(self, request, **kwargs):
        """
            Call the layer publisher on save manually since the signaling doesn't seem to work with dynamic
            classes
        :param request:
        :return:
        """
        layer_instance = self.resolve_layer(kwargs['GET'])
        user = User.objects.get(username=request.GET['username'])
        layer_publishing.on_layer_selection_post_save_layer(self, layer=layer_instance, user=user)

    def resolve_layer(self, params):
        return Layer.objects.get(id=params['layer__id'])

    def resolve_config_entity(self, params):
        return Layer.objects.get(id=params['layer__id']).presentation.config_entity

    class Meta(DynamicResource.Meta):
        abstract=True
        filtering = {
            # Accept the django query layer and user ids to identify the Layer and User
            # layer_id is used to resolve the dynamic subclass for PATCH
            #"layer": ALL_WITH_RELATIONS,

            # There is only one instance per user_id. This should always be specified for GETs
            "user": ALL_WITH_RELATIONS,
            "id": ALL
        }
        always_return_data = True
        # We don't want to deliver this, the user only sees and manipulates the bounds
        excludes = ['geometry']
        resource_name = 'layer_selection'
        # The following is set in the subclass based upon the dynamic model class passed into the class creator
        queryset = LayerSelection.objects.all() # Just for model_class initialization, should never be called

from tastypie.contrib.gis.resources import GeometryApiField
from footprint.main.resources.layer_resources import LayerResource
from footprint.main.utils.query_parsing import resolve_related_model_path_via_geographies, model_field_paths

__author__ = 'calthorpe'

from django.contrib.auth.models import User
import geojson
from tastypie import fields
from tastypie.constants import ALL_WITH_RELATIONS, ALL
from footprint.main.lib.functions import deep_merge, flat_map, map_to_dict, merge
from footprint.main.models.config.scenario import FutureScenario
from footprint.main.models.geospatial.db_entity_configuration import update_or_create_db_entity
from footprint.main.models.geospatial.feature_class_creator import FeatureClassCreator
from footprint.main.resources.pickled_dict_field import PickledDictField
from footprint.main.models import Layer
from footprint.main.models.presentation.layer_selection import LayerSelection, get_or_create_dynamic_layer_selection_class_and_table
from footprint.main.resources.feature_resources import FeatureResource
from footprint.main.resources.mixins.dynamic_resource import DynamicResource
from footprint.main.resources.mixins.mixins import ToManyFieldWithSubclasses
from footprint.main.resources.user_resource import UserResource
from footprint.main.utils.dynamic_subclassing import get_dynamic_resource_class
from footprint.main.utils.query_parsing import model_field_paths

class CustomGeometryApiField(GeometryApiField):
    def hydrate(self, bundle):
        return super(GeometryApiField, self).hydrate(bundle)
        # I don't know why the base class does this
        #if value is None:
        #    return value
        #return simplejson.dumps(value)

class LayerSelectionResource(DynamicResource):
    """
        An abstract resource class that is subclassed by the resources.py wrapper to match a particular layer_id
    """

    bounds = CustomGeometryApiField(attribute='bounds', null=True, blank=True, default=lambda:{})

    unique_id = fields.CharField(attribute='unique_id', null=False, readonly=True)
    # The layer instance is not a LayerSelection field, but a property of the LayerSelection subclass
    user = fields.ToOneField(UserResource, 'user', readonly=True, full=False)
    filter = PickledDictField(attribute='filter', null=True, blank=True)
    group_bys = PickledDictField(attribute='group_bys', null=True, blank=True)
    joins = fields.ListField(attribute='joins', null=True, blank=True)
    aggregates = PickledDictField(attribute='aggregates', null=True, blank=True)

    result_fields = fields.ListField(attribute='result_fields', null=True, blank=True, readonly=True)
    result_field_title_lookup = PickledDictField(attribute='result_field_title_lookup', null=True, blank=True, readonly=True)

    summary_results = fields.ListField(attribute='summary_results', null=True, blank=True, readonly=True)
    summary_fields = fields.ListField(attribute='summary_fields', null=True, blank=True, readonly=True)
    summary_field_title_lookup = PickledDictField(attribute='summary_field_title_lookup', null=True, blank=True, readonly=True)

    query_strings = PickledDictField(attribute='query_strings', null=True, blank=True,
                                     default=lambda: dict(aggregates_string=None, filter_string=None, group_by_string=None))

    query_sql = fields.CharField(attribute='query_sql', null=True, readonly=True)
    summary_query_sql = fields.CharField(attribute='summary_query_sql', null=True, readonly=True)

    # TODO remove
    filter_by_selection = fields.BooleanField(attribute='filter_by_selection', default=False)

    layer_lambda = lambda bundle: bundle.obj.__class__.layer
    selection_layer = fields.ToOneField(LayerResource, attribute=layer_lambda, readonly=True, full=False)

    selection_extent = CustomGeometryApiField(attribute='selection_extent', null=True, blank=True, default=lambda:{}, readonly=True)

    def full_hydrate(self, bundle, for_list=False):
        """
            Clear the previous bounds or query if the other is sent
        :param bundle:
        :return:
        """

        # Remove the computed properties. Some or all will be set
        bundle.obj.summary_results = None
        bundle.obj.summary_fields = None
        bundle.obj.summary_field_title_lookup = None

        # Call super to populate the bundle.obj
        bundle = super(LayerSelectionResource, self).full_hydrate(bundle)
        for attr in ['filter', 'aggregates', 'group_bys', 'joins', 'bounds']:
            if not bundle.data.get(attr, None):
                setattr(bundle.obj, attr, None)

        # TODO move everything under here to a method of layer_selection
        # Update the features to the queryset
        feature_class = bundle.obj.feature_class()
        query_set = bundle.obj.create_query_set(feature_class.objects)
        bundle.obj.update_features(query_set)

        related_models = bundle.obj.resolve_related_models()
        # Get the related model paths final segment. We want to map these to the db_entity_key names
        related_model_path_to_name = map_to_dict(
            lambda related_model:
                [resolve_related_model_path_via_geographies(feature_class.objects, related_model).split('__')[1],
                 related_model.db_entity_key],
                related_models
            )

        # Parse the QuerySet to get the result fields and their column title lookup
        if len(bundle.obj.joins or []) > 0:
            values_query_set = bundle.obj.values_query_set(query_set)
        else:
            field_paths = model_field_paths(feature_class, fields=feature_class.limited_api_fields())
            values_query_set = (query_set if query_set else feature_class.objects).values(*field_paths)

        bundle.obj.result_fields, bundle.obj.result_field_title_lookup = values_query_set.result_fields_and_title_lookup(
            related_models=related_models,
            # map_path_segments maps related object paths to their model name, and removes the geographies segment of the path
            map_path_segments=merge(dict(geographies=None),
                                    related_model_path_to_name)
        )

        # Create the summary results from the entire set
        summary_query_set = bundle.obj.create_summary_query_set(
            feature_class.objects)
        if summary_query_set:
            # Update the summary results
            bundle.obj.update_summary_results(summary_query_set)
        else:
            bundle.obj.clear_summary_results()

        # Debugging
        bundle.obj.query_sql = values_query_set.query
        bundle.obj.summary_query_sql = summary_query_set.query if hasattr(summary_query_set, 'query') else None

        return bundle

    def query_data_specified(self, data):
        return data.get('query', None)

    def create_subclass(self, params, **kwargs):
        """
            Subclasses the LayerSelectionResource instance's class for the given config_entity.
            This resource class can the return all LayerSelection instances for the given config_entity scope
        :param params.config_entity
        :return:
        """

        layer = self.resolve_layer(params)
        layer_selection_class = get_or_create_dynamic_layer_selection_class_and_table(layer)
        if not layer_selection_class:
            raise Exception("Layer with db_entity_key %s has no feature_class. Its LayerSelections should not be requested" % layer.db_entity_key)
        if kwargs.get('method', None) == 'PATCH':
            # Create a simple Feature resource subclass (no related fields needed)
            feature_resource_class = FeatureResource().create_subclass(params, query_may_be_empty=True)
            features = fields.ToManyField(feature_resource_class, attribute='selected_features', readonly=True, null=True, full=False)
        else:
            features = ToManyFieldWithSubclasses(
                'footprint.main.resources.feature_resources.FeatureResource',
                attribute='selected_features',
                full=False,
                readonly=True,
                null=True)
            # Create a subclass of FeatureResource to wrap the Feature class of that represents the given db_entity_key
        return get_dynamic_resource_class(
            self.__class__,
            layer_selection_class,
            fields=dict(features=features)
        )

    def search_params(self, params):
        """
        :param params
        :return:
        """
        user = User.objects.get(username=params['username'])
        return dict(user__id=user.id)

    def resolve_config_entity(self, params):
        return Layer.objects.get(id=params['layer__id']).presentation.config_entity

    def create_layer_from_layer_selection(self, params):
        # Resolve the source layer from the layer_selection__id
        source_layer = self.resolve_layer(params)
        config_entity = source_layer.presentation.config_entity
        db_entity = source_layer.db_entity_interest.db_enitty
        feature_class = FeatureClassCreator(config_entity, db_entity).dynamic_model_class()
        layer = Layer.objects.get(presentation__config_entity=config_entity, db_entity_key=db_entity.key)
        layer_selection = get_or_create_dynamic_layer_selection_class_and_table(layer, False).objects.all()[0]
        # TODO no need to do geojson here
        feature_dict = dict(
            type="Feature"
        )
        feature_dicts = map(lambda feature:
                            deep_merge(feature_dict, {"geometry":geojson.loads(feature.wkb_geometry.json)}),
                            layer_selection.selected_features or feature_class.objects.all())
        json = dict({ "type": "FeatureCollection",
                      "features": feature_dicts
        })
        db_entity_configuration = update_or_create_db_entity(config_entity, **dict(
            class_scope=FutureScenario,
            name='Import From Selection Test',
            key='import_selection_test',
            url='file://notusingthis'
        ))
        self.make_geojson_db_entity(config_entity, db_entity_configuration, data=json)

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


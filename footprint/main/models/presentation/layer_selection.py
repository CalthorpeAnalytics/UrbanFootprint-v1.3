from decimal import Decimal
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry
from django.db.models.query import QuerySet
from geojson import loads
from jsonify.templatetags.jsonify import jsonify
from picklefield import PickledObjectField
from footprint.main.lib.functions import flat_map, any_true, map_to_dict, dual_map_to_dict, map_dict, map_dict_value
from footprint.main.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.main.models.geospatial.feature_class_creator import FeatureClassCreator
from footprint.main.models.presentation.medium import Medium
from footprint.main.models.presentation.layer import Layer
from footprint.main.models.database.information_schema import InformationSchema
from footprint.main.utils.dynamic_subclassing import create_tables_for_dynamic_classes, drop_tables_for_dynamic_classes, dynamic_model_class
from footprint.main.utils.query_parsing import parse_query, model_field_paths, related_field_paths
from footprint.main.utils.utils import parse_schema_and_table, clear_many_cache_on_instance_field, normalize_null, get_property_path

__author__ = 'calthorpe_associates'

DEFAULT_GEOMETRY = GEOSGeometry('MULTIPOLYGON EMPTY')

class LayerSelection(models.Model):
    """
        An abstract feature class that represents selection layers corresponding to a ConfigEntity  and user in the system.
        Each instance has a Layer reference which references FeatureClass via its db_entity_key,
        and this FeatureClass's instances are computed and stored in selected_features based on the value of geometry.
        The selected_feature property returns a query of the FeatureClass. No Feature subclass specific field exists
        in this model instead features are simply cached in a pickedobjectfield.
    """
    objects = GeoInheritanceManager()
    class Meta(object):
        app_label = 'main'
        # LayerSelection is subclassed dynamically per-Layer and are stored in the Layer's ConfigEntity's schema.
        # They are per Layer because the feature toMany must be created dynamically to be specific to the Feature subclass
        abstract = True

    # The user to whom the selection belongs
    user = models.ForeignKey(User)

    # The geometry of the selection. If accumulating selections we can just add polygons together.
    geometry = models.GeometryField(null=True, default=DEFAULT_GEOMETRY)

    aggregates = PickledObjectField(null=True)
    filter = PickledObjectField(null=True)
    joins = PickledObjectField(null=True)
    group_bys = PickledObjectField(null=True)

    # This dictionary of the raw query strings, stored so the UI can show them again
    query_strings = PickledObjectField(null=True, default=lambda: dict(aggregates_string=None, filter_string=None, group_by_string=None))

    # The selected Feature instances of the feature class/table that the layer represents.
    # This field is always written to when the bounds property is set.
    # We model this as a blob because it never needs to be queried in part. Also, it's difficult to get Django
    # to correctly create a ManyToMany dynamic field of a dynamic Feature subclass. The declaration works fine,
    # but resolving field names tends to run into problems with the name_map cache that Django uses to track field
    # relationships.
    # This field is created dynamically in the dynamic class creation below
    #features=models.ManyToManyField(feature_class, through=dynamic_through_class, related_name=table_name)

    # The ordered list of field names matching the results
    result_fields = PickledObjectField(null=True)
    # A lookup from the field name to a human readable title
    result_field_title_lookup = PickledObjectField(null=True, default=lambda: {})

    # Stores summary results, i.e. results produced by query aggregation. These are always a list of dicts
    summary_results = PickledObjectField(null=True)
    # The ordered list of field names matching the summary results
    summary_fields = PickledObjectField(null=True)
    # A lookup from the field name to a human readable title
    summary_field_title_lookup = PickledObjectField(null=True, default=lambda: {})

    # The sql used to create the results, for debugging
    query_sql = None
    # The sql used to create the summary results, for debugging
    summary_query_sql = None

    @staticmethod
    def cleanup_title(key):
        parts = key.split('__')
        if len(parts) > 2:
            return '_'.join(key.split('__')[2:])
        else:
            return '_'.join(parts)

    def update_features(self, query_set):
        """
            Updates the features property ManyToMany with the features returned by self.create_query_set, whose
            QuerySet is based upon the current values of the LayerSelection instance
            :param query_set: The query_set from create_query_set or similar
        :return:
        """
        self.clear_features()
        if not query_set:
            # If none keep features clear and return
            return
        # Update the features based on the new query_set
        for layer_selection_feature in map(
            # Create the through class instance. In the future this will hold other info about the selection,
            # Such as the current state of variou attributes to allow undo/redo, etc
            lambda feature: self.features.through(
                    feature=feature,
                    layer_selection=self
            ), query_set.all()):
            layer_selection_feature.save()

    def resolve_related_models(self):
        """
            The array of relevant related_models based on self.joins, which contains 0 or more db_entity_keys
        """
        return map(lambda join: self.config_entity.db_entity_feature_class(join), self.joins or [])

    def values_query_set(self, query_set=None):
        """
            Returns a ValuesQuerySet based on the query_set and the related_models.
            The given query_set returns Feature class instances. We want the dictionaries with the related models
            joined in
            :param query_set. Optional instance QuerySet to use as the basis for producing the ValueQuerySet.
            If omitted then create_query_set is used to generate it
        """

        feature_class = self.feature_class()
        query_set = query_set or self.create_query_set(feature_class.objects)

        # Combine the fields of the related models
        related_models = self.resolve_related_models()
        all_field_paths = model_field_paths(feature_class, fields=feature_class.limited_api_fields()) + flat_map(
            lambda related_model: related_field_paths(feature_class.objects, related_model, fields=related_model.limited_api_fields()),
            related_models)
        # Create a feature class to represent
        # Convert the queryset to values with all main and related field paths
        return query_set.values(*all_field_paths)

    def clear_features(self):
        self.features.through.objects.all().delete()

    def update_summary_results(self, query_result):
        """
            Updates the summary results with the given QuerySet or results list
        :param self:
        :param query_result:
        :return:
        """

        if isinstance(query_result, QuerySet):
            # Find aggregate and normal field names
            aggregate_names = query_result.aggregate_names if hasattr(query_result, 'aggregate_names') else []
            self.summary_fields = (query_result.field_names if hasattr(query_result, 'field_names') else []) + aggregate_names
            # Find aggregate and normal field titles
            aggregate_titles = map_dict(lambda key, value: self.cleanup_title(key), query_result.query.aggregates) if hasattr(query_result.query, 'aggregates') else []
            titles = map(lambda tup: self.cleanup_title(tup[1]), query_result.query.select) + aggregate_titles
            # Create a lookup from field name to title
            self.summary_field_title_lookup = dual_map_to_dict(lambda key, value: [key, value], self.summary_fields, titles)
        elif len(query_result) > 0:
            # For single row aggregates. TODO figure out who to extract the names from the query
            self.summary_fields = query_result[0].keys()
            self.summary_field_title_lookup = map_to_dict(lambda key: [key, key], self.summary_fields)

        self.summary_results = map(lambda result: self.process_summary_result(result), query_result)
        self.save()

    def clear_summary_results(self):
        self.summary_results = None

    @property
    def unique_id(self):
        return '%s_%s' % (self.user.id, self.layer.id)

    @staticmethod
    def process_summary_result(result):
        return map_dict_value(
            lambda value: round(value, 2) if value and isinstance(value, (float, Decimal)) else value,
            result)

    @property
    def bounds(self):
        """
            Always the same as the geometry field for read-access
        :return:
        """
        return loads(self.geometry.json)

    @bounds.setter
    def bounds(self, value):
        """
            Convert the bounds from JSON to the GEOSGeometry format
            bounds is a python getter/setter that sets the geometry field
        :param value: geojson python object
        :return:
        """
        # TODO need for geometry
        if value and len(value.keys()) > 0:
            try:
                self.geometry = GEOSGeometry(jsonify(value))
            except:
                # TODO log warning
                self.geometry = GEOSGeometry('MULTIPOLYGON EMPTY')
        else:
            self.geometry = GEOSGeometry('MULTIPOLYGON EMPTY')

    @property
    def selected_features(self):
        """
            Returns all Feature instances in self.features
        :return:
        """

        try:
            return self.features.all()
        except:
            # Fix a terrible Django manyToMany cache initialization bug by clearing the model caches
            clear_many_cache_on_instance_field(self.features)
            return self.features.all()

    @property
    def selected_features_or_values(self):
        """
            Returns either the instance-based query_set--selected_features or the values-based on--values_query_set.
            The latter is returned if self.joins has items, meaning joins are required and we can't return the instances
        """
        return self.values_query_set() if self.joins and len(self.joins) > 0 else self.selected_features

    def create_join_feature_class(self):
        """
            Make an unmanage Django model based on the joined fields
        """
        return FeatureClassCreator(self.config_entity, self.layer.db_entity_interest.db_entity).dynamic_join_model_class(self.resolve_related_models())

    @property
    def selection_extent(self):
        """
            The bounds of the current selection or the whole thing if no selection
        """
        return self.selected_features.extent_polygon() if len(self.selected_features) > 0 else self.feature_class().objects.extent_polygon()

    def clear(self):
        """
            Clears the geometry and the selected features
        :return:
        """
        self.geometry = None
        self._clear_features()

    def _clear_features(self):
        """
            Clears the features instances
        :greturn:
        """

        self.features.delete()

    def feature_class(self):
        """
            The feature class corresponding to the instance's layer
        :return:
        """
        config_entity = self.__class__.config_entity
        return config_entity.db_entity_feature_class(self.layer.db_entity_key)

    def create_query_set(self, query_set):
        # Filter by bounds if present
        bounded_query_set = self.feature_class().objects.filter(wkb_geometry__intersects=self.geometry) \
            if self.geometry != DEFAULT_GEOMETRY else query_set
        # Filter by filter if present
        if self.filter:
            # If filters have been specified then perform the query.
            return parse_query(self.config_entity, bounded_query_set, filters=self.filter, joins=self.joins)
        elif self.geometry != DEFAULT_GEOMETRY:
            # Return the result unless neither bounded or filtered.
            # Specifying nothing results in an empty query set (i.e. there is no select all)
            return parse_query(self.config_entity, bounded_query_set, joins=self.joins)
        elif self.joins:
            return parse_query(self.config_entity, bounded_query_set, joins=self.joins)
        else:
            query_set.none()

    def create_summary_query_set(self, query_set, previous_attributes={}):
        if not self.aggregates and not self.group_bys:
            return None

        # Filter by bounds if present
        bounded_query_set = self.feature_class().objects.filter(wkb_geometry__intersects=self.geometry) \
            if self.geometry != DEFAULT_GEOMETRY else query_set

        # If filters have been specified then perform the query.
        return parse_query(self.config_entity, bounded_query_set, filters=self.filter, joins=self.joins,
                           group_bys=self.group_bys, aggregates=self.aggregates)

    def properties_have_changed(self, property_dict, *properties):
        return any_true(lambda property:
                            normalize_null(get_property_path(self, property)) !=
                            normalize_null(get_property_path(property_dict, property)),
                        properties)

    @classmethod
    def post_save(self, user_id, objects, **kwargs):
        """
            This is called after a resource saves a layer_selection. We have no use for it at the moment
        """
        pass


class LayerSelectionFeature(models.Model):
    objects = GeoInheritanceManager()

    # A class name is used to avoid circular dependency
    #layer_selection = models.ForeignKey(LayerSelection, null=False)
    #feature = models.ForeignKey(Feature, null=False)
    #layer_selection = None
    #feature = None
    medium = models.ForeignKey(Medium, null=True, default=None)

    def __unicode__(self):
        return "LayerSelection:{0}, Feature:{1}, Medium:{2}".format(self.layer_selection, self.feature, self.medium)
    class Meta(object):
        app_label = 'main'
        abstract = True

def get_or_create_dynamic_layer_selection_class_and_table(layer, no_table_creation=False):
    """
        Generate a subclass of LayerSelection specific to the layer and use it to create a table
    :param layer
    :param no_table_creation for debugging, don't create the underlying table
    :return:
    """

    config_entity = layer.presentation.subclassed_config_entity
    dynamic_class_name = 'LayerSelection{0}'.format(layer.id)
    try:
        feature_class = config_entity.db_entity_feature_class(layer.db_entity_key)
    except Exception:
        # For non feature db_entities, like google maps
        return None

    dynamic_through_class = dynamic_model_class(
        LayerSelectionFeature,
        layer.presentation.subclassed_config_entity.schema(),
        'lsf%s' % layer.id,
        class_name='{0}{1}'.format(dynamic_class_name, 'Feature'),
        fields=dict(
            layer_selection=models.ForeignKey(dynamic_class_name, null=False),
            feature=models.ForeignKey(feature_class, null=False),
        )
    )

    # Table is layer specific. Use ls instead of layerselection to avoid growing the schema.table over 64 characters, sigh
    table_name = 'ls%s' % layer.id
    dynamic_class = dynamic_model_class(
        LayerSelection,
        # Schema is that of the config_entity
        layer.presentation.subclassed_config_entity.schema(),
        table_name,
        class_name=dynamic_class_name,
        # The config_entity instance is a class attribute
        class_attrs=dict(
            config_entity__id=config_entity.id,
            layer__id=layer.id,
            override_db=config_entity.db
        ),
        related_class_lookup=dict(
            config_entity='footprint.main.models.config.config_entity.ConfigEntity',
            layer='footprint.main.models.presentation.layer.Layer'),
        fields=dict(
            features=models.ManyToManyField(feature_class, through=dynamic_through_class, related_name=table_name)
        )
    )

    # Make sure the tables exist
    if not no_table_creation:
        create_tables_for_dynamic_classes(dynamic_class, dynamic_through_class)

    return dynamic_class

def drop_layer_selection_table(layer_selection_class):
    """
        Drop the dynamic LayerSelection class table. This should be called whenever the owning layer is deleted
    :param layer_selection_class:
    :return:
    """
    if InformationSchema.objects.table_exists(*parse_schema_and_table(layer_selection_class._meta.db_table)):
        drop_tables_for_dynamic_classes(layer_selection_class)

def layer_selections_of_config_entity(config_entity):
    """
        Returns all LayerSelection instances of the ConfigEntity
    :param config_entity:
    :return:
    """
    return flat_map(
        lambda layer: list(get_or_create_dynamic_layer_selection_class_and_table(layer, no_table_creation=True)),
        Layer.objects.filters(config_entity=config_entity))



from itertools import chain
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry
from picklefield import PickledObjectField
from footprint.lib.functions import flat_map
from footprint.managers.geo_inheritance_manager import GeoInheritanceManager
from footprint.models import Layer, Medium
from footprint.models.base.base_feature import TemplateBaseFeature
from footprint.models.geospatial.feature import Feature
from footprint.utils.query_parsing import parse_query
from footprint.models.database.information_schema import InformationSchema
from footprint.utils.dynamic_subclassing import get_dynamic_model_class, create_table_for_dynamic_class, drop_table_for_dynamic_class
from footprint.utils.utils import parse_schema_and_table

__author__ = 'calthorpe'

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

    # The user to whom the selection belongs
    user = models.ForeignKey(User)

    # The layer which this LayerSelection represents
    #layer = models.ForeignKey(Layer)

    # The geometry of the selection. If accumulating selections we can just add polygons together.
    geometry = models.GeometryField(null=True, default=DEFAULT_GEOMETRY)

    aggregates = PickledObjectField(null=True)
    query = PickledObjectField(null=True)
    joins = PickledObjectField(null=True)
    groupBy = PickledObjectField(null=True)

    # The selected Feature instances of the feature class/table that the layer represents.
    # This field is always written to when the bounds property is set.
    # We model this as a blob because it never needs to be queried in part. Also, it's difficult to get Django
    # to correctly create a ManyToMany dynamic field of a dynamic Feature subclass. The declaration works fine,
    # but resolving field names tends to run into problems with the name_map cache that Django uses to track field
    # relationships. More importantly. Now that we use a LayerSelection class for all the feature tables of a
    # single config_entity, we can't even dynamically specify the Feature class.
    #features = PickledObjectField(default=lambda: [])

    def update_features(self, query_result):
        self.features.through.objects.all().delete()
        for layer_selection_feature in map(
                lambda feature: self.features.through(
                        feature=feature,
                        layer_selection=self
                ), query_result):
            layer_selection_feature.save()

    @property
    def bounds(self):
        """
            Always the same as the geometry field for read-access
        :return:
        """
        return self.geometry

    @bounds.setter
    def bounds(self, value):
        """
            Bounds are the incoming geometry selected by the user. They might add to or replace the geometry
            Whenever the bounds are set we set the geometry and calculate the intersecting features to set features
        :param value:
        :return:
        """
        self.geometry = value
        self.save()
        if self.geometry or not self.query:
            self.update_features(self.feature_class().objects.filter(geography__geometry__intersects=self.geometry or DEFAULT_GEOMETRY))

    @property
    def _query(self):
        pass

    @_query.setter
    def _query(self, value):
        """
            Parses the query attribute, an embedded python dictionary, into a Django Query selection
        :return:
        """
        feature_class = self.feature_class()
        self.query = value
        if self.query:
            self.update_features(parse_query(feature_class.objects, self.query, joins=self.joins))

    @property
    def selected_features(self):
        """
            A parsed query from a tokenized python dict.
        :return:
        """

        try:
            return self.features.all()
        except:
            # Tries to fix a terrible Django manyToMany cache initialization bug by clearing the model caches
            meta = super(self.features.__class__, self.features).get_query_set().model._meta
            for cache_attr in ['_related_many_to_many_cache', '_m2m_cache', '_name_map']:
                if hasattr(meta, cache_attr):
                    delattr(meta, cache_attr)
            meta.init_name_map()
            return self.features.all()



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
        :return:
        """

        self.features = []
        self.save()

    def feature_class(self):
        """
            The feature class corresponding to the instance's layer
        :return:
        """
        config_entity = self.__class__.config_entity
        return config_entity.feature_class_of_db_entity(self.layer.db_entity_key)

    class Meta(object):
        app_label = 'footprint'
        abstract = True

class LayerSelectionFeature(models.Model):
    objects = GeoInheritanceManager()

    # A class name is used to avoid circular dependency
    #layer_selection = models.ForeignKey(LayerSelection, null=False)
    #feature = models.ForeignKey(Feature, null=False)
    layer_selection = None
    feature = None
    medium = models.ForeignKey(Medium, null=True, default=None)

    def __unicode__(self):
        return "LayerSelection:{0}, Feature:{1}, Medium:{2}".format(self.layer_selection, self.feature, self.medium)
    class Meta(object):
        app_label = 'footprint'
        abstract = True

def create_dynamic_layer_selection_class_and_table(layer, no_table_creation=False):
    """
        Generate a subclass of LayerSelection specific to the layer and use it to create a table
    :param layer
    :param no_table_creation for debugging, don't create the underlying table
    :return:
    """

    config_entity = layer.presentation.subclassed_config_entity
    dynamic_class_name = 'LayerSelection{0}'.format(layer.id)
    try:
        feature_class = config_entity.feature_class_of_db_entity(layer.db_entity_key)
    except Exception:
        # If no feature_class exists for the db_entity, create a generic feature class
        # that never matches anything
        # TODO. Using TemplateBaseFeature for convenience
        feature_class = TemplateBaseFeature

    dynamic_association_class = get_dynamic_model_class(
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
    dynamic_class = get_dynamic_model_class(
        LayerSelection,
        # Schema is that of the config_entity
        layer.presentation.subclassed_config_entity.schema(),
        table_name,
        class_name=dynamic_class_name,
        # The config_entity instance is a class attribute
        class_attrs=dict(
            config_entity=config_entity,
            layer=layer,
            override_db=config_entity.db
        ),
        fields=dict(
            features=models.ManyToManyField(feature_class, through=dynamic_association_class, related_name=table_name)
        )
    )

    # Make sure the tables exist
    if not no_table_creation:
        create_table_for_layer_selection_class(dynamic_class)
        create_table_for_layer_selection_class(dynamic_association_class)

    return dynamic_class

def create_table_for_layer_selection_class(layer_selection_class):
    """
        Create the main table for the given layer_selection_class if it don't exist
    :param layer_selection_class:
    :return:
    """
    if not InformationSchema.objects.table_exists(*parse_schema_and_table(layer_selection_class._meta.db_table)):
        create_table_for_dynamic_class(layer_selection_class)

def drop_layer_selection_table(layer_selection_class):
    """
        Drop the dynamic LayerSelection class table. This should be called whenever the owning layer is deleted
    :param layer_selection_class:
    :return:
    """
    if InformationSchema.objects.table_exists(*parse_schema_and_table(layer_selection_class._meta.db_table)):
        drop_table_for_dynamic_class(layer_selection_class)

def layer_selections_of_config_entity(config_entity):
    """
        Returns all LayerSelection instances of the ConfigEntity
    :param config_entity:
    :return:
    """
    return flat_map(
        lambda layer: list(create_dynamic_layer_selection_class_and_table(layer, no_table_creation=True)),
        Layer.objects.filters(config_entity=config_entity))


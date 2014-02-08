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
import os
import shutil

from footprint.initialization.fixture import LayerConfigurationFixture
from footprint.initialization.publishing.layer_initialization import LayerMediumKey, LayerTag
from footprint.initialization.utils import resolve_fixture
from footprint.models import LayerLibrary, Scenario
from footprint.models.presentation.layer_selection import create_dynamic_layer_selection_class_and_table
from footprint.models.presentation.tilestache_config import TileStacheConfig
from footprint.models.presentation.layer import Layer
from footprint.models.keys.keys import Keys
from footprint.models.presentation.medium import Medium
from footprint.models.presentation.template import Template
from footprint.models.tag import Tag

__author__ = 'calthorpe'


def on_config_entity_post_save_layer(sender, **kwargs):
    """
        Sync tilestache to a ConfigEntity class after the latter is saved
    """
    config_entity = kwargs['instance']

    # Only create layers for Scenarios
    if not isinstance(config_entity, Scenario):
        return

    #    Create LayerLibrary instances based on each LayerLibrary configuration if the configuration's scope
    #    matches that of self.config_entity
    client_layer_configuration = resolve_fixture(
        "publishing",
        "layer",
        LayerConfigurationFixture,
        config_entity.schema(),
        config_entity=config_entity)

    layer_libraries = map(
        lambda layer_library_configuration: _update_or_create_layer_library(config_entity, layer_library_configuration),
        client_layer_configuration.matching_scope(client_layer_configuration.layer_libraries(),
                                                  class_scope=config_entity.__class__))

    # For all unique layers (they might be shared by libraries) configure layer_selection tables
    layers = Layer.objects.filter(presentation__in=layer_libraries)
    # Create a layer_selection class for the layer if it is selectable
    for layer in layers:
        create_dynamic_layer_selection_class_and_table(layer)

def _update_or_create_layer_library(config_entity, layer_library_configuration):
    layer_library = LayerLibrary.objects.update_or_create(
        key=layer_library_configuration.key,
        scope=config_entity.schema(),
        config_entity=config_entity,
        defaults=dict(
            configuration=layer_library_configuration,
            name=layer_library_configuration.name.format(config_entity.name),
            description=layer_library_configuration.description.format(config_entity.name)
        )
    )[0]

    # Uncomment to delete layers
    #for layer in Layer.objects.filter(presentation=layer_library):
    #    layer.delete()
    #   create_dynamic_layer_selection_class_and_table(layer, False).objects.all().delete()

    # Create all of the Layer instances. These reference the layer_library instance
    map(lambda layer_configuration: _layer_from_db_entity(config_entity, layer_library, layer_configuration),
        layer_library_configuration.data.presentation_media_configurations)

    # Update or create the Layers of the LayerLibrary
    return layer_library


def _layer_from_db_entity(config_entity, layer_library, layer_configuration):
    """
        Create a Layer for each DbEntity in the LayerConfiguration. These instances constitute the default
        library of the config_entity, which is a library of all DbEntities. The media of these instances can be set
        to style media.
    :param layer_configuration:
    :return:
    """

    # Resolve the active DbEntity of the ConfigEntity based on the key of the LayerConfiguration
    db_entity_key = layer_configuration.db_entity_key
    # In case multiple DbEntities with the same key exist, get the active one
    try:
        db_entity = config_entity.get_selected_db_entity(db_entity_key)
    except Exception, e:
        raise Exception(
            "db_entity_key {0} does not exist for config_entity {1}. Did you configure the LayerConfiguration for the wrong scope? Original exception: {2}".format(
                db_entity_key, config_entity, e.message))

    # Get the Template instance for the db_entity_key
    # The key is based on the base class of the db_entity_key if one exists
    # If no matching template is found use the default Medium
    try:
        template_id_key = LayerMediumKey.Fab.ricate(config_entity.base_class_of_db_entity(db_entity_key).__name__)
        template = Medium.objects.get_subclass(
            key=template_id_key
        )
    except Exception:
        template = Medium.objects.get(
            key=LayerMediumKey.DEFAULT
        )

    # Extract the context from the template if there is one.
    # This serves as the default medium_context of the Layer, which can later be customized (e.g. a user can specify
    # specific colors and other stylistic data)
    template_context = template.template_context if isinstance(template, Template) else None

    try:
        rendered_medium = template.render_attributed_content(template_context, content_key='css')
    except KeyError:
        raise Exception(
            "For db_entity_key %s could not find one or more of Template content attributes of set: %s in medium_context with attribute(s): %s" %
            (db_entity_key, ', '.join(template.content['attributes']), ', '.join(template_context['attributes'])))

    layer = Layer.objects.update_or_create(
        presentation=layer_library,
        db_entity_key=db_entity_key,
        defaults=dict(medium=template,
                      name='style__{0}__{1}__{2}'.format(layer_library.config_entity.id, layer_library.id, db_entity_key),
                      configuration=dict(
                          built_form_set_key=layer_configuration.built_form_set_key,
                          sort_priority=layer_configuration.sort_priority if layer_configuration.sort_priority > 0 else 100,
                          attribute_sort_priority=layer_configuration.attribute_sort_priority,
                      ),
                      visible_attributes=layer_configuration.visible_attributes,

                      # A copy of the template context. This default context can be updated by the user to customize
                      # the layer styling
                      medium_context=template_context,
                      # A rendered version of the template_context
                      rendered_medium=rendered_medium,
                      visible=layer_configuration.visible)
    )[0]

    layer.tags.clear()
    # Tag the layer with the configured tags or the default
    layer.tags.add(*(layer_configuration.tags or
                    [Tag.objects.update_or_create(tag=layer.presentation.config_entity.db_entity_owner(layer.db_entity_interest.db_entity).key)[0]]))
                    #[Tag.objects.get(tag=LayerTag.DEFAULT)])

# Customize the medium_context to have a class that refers specifically to this layer
    # TODO document why this is needed
    if template_context:
        layer.medium_context['htmlClass'] = 'layer_{0}'.format(layer.id)
        layer.save()
    return layer




def on_post_analytic_run(sender, **kwargs):
    """
        Responds to analytic module runs
        kwargs: module is the string name of the module (TODO covert to instance)
            config_entity is the config_entity that ran
    :return:
    """
    module = kwargs['module']
    config_entity = kwargs['config_entity']
    if module == 'core':
        CORE_DEPENDENT_DB_ENTITY_KEYS = [Keys.DB_ABSTRACT_FUTURE_SCENARIO_FEATURE, Keys.DB_ABSTRACT_END_STATE_FEATURE,
                                         Keys.DB_ABSTRACT_INCREMENT_FEATURE]
        layer_libraries = LayerLibrary.objects.filter(config_entity=config_entity)
        layers = Layer.objects.filter(presentation__in=layer_libraries, db_entity_key__in=CORE_DEPENDENT_DB_ENTITY_KEYS)
        # Invalidate these layers
        for layer in layers:
            invalidate_cache(layer, TileStacheConfig.objects.get().config)

def on_layer_selection_post_save_layer(sender, layer=None, user=None):
    """
        Invalidate the layer selection cache
    :param sender:
    :param layer
    :param user
    :return:
    """
    invalidate_cache(layer, TileStacheConfig.objects.get().config, user, ['selection'])

def invalidate_cache(layer, config, user=None, layer_types=None):
    """
    Invalidates the entire cache folder for the layer
    :return:
    """
    tilestache_cache_path = getattr(config.cache, 'cachepath', None)
    if not tilestache_cache_path:
        return

    visible_attr = layer.visible_attributes[0] or None

    tilestache_layer_name = 'layer_{id}{visible_attribute}'.format(
        id=layer.id,
        visible_attribute='_{0}'.format(visible_attr) if visible_attr else ''
    )

    for layer_type in layer_types or ['raster', 'vector', 'selection']:
        if layer_type == 'selection' and not user:
            continue
        layer_cache = os.path.join(tilestache_cache_path, tilestache_layer_name + "{user_id}_{layer_type}".format(
            user_id='_{0}'.format(user.id) if user else '',
            layer_type=layer_type
        ))
        if os.path.exists(layer_cache):
            shutil.rmtree('{cache}'.format(cache=layer_cache))

def on_db_entity_save():
    """
    respond to whenever a db entity is added or updated
    :return:
    """


def on_layer_style_save():
    """
    respond to any changes in style (
    :return:
    """


def on_config_entity_pre_delete_layer(sender, **kwargs):
    """
    """
    config_entity = kwargs['instance']
    LayerLibrary.objects.filter(
        key=Keys.LAYER_LIBRARY_DEFAULT,
        scope=config_entity.key).delete()


def on_scenario_feature_save(sender, **kwargs):
    """
    this method will call the layer invalidation after a scenario has been edited
    :param sender:
    :param kwargs:
    :return:
    """
    scenario = kwargs['instance']
    changed_layers = scenario.layers.filter(db_entity_key__in=1)
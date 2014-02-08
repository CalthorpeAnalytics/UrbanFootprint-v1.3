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
#from memory_profiler import profile
import copy

import logging
from django.contrib.auth.models import User

from footprint.client.configuration.fixture import LayerConfigurationFixture, ConfigEntityFixture
from footprint.main.lib.functions import map_to_dict, merge
from footprint.main.models import PresentationConfiguration
from footprint.main.models.presentation.presentation_configuration import LayerConfiguration
from footprint.main.publishing.layer_initialization import LayerMediumKey
from footprint.client.configuration.utils import resolve_fixture
from footprint.main.models.presentation.layer_library import LayerLibrary
from footprint.main.models.config.config_entity import ConfigEntity
from footprint.main.models.config.scenario import Scenario
from footprint.main.models.presentation.layer_selection import get_or_create_dynamic_layer_selection_class_and_table
from footprint.main.models.presentation.layer import Layer
from footprint.main.models.keys.keys import Keys
from footprint.main.models.presentation.medium import Medium
from footprint.main.models.presentation.template import Template
from footprint.main.models.tag import Tag

__author__ = 'calthorpe_associates'
logger = logging.getLogger(__name__)

#@profile
def on_config_entity_post_save_layer(sender, **kwargs):
    """
        Sync tilestache to a ConfigEntity class after the latter is saved
        :param **kwargs: optional "db_entity_keys" to limit the layers created to those DbEntities
    """
    config_entity = kwargs['instance']
    logger.debug("\t\tHandler: on_config_entity_post_save_layer. ConfigEntity: %s" % config_entity.name)
    if ConfigEntity._heapy:
        ConfigEntity.dump_heapy()

    # Only create layers for Scenarios
    if not isinstance(config_entity, Scenario):
        return

    #    Create LayerLibrary instances based on each LayerLibrary configuration if the configuration's scope
    #    matches that of config_entity
    client_layer_configuration = resolve_fixture(
        "publishing",
        "layer",
        LayerConfigurationFixture,
        config_entity.schema(),
        config_entity=config_entity)

    map(
        lambda layer_library_configuration: _update_or_create_layer_library(
            config_entity, layer_library_configuration, **kwargs),
        client_layer_configuration.matching_scope(client_layer_configuration.layer_libraries(),
                                                  class_scope=config_entity.__class__))

#@profile
def on_db_entity_post_save_layers(sender, **kwargs):
    """
        Update/Create layers for the give DbEntityInterest.
        This is just like on_config_entity_post_save_layers except that we only create the layer
        for this db_entity
    """

    db_entity_interest = kwargs['instance']
    config_entity = db_entity_interest.config_entity.subclassed_config_entity
    db_entity = db_entity_interest.db_entity
    logger.debug("\t\tHandler: on_db_entity_post_save_layers. DbEntity: %s" % db_entity.full_name)
    if ConfigEntity._heapy:
        ConfigEntity.dump_heapy()

    # Only create layers for Scenarios
    if not isinstance(config_entity, Scenario):
        return

    #    Create LayerLibrary instances based on each LayerLibrary configuration if the configuration's scope
    #    matches that of config_entity
    client_layer_configuration = resolve_fixture(
        "publishing",
        "layer",
        LayerConfigurationFixture,
        config_entity.schema(),
        config_entity=config_entity)

    map(
        lambda layer_library_configuration: _update_or_create_layer_library(
            config_entity, layer_library_configuration, db_entity_keys=[db_entity.key]),
        client_layer_configuration.matching_scope(client_layer_configuration.layer_libraries(),
                                                  class_scope=config_entity.__class__))

def _update_or_create_layer_library(config_entity, layer_library_configuration, **kwargs):
    """
        Update or create the LayerLibrary for the given config_entity and configuration.
        Also create update or craet all layers of that library unless limited by kwargs['db_entity_keys']
        :param kwargs: 'db_entity_keys': Optional list to limit layer update/create to those DbEntities
    """
    db_entity_keys = kwargs.get('db_entity_keys', None)

    logger.debug("\t\t\tUpdate/Create LayerLibrary %s" % layer_library_configuration.key)
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

    db_entity_key_to_configuration = map_to_dict(lambda configuration: [configuration.db_entity_key, configuration],
                                                 layer_library_configuration.data.presentation_media_configurations)
    if db_entity_keys:
        # Configure all given db_entity_keys, whether or not a matching configuration exists.
        # This allows us to handle uploaded layers
        map(lambda db_entity_key: update_or_create_layer(layer_library,
                                                         db_entity_key_to_configuration.get(db_entity_key),
                                                         db_entity_key=db_entity_key),
            filter(lambda db_entity_key: config_entity.computed_db_entities(key=db_entity_key).count() == 1,
                   db_entity_keys))
    else:
        if not config_entity.origin_config_entity:
            # Update or create the Layers of the layer_library_configuration
            layers = map(
                lambda layer_configuration: update_or_create_layer(layer_library, layer_configuration),
                layer_library_configuration.data.presentation_media_configurations)
        else:
            # If this is a cloned config_entity, clone or update clones
            layers = map(
                lambda origin_layer: clone_or_update_cloned_layer(layer_library, origin_layer),
                Layer.objects.filter(presentation__config_entity=config_entity.origin_config_entity))

    return layer_library

def layer_configuration_from_layer(layer, **kwargs):
    """
        Reverses the work of update_or_create_layer for cloning.
        :param kwargs: overrides
    """
    return LayerConfiguration(
        **merge(
            dict(
                db_entity_key=layer.db_entity_key,
                layer_library_key=layer.presentation.key,
                visible=layer.visible,
                visible_attributes=layer.visible_attributes,
                built_form_set_key=layer.configuration.get('built_form_key', None),
                sort_priority=layer.configuration.get('sort_priority', None),
                attribute_sort_priority=layer.configuration.get('attribute_sort_priority', None),
                column_alias_lookup=layer.configuration.get('column_alias_lookup', None),
                tags=layer.tags.all()
            ),
            kwargs)
    )

def clone_or_update_cloned_layer(layer_library, origin_layer):
    """
        Clones the given layer into the target_config_entity if it doesn't already exist there
    """

    layer_configuration =layer_configuration_from_layer(
        origin_layer,
        # Override this in case the layer is being cloned to a library with a different key
        layer_library_key=layer_library.key
    )
    update_or_create_layer(layer_library, layer_configuration)

def update_or_create_layer(layer_library, layer_configuration=None, db_entity_key=None):
    """
        Create a Layer for each DbEntity in the LayerConfiguration. These instances constitute the default
        library of the config_entity, which is a library of all DbEntities. The media of these instances can be set
        to style media.
    :param layer_configuration: Optional. A full configuration
    :param db_entity_key. Optional. Use instead of full configuration to generate defaults
    :return:
    """

    if not layer_configuration:
        # See if the layer and its configuration exists
        layers = Layer.objects.filter(presentation=layer_library, db_entity_key=db_entity_key)
        if len(layers) == 1 and layers[0].configuration:
            # Restore configuration
            logger.debug("\t\t Imported Layer for %s already exists. Updating" % db_entity_key)
            layer_configuration = layer_configuration_from_layer(layers[0])
        else:
            # Create the configuration
            logger.debug("\t\t Importer Layer for %s does not exist. Creating" % db_entity_key)
            layer_configuration = create_layer_configuration_for_import(layer_library.subclassed_config_entity, db_entity_key)

    # Resolve the active DbEntity of the ConfigEntity based on the key of the LayerConfiguration
    db_entity_key = layer_configuration.db_entity_key
    logger.debug("\t\t\tLayer Publishing DbEntity Key: %s" % db_entity_key)

    # In case multiple DbEntities with the same key exist, get the active one
    try:
        db_entity = layer_library.subclassed_config_entity.computed_db_entities().get(key=db_entity_key)
    except Exception, e:
        raise Exception(
            "db_entity_key {0} does not exist for config_entity {1}. Did you configure the LayerConfiguration for the wrong scope? Original exception: {2}".format(
                db_entity_key, layer_library.subclassed_config_entity, e.message))

    # Get the Template instance for the db_entity_key
    # The key is based on the base class of the db_entity_key if one exists
    # If no matching template is found use the default Medium
    try:
        template_id_key = LayerMediumKey.Fab.ricate(layer_library.subclassed_config_entity.abstract_class_of_db_entity(db_entity_key).__name__)
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
                      # The name by default matches the DbEntity
                      name=db_entity.name,
                      configuration=dict(
                          built_form_set_key=layer_configuration.built_form_set_key,
                          sort_priority=layer_configuration.sort_priority if layer_configuration.sort_priority > 0 else 100,
                          attribute_sort_priority=layer_configuration.attribute_sort_priority,
                          column_alias_lookup=layer_configuration.column_alias_lookup,
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

    # Customize the medium_context to have a class that refers specifically to this layer
    # TODO document why this is needed [it is not]
    if template_context:
        layer.medium_context['htmlClass'] = 'layer_{0}'.format(layer.id)
        layer.save()

    # Update or create the LayerSelection tables and instances for this layer
    update_or_create_layer_selections_for_layer(layer)

    return layer

def on_db_entity_save():
    """
    respond to whenever a db entity is added or updated
    :return:
    """


def on_layer_style_save():
    """
    respond to any changes in style
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


def update_or_create_layer_selections(layer_libraries=None, config_entity=None):
    # For all unique layers (they might be shared by libraries) configure layer_selection tables
    layer_libraries_of_config_entity = layer_libraries if layer_libraries else LayerLibrary.objects.filter(config_entity=config_entity)
    layers = Layer.objects.filter(presentation__in=layer_libraries_of_config_entity)
    # Create a layer_selection class for the layer if it is selectable
    for layer in layers:
        update_or_create_layer_selections_for_layer(layer)

def update_or_create_layer_selections_for_layer(layer):
    """
        Create LayerSelections for all users for this layer.
    """
    layer_selection_class = get_or_create_dynamic_layer_selection_class_and_table(layer)
    if layer_selection_class:
        logger.debug("\t\t\tCreating LayerSelection for Layer of DbEntity Key: %s" % layer.db_entity_key)
        for user in User.objects.all():
            # Create an instance for each user in the system
            logger.debug("\t\t\t\t Inserting LayerSelection instance for user: %s" % user.username)
            layer_selection_class.objects.update_or_create(user=user)


def create_layer_configuration_for_import(config_entity, db_entity_key):
    """
        Creates a LayerConfiguration for imported layers using the template
        LayerConfigurations designed in the LayerConfigurationFixture.import_layer_configurations
    """

    client_layer_configuration = resolve_fixture(
        "publishing",
        "layer",
        LayerConfigurationFixture,
        config_entity.schema(),
        config_entity=config_entity)

    layer_configuration = copy.copy(client_layer_configuration.import_layer_configurations()[0])
    # Update the template LayerConfiguration to our db_entity_key
    layer_configuration.db_entity_key = db_entity_key
    return layer_configuration

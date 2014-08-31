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
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import Signal
from footprint import settings
from footprint.main.lib.functions import map_to_dict, merge, remove_keys
from footprint.main.models.geospatial.db_entity_keys import DbEntityKey
from footprint.main.models.model_utils import model_dict
from footprint.main.models.presentation.presentation_configuration import LayerConfiguration
from footprint.main.publishing import tilestache_publishing
from footprint.main.publishing.layer_initialization import LayerMediumKey
from footprint.main.models.presentation.layer_library import LayerLibrary
from footprint.main.models.config.scenario import Scenario, FutureScenario, BaseScenario
from footprint.main.models.presentation.layer_selection import get_or_create_dynamic_layer_selection_class_and_table
from footprint.main.models.presentation.layer import Layer
from footprint.main.models.keys.keys import Keys
from footprint.main.models.presentation.medium import Medium
from footprint.main.models.presentation.template import Template
from footprint.main.models.tag import Tag
from footprint.main.publishing.publishing import post_save_publishing
from footprint.main.utils.subclasses import receiver_subclasses
from footprint.main.utils.utils import resolvable_module_attr_path

__author__ = 'calthorpe_associates'
logger = logging.getLogger(__name__)

# All initial signals. They can run without dependencies
# All signals that can run after layers
post_save_layer_initial = Signal(providing_args=[])

def dependent_signal_paths(signal_path):
    """
        Gives the hierarchy of publisher signal calling order based on the given signal
        Signals are given as strings instead of paths for serialization ease
        param: signal_path. The signal path for which the dependent signals are returned
        return: An array of signal_paths or an empty array
    """
    return []

# Very wild guess about layer saving proportional times to send to the client
# These represent the parsed signal names sent to the client after the dependencies of
# the signal finish running
signal_proportion_lookup = dict(
    # initial signal after save
    post_save_layer_initial=1
)

def on_layer_post_save_process_layer(sender, **kwargs):
    """
        For layer create/update/clone, this updates the saved layer
    """
    from footprint.client.configuration.fixture import LayerConfigurationFixture
    from footprint.client.configuration.utils import resolve_fixture
    layer = kwargs['instance']
    if layer._no_post_save_publishing:
        return
    logger.debug("\t\tHandler: Layer Publishing. on_layer_post_save_process_layer %s" % layer.full_name)
    db_entity_interest = layer.db_entity_interest
    db_entity = db_entity_interest.db_entity
    config_entity = db_entity_interest.config_entity.subclassed_config_entity
    # Only create layers for Scenarios
    if not isinstance(config_entity, Scenario):
        return
    client_layer_configuration = resolve_fixture(
        "publishing",
        "layer",
        LayerConfigurationFixture,
        config_entity.schema(),
        config_entity=config_entity)

    # Update the layer via the layer library update_or_create
    map(
        lambda layer_library_configuration: _update_or_create_layer_library_and_layers(
            config_entity, layer_library_configuration, db_entity_keys=[db_entity.key]),
        client_layer_configuration.matching_scope(client_layer_configuration.layer_libraries(),
                                                  class_scope=config_entity.__class__))

def post_save_layer_initial_publishers(cls):
    """
        Run layer processing and then tilestache
    """
    post_save_layer_initial.connect(on_layer_post_save_process_layer, cls, True, "process_on_layer_post_save")
    post_save_layer_initial.connect(tilestache_publishing.on_layer_post_save_tilestache, cls, True, "tilestache_on_layer_post_save")

# Register receivers for just Scenarios, since they are the only ones that have layers
# This is the config_entity of the layer's DbEntityInterest
for cls in [FutureScenario, BaseScenario]:
    post_save_layer_initial_publishers(cls)

def _update_or_create_child_layers(config_entity, db_entity_key):
    if not isinstance(config_entity, Scenario):
        # If our DbEntityInterest.config_entity is not a Scenario, we need to do a bit of trickery
        # to find the Scenario that created the layer. Then we need to clone the layer to the other Scenarios
        some_layers = Layer.objects.filter(
            presentation__config_entity__in=config_entity.children(),
            db_entity_key=db_entity_key)
        if len(some_layers) == 0:
            # We have a problem. The layer should exist for at least one scenario
            raise Exception("Layer expected to exist for db_entity %s, but does not" % db_entity_key)
        template_layer = some_layers[0]
        # Create layers that don't exist
        Layer._no_post_save_publishing = True
        logger.info("Updating layer of db_entity_key %s, config_entity %s" % (db_entity_key, config_entity.name))
        layers = map(lambda scenario: Layer.objects.update_or_create(
                presentation__config_entity=scenario,
                db_entity_key=db_entity_key,
                defaults=merge(
                    remove_keys(model_dict(template_layer), ['db_entity_key', 'presentation']),
                    dict(presentation=LayerLibrary.objects.get(config_entity=scenario))
                )
            )[0],
            config_entity.children())
        Layer._no_post_save_publishing = False
    else:
        layers = Layer.objects.filter(
            presentation__config_entity=config_entity,
            db_entity_key=db_entity_key)
        if len(layers) != 1:
            # We have a problem. The layer should exist
            raise Exception("Layer expected to exist for db_entity %s, but does not" % db_entity_key)
    return layers

def on_db_entity_post_save_layer(sender, **kwargs):
    # Only run this if the layer has already been created
    # Otherwise when the layer is created it will kick off publishing
    # Normally the layer will exist because it saves immediately after the DbEntity
    # and before we get to this stage in post save publishing. The exception is testing with celery off
    db_entity_interest = kwargs['instance']
    config_entity = db_entity_interest.config_entity.subclassed_config_entity
    if settings.CELERY_ALWAYS_EAGER:
        return

    # Post the layer or multiple layers if the config_entity is a Project
    for layer in _update_or_create_child_layers(config_entity, db_entity_interest.db_entity.key):
        config_entity = layer.presentation.config_entity
        logger.debug("Handler: post_save_layer for config_entity {config_entity}, db_entity {db_entity}, and user {username}.".format(
            config_entity=config_entity,
            db_entity=db_entity_interest.db_entity,
            username=db_entity_interest.db_entity.updater.username,
        ))
        _on_layer_post_save(layer)

@receiver_subclasses(post_save, Layer, "layer_post_save")
def on_layer_post_save(sender, **kwargs):
    # Never run on creation unless we are running without CELERY in test mode
    # In no-celery testing the DbEntity will be post_save published completely before the layer is first saved,
    # so we have to run post save publishing
    layer = kwargs['instance']
    config_entity = layer.presentation.config_entity.subclassed_config_entity
    db_entity = config_entity.computed_db_entities(key=layer.db_entity_key, with_deleted=True)[0]

    config_entity = config_entity.db_entity_owner(db_entity)
    if layer._no_post_save_publishing:
        return
    if not settings.CELERY_ALWAYS_EAGER:
        return
    # Make sure the corresponding layer of other Scenarios save
    for layer in _update_or_create_child_layers(config_entity, layer.db_entity_key):
        _on_layer_post_save(layer)

def _on_layer_post_save(layer):
    """
        Called after a Layer saves, but not when a config_entity is running post_save publishers
        In other words, this is only called after a direct Layer save/update.
        This does the same as on_config_entity_post_save_layer, but starts with the 'post_save_es'
        signal to do only DbEntity dependent publishing.
    """

    if layer._no_post_save_publishing:
        return
    config_entity = layer.presentation.config_entity.subclassed_config_entity
    # Only create layers for Scenarios
    if not isinstance(config_entity, Scenario):
        return

    db_entity_interest = config_entity.computed_db_entity_interests(db_entity__key=layer.db_entity_key, with_deleted=True)[0]

    if db_entity_interest.deleted:
        # If the db_entity_interest is deleted, make sure the layer is deleted.
        layer.deleted= True
        layer._no_post_save_publishing = True
        layer.save()
        layer._no_post_save_publishing = False
        return

    db_entity = db_entity_interest.db_entity
    user = db_entity.creator if config_entity.creator else User.objects.all()[0]
    # post_save_db_entity publishing should always be disabled if we are saving a ConfigEntity
    logger.debug("Handler: post_save_layer for config_entity {config_entity}, db_entity {db_entity}, and user {username}.".format(
        config_entity=config_entity,
        db_entity=db_entity,
        username=user.username,
    ))

    starting_signal_path = resolvable_module_attr_path(__name__, 'post_save_layer_initial')

    try:
        # Make sure no transactions are outstanding
        transaction.commit()
    except Exception, e:
        pass
    return post_save_publishing(
        starting_signal_path,
        config_entity,
        user,
        instance=layer,
        instance_key=db_entity.key,
        signal_proportion_lookup=signal_proportion_lookup,
        dependent_signal_paths=dependent_signal_paths,
        signal_prefix='post_save_layer'
    )


def on_config_entity_post_save_layer(sender, **kwargs):
    """
        Sync tilestache to a ConfigEntity class after the latter is saved
        :param **kwargs: optional "db_entity_keys" to limit the layers created to those DbEntities
    """
    from footprint.client.configuration.fixture import LayerConfigurationFixture
    from footprint.client.configuration.utils import resolve_fixture
    # Disable post save publishing on individual layers. The ConfigEntity is controlling publishing
    config_entity = kwargs['instance']
    logger.debug("\t\tHandler: on_config_entity_post_save_layer. ConfigEntity: %s" % config_entity.name)

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

    for layer_library_configuration in \
        client_layer_configuration.matching_scope(client_layer_configuration.layer_libraries(),
                                                  class_scope=config_entity.__class__):
        _update_or_create_layer_library_and_layers(config_entity, layer_library_configuration, **kwargs)



def _update_or_create_layer_library_and_layers(config_entity, layer_library_configuration, **kwargs):
    """
        Update or create the LayerLibrary for the given config_entity and configuration.
        Also create update or create all layers of that library unless limited by kwargs['db_entity_keys']
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
            filter(lambda db_entity_key: config_entity.valid_computed_db_entities(key=db_entity_key).count() == 1,
                   db_entity_keys))
    else:
        if not config_entity.origin_instance:
            # Update or create the Layers of the layer_library_configuration
            layers = map(
                lambda layer_configuration: update_or_create_layer(layer_library, layer_configuration),
                layer_library_configuration.data.presentation_media_configurations)
        else:
            # If this is a cloned config_entity, clone or update clones
            layers = map(
                lambda origin_layer: clone_or_update_cloned_layer(layer_library, origin_layer),
                filter(lambda layer: layer.db_entity_interest.db_entity.is_valid,
                       Layer.objects.filter(presentation__config_entity=config_entity.origin_instance)))

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
                tags=layer.tags.all()
            ),
            dict(
                built_form_set_key=layer.configuration.get('built_form_key', None),
                sort_priority=layer.configuration.get('sort_priority', None),
                attribute_sort_priority=layer.configuration.get('attribute_sort_priority', None),
                column_alias_lookup=layer.configuration.get('column_alias_lookup', None),
            ) if layer.configuration else dict(),
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

def update_or_create_layer(layer_library, layer_configuration=None, db_entity_key=None, skip_layer_selection=False):
    """
        Create a Layer for each DbEntity in the LayerConfiguration. These instances constitute the default
        library of the config_entity, which is a library of all DbEntities. The media of these instances can be set
        to style media.
    :param layer_configuration: Optional. A full configuration
    :param db_entity_key. Optional. Use instead of full configuration to generate defaults
    :return:
    """

    # Turn off all layer post_save_publishing, otherwise saving the layer below would infinitely recurse
    # The only layer save that triggers on_layer_post_save is an independent save of a layer.
    # The code here is called by that or by the on_config_entity_post_save layer
    Layer._no_post_save_publishing = True

    if not layer_configuration:
        # See if the layer and its configuration exists
        layers = Layer.objects.filter(presentation=layer_library, db_entity_key=db_entity_key)
        if len(layers) == 1 and layers[0].configuration:
            # Restore configuration
            logger.debug("\t\t Imported Layer for %s already exists. Updating" % db_entity_key)
            layer_configuration = layer_configuration_from_layer(layers[0])
        else:
            # Create the configuration
            logger.debug("\t\t Imported Layer for %s does not exist. Creating" % db_entity_key)
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
                    [Tag.objects.update_or_create(tag=layer.presentation.config_entity.db_entity_owner(layer.db_entity_interest.db_entity).name)[0]]))

    # Customize the medium_context to have a class that refers specifically to this layer
    # TODO document why this is needed [it is not]
    if template_context:
        layer.medium_context['htmlClass'] = 'layer_{0}'.format(layer.id)
        layer.save()

    if not skip_layer_selection:
        # Update or create the LayerSelection tables and instances for this layer
        update_or_create_layer_selections_for_layer(layer)

    Layer._no_post_save_publishing = False
    return layer


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

    # Do nothing if the layer doesn't have features, such as background imagery
    if not layer.db_entity_interest.db_entity.feature_class_configuration:
        return

    layer_selection_class = get_or_create_dynamic_layer_selection_class_and_table(layer)
    if layer_selection_class:
        logger.debug("\t\t\tCreating LayerSelection for Layer of DbEntity Key: %s" % layer.full_name)
        for user in User.objects.all():
            # Create an instance for each user in the system
            logger.debug("\t\t\t\t Inserting LayerSelection instance for user: %s" % user.username)
            layer_selection_class.objects.update_or_create(user=user)


def create_layer_configuration_for_import(config_entity, db_entity_key):
    """
        Creates a LayerConfiguration for imported layers using the template
        LayerConfigurations designed in the LayerConfigurationFixture.import_layer_configurations
    """
    from footprint.client.configuration.fixture import LayerConfigurationFixture
    from footprint.client.configuration.utils import resolve_fixture
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

def on_post_save_built_form_layer(sender, **kwargs):
    """
        A signal handler to redo styles on relevant layers after a BuiltForm instances is created or updated.

    """
    from footprint.client.configuration.fixture import LayerConfigurationFixture
    from footprint.client.configuration.utils import resolve_fixture

    built_form = kwargs['instance']
    if built_form.__class__.__name__ in ['Crop', 'CropType', 'LandscapeType']:
        built_form_dependent_db_entity_keys = [DbEntityKey.FUTURE_AGRICULTURE, DbEntityKey.BASE_AGRICULTURE]
    else:
        built_form_dependent_db_entity_keys = [DbEntityKey.FUTURE_SCENARIO, DbEntityKey.END_STATE]
    layer_fixture = resolve_fixture(
        "publishing",
        "layer",
        LayerConfigurationFixture,
        settings.CLIENT)
    layer_fixture.update_or_create_media(built_form_dependent_db_entity_keys)

    # Find all DbEntities that reference built_form.
    layer_libraries = LayerLibrary.objects.filter(deleted=False)
    # Find the corresponding layers of all LayerLibrary instances
    layers = Layer.objects.filter(presentation__in=layer_libraries, db_entity_key__in=built_form_dependent_db_entity_keys)
    # Turn off post save publishing for layers. The built_form_publisher will do tilestache saves explicitly
    # The only purpose of this is to get better progress indicators. It won't be needed when we redo progress signals later
    # Invalidate these layers
    for layer in layers:
        update_or_create_layer(layer.presentation, db_entity_key=layer.db_entity_key, skip_layer_selection=True)

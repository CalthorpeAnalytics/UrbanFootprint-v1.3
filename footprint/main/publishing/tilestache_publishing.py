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
# from memory_profiler import profile
import os
import logging
import shutil
import TileStache
from TileStache.Config import buildConfiguration
from footprint.main.models.presentation.layer import Layer
from footprint.main.models.presentation.layer_library import LayerLibrary
from footprint.main.models.presentation.tilestache_config import TileStacheConfig
from footprint.main.models.config.scenario import Scenario
from footprint.main.models.config.config_entity import ConfigEntity

import shlex
import subprocess
import json
from django.template import Template, Context
from footprint.main.models.keys.keys import Keys
from footprint.main.utils.utils import database_settings, create_static_content_subdir, get_property_path
from TileStache.Config import _parseConfigfileLayer
from django.contrib.auth.models import User
from footprint.main.lib.functions import merge, unique
from footprint.main.models.presentation.layer_selection import get_or_create_dynamic_layer_selection_class_and_table
from footprint.main.utils.utils import connection_dict
from django.conf import settings
logger = logging.getLogger(__name__)

#@profile
def on_config_entity_post_save_tilestache(sender, **kwargs):
    """
        Update/Create the tilestache data for the layers given DbEntityInterest
        :param: kwargs: Optional db_entity_keys to limit the layers to those of the given keys
    """
    config_entity = kwargs['instance']
    logger.debug("\t\tHandler: on_config_entity_post_tilestache. ConfigEntity: %s" % config_entity.name)
    if ConfigEntity._heapy:
        ConfigEntity.dump_heapy()
    if not isinstance(config_entity, Scenario):
        return

    _on_post_save_tilestache(config_entity, **kwargs)

#@profile
def on_db_entity_post_save_tilestache(sender, **kwargs):
    """
        Update/Create the tilestache data for the layer(s) of the given DbEntityInterest
    """

    logger.debug("\t\tHandler: on_db_entity_post_save_tilestache")
    if ConfigEntity._heapy:
        ConfigEntity.dump_heapy()

    db_entity_interest = kwargs['instance']
    config_entity = db_entity_interest.config_entity.subclassed_config_entity
    db_entity = db_entity_interest.db_entity
    _on_post_save_tilestache(config_entity, db_entity_keys=[db_entity.key])

def _on_post_save_tilestache(config_entity, **kwargs):
    """
        Update/Create of the tilestache data for layers of the config_entity
        :param: config_entity
        :param: kwargs: Optional db_entity_keys to limit the layers to those of the given keys
    """

    layer_libraries = LayerLibrary.objects.filter(
        scope=config_entity.schema(),
        config_entity=config_entity
    )
    layers = Layer.objects.filter(presentation__in=layer_libraries,
                                  db_entity_key__in=kwargs['db_entity_keys']) if kwargs.get('db_entity_keys') else \
        Layer.objects.filter(presentation__in=layer_libraries)
    tilestache_config, created, updated = TileStacheConfig.objects.update_or_create(name='default')
    modify_config(config_entity, tilestache_config, layers)

def modify_config(config_entity, tilestache_config, layers):
    """
        Using the attributes of the given Layer objects, updates the default tilestache configuration object and stores
        it in the database. Each layer instance is used to create a raster, vector, and selection (vector) layer for
        each configured attribute. These layers are keyed uniquely by the layer instance id, attribute, and layer type,
        so they will simply overwrite themselves in the config and accumulate.

    :param tilestache_config:
    :param layers:
    :return:
    """

    if tilestache_config.enable_caching:
        cache = {
            "name": "Disk",
            "path": "/tmp/stache",
            "umask": "0000"
        }

    else:
        cache = {"name": "Test"}

    # Get or define the config dict
    config = tilestache_config.config if isinstance(tilestache_config.config, TileStache.Config.Configuration) else buildConfiguration({
        'logging': "info",
        'layers': {},
        'cache': cache,
        })

    for layer in layers:
        # If the layer contains a style configuration
        if layer.medium_context:

            # Render the raster styles for each attribute styled in the layer's medium
            render_attribute_styles(layer)

            # Create a vector, raster, and vector select layer for each attribute listed in the medium_context
            for attribute, medium_context in layer.medium_context['attributes'].items():
                logger.debug("\t\t\t: Creating tilestache layer for layer %s, attribute %s" % (layer.db_entity_key, attribute))
                create_vector_layer(config_entity, layer, attribute, config)
                create_raster_layer(config_entity, layer, attribute, config)
                create_layer_selection(config_entity, layer, attribute, config)
            invalidate_cache(layer, config)

    tilestache_config.config = config
    tilestache_config.save()


def on_config_entity_pre_delete_tilestache(sender, **kwargs):
    pass


def create_vector_layer(config_entity, layer, attribute, config):
    # If the db_entity doesn't have an explicit query create a query from the table and schema that joins
    # in the geography column.
    db_entity = layer.db_entity_interest.db_entity
    query = create_query(attribute, config_entity, layer)
    connection = connection_dict(layer.presentation.config_entity.db)
    vector_layer = {
        "metatile": {
            "rows": 6,
            "columns": 6,
            "buffer": 50,
            },
        'provider': {
            'name': 'vector',
            'driver': 'postgis',
            'clipped': False,
            'parameters': merge(
                connection,
                dict(
                    query=query,
                    column="wkb_geometry",
                )
            ),
            # 'properties': fields,

        },
        'allowed origin': "*",
        'id_property': db_entity._meta.pk.name
    }
    config.layers["layer_{0}_{1}_vector".format(layer.id, attribute)] = \
        _parseConfigfileLayer(vector_layer, config, '')


def create_raster_layer(config_entity, layer, attribute, config):
    raster_layer = {
        "metatile": {
            "rows": 6,
            "columns": 6,
            "buffer": 50,
        },
        'provider': {
            'name': 'mapnik',
            'mapfile': layer.rendered_medium[attribute]['cartocss']
        }
    }
    config.layers["layer_{0}_{1}_raster".format(layer.id, attribute)] = _parseConfigfileLayer(raster_layer, config, '')


def create_query(attribute, config_entity, layer):
    db_entity = layer.db_entity_interest.db_entity
    feature_class = config_entity.feature_class_of_db_entity_key(db_entity.key)
    # Create a query that selects the wkb_geometry and the attribute we need
    # There's nothing to prevent styling multiple attributes in the future
    try:
        query = str(feature_class.objects.values(*unique(['wkb_geometry', attribute])).query)
    except Exception, e:
        raise Exception("Error creating the query for db_entity %s. Original exception: %s" % (db_entity.key, e.message))
    column_alias = get_property_path(layer.configuration, 'column_alias_lookup.{0}'.format(attribute))
    # This would be better done by values() supporting aliases:
    # https://code.djangoproject.com/attachment/ticket/16735/column_alias.diff
    # There is a patch available at https://code.djangoproject.com/attachment/ticket/16735/column_alias.diff that could be applied instead of this:
    # Replace the select column with the colum as alias. Only 1 replacement is done to avoid mutilating a join with the same column
    updated_query = query.replace(
        '{column_alias}"'.format(column_alias=column_alias), '{column_alias}" as {attribute}'.format(
            column_alias=column_alias, attribute=attribute), 1) if column_alias else query
    return updated_query


def create_layer_selection(config_entity, layer, attribute, config):
    db_entity = layer.db_entity_interest.db_entity
    connection = connection_dict(layer.presentation.config_entity.db)

    for user in User.objects.all():
        # Each layer has a dynamic class representing its SelectedFeature table
        get_or_create_dynamic_layer_selection_class_and_table(layer)
        layer_selection_class = get_or_create_dynamic_layer_selection_class_and_table(layer)
        # Each LayerSelection instance is per user
        layer_selection = layer_selection_class.objects.get(user=user)
        layer_selection._meta._related_many_to_many_cache = None
        layer_selection._meta._related_objects_cache = None
        # Extract the query from the QuerySet
        query = str(layer_selection.selected_features.values('wkb_geometry').query)

        vector_selection_layer = {
            'provider': {
                'name': 'vector',
                'driver': 'postgis',
                'clipped': False,

                'parameters': merge(
                    connection,
                    dict(
                        query=query,
                        column="wkb_geometry",
                    )
                ),
                # 'properties': fields,

            },
            'write cache': False,
            'allowed origin': "*",
            'id_property': db_entity._meta.pk.name
        }

        vector_selection_layer = _parseConfigfileLayer(vector_selection_layer, config, '')
        # TODO we'll need to use raster at higher zoom levels
        # raster_selection_layer = _parseConfigfileLayer(raster_layer, config, '')

        config.layers["layer_{0}_{1}_{2}_selection".format(layer.id, attribute, user.id)] = vector_selection_layer
        # config.layers["layer_{0}_{1}_{2}_raster".format(db_entity_id, attribute)] = raster_layer


def style_id(layer):
    layer_library = layer.presentation
    return 'style__{0}__{1}__{2}'.format(layer_library.subclassed_config_entity.id, layer_library.id, layer.db_entity_key)

def render_attribute_styles(layer):
    """
        Iterates through the Layer.medium_context attributes, using the context stored for each attribute to render
        the css and cartocss style templates. The results are placed in the layer.rendered_medium in the form
        dict(attribute1:dict('css':rendered_css, 'cartocss': rendered_carto_css)). The carto_css is actually a file
        path since this is required by tilestache (TODO that it can't be a string)
    :param layer:
    :return:
    """

    # Fetch the dictionary of styles data for each styled attribute
    style = layer.medium_context
    style['id'] = style_id(layer)

    # Write the style to the filesystem
    for attribute, attribute_context in layer.medium_context['attributes'].items():
        layer.rendered_medium[attribute] = {}
        layer.rendered_medium[attribute]['css'] = make_css(layer, attribute)
        layer.rendered_medium[attribute]['cartocss'] = make_carto_css(layer, attribute)

    layer.save()

    return layer


def make_css(layer, attribute):
    """
        Loads the SVG CSS for the given attribute name
    :param layer: The Layer instance
    :param attribute: An attribute/column of the DbEntity, such as built_form_id
    :return:
    """

    # Take the possibly customized context of the layer. If the dict has not been customized, it will simply
    # match the default default layer.medium.template_context.context
    customized_context = Context(layer.medium_context)
    formatted_style = Template(layer.medium.content['attributes'][attribute]['css']).render(customized_context)
    return formatted_style


def make_carto_css(layer, attribute):
    """
    Renders a mapnik XML file based on the properties of the layer and, optionally,
    style attributes. This process first writes an MML file to the filesystem. It then invokes the node.js
    carto command to create a carto xml file

    :param layer:
    :param attribute:
    :return:
    """
    mml = make_mml(layer, attribute)
    xml_filepath = carto_css(mml, style_id(layer))
    return xml_filepath


def make_mml(layer, attribute):
    """
    Generates mml string from a layer and a style
    :param layer: Layer object
    :param attribute: the attribute of the layer object that is getting styled

    :return:
    """
    carto_css_style = make_carto_css_style(layer, attribute)
    #sys.stdout.write(str(carto_css_style))
    db = database_settings(layer.presentation.config_entity.db)
    query = create_query(attribute, layer.presentation.config_entity, layer)
    db_entity = layer.db_entity_interest.db_entity
    # Get the base version of the feature class that holds wkb_geometry
    feature_class = layer.presentation.config_entity.db_entity_feature_class(db_entity.key, base_class=True)

    mml = {
        "Layer": [
            {
                "Datasource": {
                    "dbname": db['NAME'],
                    "extent": "",
                    "geometry_field": "wkb_geometry",
                    "host": "localhost",
                    "password": db['PASSWORD'],
                    "port": db['PORT'],
                    "srid": 4326,
                    # Put the query in the table property as a subquery
                    # Mapnik will wrap this in SELECT AsBinary('wkb_geometry') as subquery WHERE 'wkb_geometray' and ...bounds...
                    "table": '(%s) as foo' % query,
                    # The base feature_class holds wkb_geometry
                    "geometry_table": feature_class._meta.db_table,
                    "type": "postgis",
                    "user": db['USER'],
                },
                "id": layer.id,
                "name": style_id(layer),

                #TODO: look up layer tag from the library so that we can use this function for any layer
                "class": db_entity.key,

                #TODO: look up geometry type from the geometry_columns table
                "geometry": "polygon",
                "srs": Keys.SRS_4326,
                },
            ],
        "Stylesheet": [carto_css_style],
        "interactivity": True,
        "maxzoom": 15,
        "minzoom": 7,
        "format": "png",
        "srs": Keys.SRS_GOOGLE,

        }
    #sys.stdout.write(str(mml))
    return json.dumps(mml)


def make_carto_css_style(layer, attribute):
    """
    :param layer: the layer to be styled
    :param attribute: The attribute whose cartocss template is to be rendered with the layer.medium_context as the
    template context
    :return  dict with an id in the form {layer.name}.mss and data key valued by the rendered template
    """

    style_template = Template(layer.medium.content['attributes'][attribute]['cartocss'])
    context = Context(layer.medium_context)
    formatted_style = style_template.render(context)
    return {
        'id': '{0}.mss'.format(style_id(layer)),
        'data': "{0}".format(formatted_style)
    }

def carto_css(mml, name):
    """
    Takes MML string input and writes it to a Mapnik XML file.
    :param mml: an mml string, containing the proper CartoCSS styling and connection attributes required by the
    CartoCSS conversion program
    :param name: the unique name of the layer (standard method is to name it with its database schema and table name)
    :return mapfile: a cascadenik-ready document.
    """

    create_static_content_subdir('cartocss')
    mmlFile = "{0}/cartocss/{1}.mml".format(settings.MEDIA_ROOT, name)
    mapFile = mmlFile.replace(".mml", ".xml")
    f = open(mmlFile, 'w+')
    f.write(mml)
    f.close()

    logger.debug("Path: %s" % os.environ['PATH'])
    carto_css_command = shlex.split("carto {0} > {1}".format(mmlFile, mapFile))
    logger.debug("Running carto: %s" % carto_css_command)
    carto_css_content = None
    try:
        carto_css_content = subprocess.check_output(carto_css_command)
        f = open(mapFile, 'w')
        f.write(carto_css_content)
        f.close()

    except Exception, e:
        logger.error("Failed to generate cartocss for {mml}. Exception: {message}. Fix the mml and run footprint_init --tilestache --skip".format(mml=mmlFile, message=e.message, carto_output=carto_css_content))
        raise e

    return mapFile

def on_post_analytic_run_tilestache(sender, **kwargs):
    """
        Responds to analytic module runs
        kwargs: module is the string name of the module (TODO covert to instance)
            config_entity is the config_entity that ran
    :return:
    """

    module = kwargs['module']
    config_entity = kwargs['config_entity']

    logger.debug("\t\tHandler: on_post_analytic_run_tilestache. ConfigEntity: %s. Module %s" % (config_entity.name, module))

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
        layer_cache = shlex.os.path.join(tilestache_cache_path, tilestache_layer_name + "{user_id}_{layer_type}".format(
            user_id='_{0}'.format(user.id) if user else '',
            layer_type=layer_type
        ))
        if shlex.os.path.exists(layer_cache):
            shutil.rmtree('{cache}'.format(cache=layer_cache))


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
import TileStache
from TileStache.Config import buildConfiguration

from footprint.models import Layer, LayerLibrary, TileStacheConfig, Scenario
from footprint.publishing.mapnik_api import render_attribute_styles
from footprint.publishing.tilestache_layers import create_vector_layer, create_raster_layer, create_layer_selection


def on_config_entity_post_save_tilestache(sender, **kwargs):
    config_entity = kwargs['instance']
    if not isinstance(config_entity, Scenario):
        return

    layer_libraries = LayerLibrary.objects.filter(
        scope=config_entity.schema(),
        config_entity=config_entity
    )

    layers = Layer.objects.filter(presentation__in=layer_libraries)
    tilestache_config, created, updated = TileStacheConfig.objects.update_or_create(name='default')
    modify_config(tilestache_config, layers)

def modify_config(tilestache_config, layers):
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
                create_vector_layer(layer, attribute, config)
                create_raster_layer(layer, attribute, config)
                create_layer_selection(layer, attribute, config)

    tilestache_config.config = config
    tilestache_config.save()

def on_config_entity_pre_delete_tilestache(sender, **kwargs):
    pass

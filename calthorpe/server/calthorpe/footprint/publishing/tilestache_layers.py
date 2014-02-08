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

from TileStache.Config import _parseConfigfileLayer
from django.contrib.auth.models import User
from footprint.lib.functions import merge
from footprint.models.presentation.layer_selection import create_dynamic_layer_selection_class_and_table
from footprint.utils.utils import connection_dict

def create_vector_layer(layer, attribute, config):
    # If the db_entity doesn't have an explicit query create a query from the table and schema that joins
    # in the geography column.
    db_entity = layer.db_entity_interest.db_entity
    query_or_table = db_entity.query if db_entity.query not in ('', None) \
        else "{0}.{1}".format(db_entity.schema, db_entity.table)
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
                    # TODO: debug this s.t. the query actually workssample_core_run.py
                    table=query_or_table,
                    column="wkb_geometry"
                )
            ),
            # 'properties': fields,

        },
        'allowed origin': "*",
        'id_property': db_entity._meta.pk.name,
    }
    config.layers["layer_{0}_{1}_vector".format(layer.id, attribute)] =\
        _parseConfigfileLayer(vector_layer, config, '')

def create_raster_layer(layer, attribute, config):
    db_entity = layer.db_entity_interest.db_entity
    raster_layer = {
        "metatile": {
            "rows": 6,
            "columns": 6,
            "buffer": 50,
        },
        'provider': {
            'name': 'mapnik',
            'mapfile': layer.rendered_medium[attribute]['cartocss'],

        }
    }
    config.layers["layer_{0}_{1}_raster".format(layer.id, attribute)] = _parseConfigfileLayer(raster_layer, config, '')


def create_layer_selection(layer, attribute, config):
    db_entity = layer.db_entity_interest.db_entity
    connection = connection_dict(layer.presentation.config_entity.db)

    for user in User.objects.all():
        # Each layer has a dynamic class representing its SelectedFeature table
        create_dynamic_layer_selection_class_and_table(layer)
        layer_selection_class = create_dynamic_layer_selection_class_and_table(layer)
        # Each LayerSelection instance is per Userget_all_related_objects()
        layer_selection = layer_selection_class.objects.update_or_create(user=user)[0]
        layer_selection._meta._related_many_to_many_cache = None
        layer_selection._meta._related_objects_cache = None
        try:
            str(layer_selection.features.query)
        except:
            # Fixes a terrible Django manyToMany cache initialization bug by clearing the model caches
            meta = super(layer_selection.features.__class__, layer_selection.features).get_query_set().model._meta
            for cache_attr in ['_related_many_to_many_cache', '_m2m_cache']:
                if hasattr(meta, cache_attr):
                    delattr(meta, cache_attr)
            meta.init_name_map()


        query = str(layer_selection.features.query)

        vector_selection_layer = {
            'provider': {
                'name': 'vector',
                'driver': 'postgis',
                'clipped': False,
                'write cache': False,
                'parameters': merge(
                    connection,
                    dict(
                        query=query,
                        column="geometry",
                    )
                ),
                # 'properties': fields,

            },
            'allowed origin': "*",
            'id_property': db_entity._meta.pk.name,
        }

        vector_selection_layer = _parseConfigfileLayer(vector_selection_layer, config, '')
        # TODO we'll need to use raster at higher zoom levels
        # raster_selection_layer = _parseConfigfileLayer(raster_layer, config, '')

        config.layers["layer_{0}_{1}_{2}_selection".format(layer.id, attribute, user.id)] = vector_selection_layer
        # config.layers["layer_{0}_{1}_{2}_raster".format(db_entity_id, attribute)] = raster_layer

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

import sys
from os import path
from django.core import serializers
from django.db import connections, transaction
from django.views.generic.simple import direct_to_template
from footprint.main.lib.functions import merge, map_to_dict
from footprint.main.utils.utils import table_name_only, string_not_empty, getSRIDForTable
from footprint.main.views import scenario_context
from django.conf import settings
sys.path.append(settings.CALTHORPE_ENGINE_PATH)
from django.utils.safestring import mark_safe
import TileStache
from TileStache.Config import buildConfiguration
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils import simplejson
from footprint.main.models.config.scenario import Scenario


def get_config():
    with open(path.join(settings.STATIC_ROOT, "js/tile_stache_config.js")) as f:
        json = simplejson.load(f)
    return buildConfiguration(json)

@login_required
def tilestache(request, layer_name, z, x, y, extension):
    """
    Proxy to tilestache
    {X} - coordinate column.
    {Y} - coordinate row.
    {B} - bounding box.
    {Z} - zoom level.
    {S} - host.
    """
    config = get_config()
    path_info = "%s/%s/%s/%s.%s" % (layer_name, z, x, y, extension)
    coord, extension = TileStache.splitPathInfo(path_info)[1:]
    mimetype, content = TileStache.getTile(config.layers[layer_name], coord, extension)
    return HttpResponse(content, mimetype=mimetype)

@login_required
def view_tilestache_map(request, scenario_id):
    return tilestache_map(request, scenario_id, False)

@login_required
def view_tilestache_map_fullscreen(request, scenario_id):
    return tilestache_map(request, scenario_id, True)

def tilestache_map(request, scenario_id, fullscreen):
    scenarios = Scenario.objects.filter(id=scenario_id)
    scenario = scenarios[0]

    config = get_config()
    layer_urls = []
    for l in config.layers:
        if isinstance(config.layers[l].provider, TileStache.Providers.Vector.Provider):
            # TODO reverse doesn't work on tiles (probably because it's not in views.py) Thus we are forced to use the EXTERNAL_HOST_URL.
            #layer_urls.append(reverse('tilestache', current_app='main', args=[l, '{Z}', '{X}', '{Y}', 'geojson']).replace('%7B', '{').replace('%7D', '}')) # FAILS to resolve the tilestache view
            layer_urls.append(settings.EXTERNAL_HOST_URL + "/footprint/tilestache/{0}/{1}/{2}/{3}.{4}".format(l, '{Z}', '{X}', '{Y}', 'geojson').replace('%7B', '{').replace('%7D', '}'))
    return render_to_response('footprint/scenario_polymaps.html',
        merge({
            's':scenario,
            'layerUrls' : mark_safe(simplejson.dumps(layer_urls)),
        }), context_instance=RequestContext(request))

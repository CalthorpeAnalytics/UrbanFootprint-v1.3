from django.http import HttpResponse
from footprint.main.models import TileStacheConfig

__author__ = 'calthorpe_associates'

import TileStache

def tilestache_tiles(request, layer_name, z, x, y, extension):
    """
    :param request:
    :param layer_name:
    :param z:
    :param x:
    :param y:
    :param extension:
    :return:

    Proxy to tilestache
    {X} - coordinate column.
    {Y} - coordinate row.
    {B} - bounding box.
    {Z} - zoom level.
    {S} - host.
    """

    config = TileStacheConfig.objects.filter(name='default')[0].config
    path_info = "%s/%s/%s/%s.%s" % (layer_name, z, x, y, extension)
    coord, extension = TileStache.splitPathInfo(path_info)[1:]
    mimetype, content = TileStache.getTile(config.layers[layer_name], coord, extension)
    return HttpResponse(content, mimetype=mimetype)

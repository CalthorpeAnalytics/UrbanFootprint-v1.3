import os, TileStache

config_file = os.environ.get('TILESTACHE_CONFIG', '/srv/calthorpe/urban_footprint/calthorpe/server/calthorpe/mainsite/static/js/tile_stache_config.js')
application = TileStache.WSGITileServer(config_file)

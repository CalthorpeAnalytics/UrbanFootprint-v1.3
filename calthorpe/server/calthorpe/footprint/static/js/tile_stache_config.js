fake_config = {
  "logging":"info",
  "cache":
  {
    "name": "Disk",
    "path": "/tmp/stache",
    "umask": "0000",
    "verbose": true
  },
  "layers":
  {
        "parcels": {
                "provider": {
                    "name": "vector",
                    "driver": "postgis",
                    "clip": false,
                    "parameters": {
			"host":     "localhost",
                        "dbname": "urbanfootprint",
                        "user": "calthorpe",
                        "password": "Calthorpe123",
                        "table": "public.sacog_2035_scs_parcel_canvas",
                        "column":"wkb_geometry"
                    }
                }
            },
      "osm":
    {
        "provider": {"name": "proxy", "provider": "OPENSTREETMAP"},
        "png options": {"palette": "http://tilestache.org/example-palette-openstreetmap-mapnik.act"}
    }
  }
}

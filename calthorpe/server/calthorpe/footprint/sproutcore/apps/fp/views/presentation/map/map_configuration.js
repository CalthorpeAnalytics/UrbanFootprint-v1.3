require('resources/mousetrap')

$(function() {
    window.po = org.polymaps;
});

/***
 * A configuration of the polymaps layer for a particular Footprint.Layer instance
 * @type {*}
 */
Footprint.MapLayerGroup = SC.Object.extend({

    /***
     * The attribute names of the three layers in each mapLayerGroup.
     * The vector and selectionLayer are both vector layers, the raster is ... a raster
     * raster and vector are different representations of the underlying geometries, whereas selectionLayer is a subset
     * of the geometries of raster/vector that the user has selected.
     */
    mapLayerGroupLayers:['raster', 'vector', 'selectionLayer'],

    map:null,

    /***
     * Adds all the mapLayerGroup layers to the map
     */
    addLayersToMap: function() {
        var map = this.get('map');
        this.get('mapLayerGroupLayers').forEach(function(name) {
            var mapLayer = this.get(name);
            if (mapLayer)
                map.add(mapLayer);
        }, this);
    },

    // An example of adding events to vector features
    _addListersToFeatures: function(mapLayer) {
            /*
             if (name == 'selectionLayer' && mapLayer.features) {
             var features = mapLayer.features();
             features.forEach(function(feature) {
             // add double-click listener, which pops up with information specified in the fields
             feature.element.addEventListener("dblclick", (function(feature) {
             return function(event) {
             SC.AlertPane.info(feature);
             }
             })(feature), false);

             // add click listener, which checks if the option key is being pressed before acting
             feature.element.addEventListener("click", (function(feature) {
             return function(event) {
             if (event.altKey) {
             SC.AlertPane.info(feature);
             }
             }
             })(feature), false);
             }, this);
             }
             */
    },

    /***
     * Bound to layer.visible to indicate whether the group should be shown or not.
     */
    visible:null,
    visibleBinding:SC.Binding.oneWay('*layer.visible'),

    onVisible: function() {
        if (!this.didChangeFor('onVisibleChange', 'visible'))
            return;
        this.setVisibilityBasedOnZoom();
    }.observes('.visible'),

    /***
     * Determines if the given mapGroupLayer is visible at the current map zoom level
     * @param mapLayerGroupLayerName
     * @returns {*}
     */
    visibleAtZoomLevel: function(mapLayerGroupLayerName) {
        var map = this.get('map');
        if (mapLayerGroupLayerName=='raster')
            return map.zoom() < 19;
        if (mapLayerGroupLayerName=='vector')
            return map.zoom() >= 19;
        return YES;
    },

    /***
     * Sets visibility of each mapLayerGroupLayer based on overall visibility and zoom level
     */
    setVisibilityBasedOnZoom: function() {
        this.get('mapLayerGroupLayers').forEach(function(name) {
            var mapLayer = this.get(name);
            if (mapLayer)
                mapLayer.visible(this.get('visible') && this.visibleAtZoomLevel(name));
        }, this);
    },
    /***
     * Set visibility based on the property of the layer
     */
    setVisibility: function() {
        this.get('mapLayerGroupLayers').forEach(function(name) {
            var mapLayer = this.get(name);
            if (mapLayer)
                mapLayer.visible(this.get('visible'))
        }, this);
    },


    /***
     * The Footprint.Layer instance
     */
    layer: null,
    /***
     * The vector map layer
    */
    vector: null,
    /***
     * The raster map layer
     */
    raster: null,
    /***
     * The user selection layer
     */
    selectionLayer: null,
    selection:null // not sure if we need this now
});

/***
 * A Mixin to MapView that configures the map and layers.
 * Note that all references to layers indicate Footprint.Layer instances. All references to mapLayers indicate
 * Polymaps layers.
 * Over time more and more of data here should move into mediating controllers and models.
 * For instance, the background map image(s) should be a selectable and/or configurable
 * @type {*}
 */
Footprint.MapConfiguration = {


    /***
     * The initial center of the map, calculated based on the bounds of the content
     */
    mapInitialCenter: function() {
        // TODO remove hard-coded center
        return {lat: 38.5450, lon: -121.7394};
    }.property('content').cacheable(),

    mapInitialExtent: function() {
        // TODO remove hard-coded initial extent
        return this.get('configuredExtent') || [
            {lat: 38.5, lon: -121.8},
            {lat: 38.6, lon: -121.7}
        ]
    }.property('content').cacheable(),

    configuredExtent: null,
    observeConfiguredExtent:function() {
        if (this.get('mapCreated') && this.get('configuredExtent')) {
            this.extent(this.get('configuredExtent'));
        }
    }.observes('.configuredExtent'),

    configuredCenter: null,
    observeConfiguredCenter:function() {
        if (this.get('mapCreated') && this.get('configuredCenter')) {
            this.center(this.get('configuredCenter'));
        }
    }.observes('.configuredCenter'),

    /***
     * Sets the center of the map
     * @param lat_lon_dict
     */
    center: function(lat_lon_dict) {
        //this.get('map').center(lat_lon_dict);
    },

    /***
     * Sets the extent of the map
     * @param lat_lon_dict
     */
    extent: function(bbox) {
        this.get('map').extent(bbox);
    },

    /***
     * The zoom range of the map
     */
    mapZoomRange: function() {
        return [10, 18];
    }.property().cacheable(),

    /***
     * The initial zoom level of the map
     * TODO this should be based on the content bounds in the future
     */
    mapInitialZoom: function() {
        return 16;
    }.property().cacheable(),

    /***
     * The div element containing the polymaps map.
     * @returns {*}
     */
    mapNode: function() {
        return this.$('.footprint-map')[0];
    }.property(),

    /***
     * Non-backgound layers
     */
    foregroundLayers: function() {
        if (this.get('layers') && this.get('layersStatus') & SC.Record.READY)
            return this.get('layers').filter(function(layer) {
                return !layer.get('tags').mapProperty('tag').contains('background');
            }, this);
        return [];
    }.property('layers', 'layersStatus').cacheable(),

    /***
     * Backgound layers
     */
    backgroundLayers: function() {
        if (this.get('layers') && this.get('layersStatus') & SC.Record.READY)
            return this.get('layers').filter(function(layer) {
                return layer.get('tags').mapProperty('tag').contains('background');
            }, this) || [];
        return [];
    }.property('layers', 'layersStatus').cacheable(),

    /***
     * Each layer in layers has a unique db_entity_key that is used to identify it in mapLayerGroups
     * This returns all of them
     */
    foregroundLayerKeys: function() {
        if (this.get('foregroundLayers') && this.get('layersStatus') & SC.Record.READY)
        return this.get('foregroundLayers').mapProperty('db_entity_key');
    }.property('foregroundLayers', 'layersStatus').cacheable(),

    /***
     * Each layer in layers has a unique db_entity_key that is used to identify it in mapLayerGroups
     * This returns all of them
     */
    backgroundLayerKeys: function() {
        if (this.get('backgroundLayers') && this.get('layersStatus') & SC.Record.READY)
            return this.get('backgroundLayers').mapProperty('db_entity_key');
    }.property('backgroundLayers', 'layersStatus').cacheable(),

    /**
     * All layer keys
     */
    layerKeys: function() {
        if (this.get('layers') && this.get('layersStatus') & SC.Record.READY)
            return this.get('layers').mapProperty('db_entity_key');
    }.property('layers', 'layersStatus').cacheable(),

    /***
     * An SC.Object of Footprint.MapLayerGroup instances, keyed by db_entity_key. Each layerGroup holds a vector, raster,
     * and layer_selection layer corresponding to a Footprint.Layer instance. Footprint.Layer instances are those
     * of the ConfigEntity's configured map Presentation instance.
     */
    mapLayerGroups: null,

    /***
     * The activeLayerGroup based on the activeLayer
     * @returns {*}
     */
    activeLayerGroup: function() {
        if (this.getPath('activeLayer.db_entity_key'))
            return this.get('mapLayerGroups').getPath(this.getPath('activeLayer.db_entity_key'));
    }.property('activeLayer').cacheable(),

    /***
     * The DOM element where the map is found (used for dblclick and other browser signals to the map)
     */
    mapWindow: null,

    /***
     * Called at the first render to setup the map
     * @private
     */
    createMap: function() {
        this.set('map', po.mcmap()
//            .tileSize({X: 512, Y: 512})
            // Set the map container and add the svg element
            .container(this.get('mapNode').appendChild(po.svg("svg")))

            // Center the map in the middle of the active ConfigEntity and calculate the zoom based on the bounds
            .center(this.get('mapInitialCenter')).zoomRange(this.get('mapZoomRange')).zoom(this.get('mapInitialZoom')));

        var map = this.get('map');

        // Add the background images
        // TODO make this configurable
        var background_uris = this.get('mapBackgroundUri');

        // Set additional properties on the container
        map.container().setAttribute("id", "map-interface");
        map.container().setAttribute("width", "100%");
        map.container().setAttribute("height", "100%");

        this.mapWindow = map.focusableParent();

        // Enable drag and mouse wheel
        map.add(po.compass(map));
        map.add(po.drag(map));
        map.add(po.wheel(map));

        map.on('move', function() {
            Footprint.mapController.refreshMapLayerZoomVisibility()
        });

        this.initStyling();
        this.set('mapCreated', YES);

        // Center to the project bounds
        this.set('configuredCenter', this.mapInitialCenter);
        this.onProjectActiveControllerStatus();
        this.addObserver('layers', this, 'updateLayers');
        this.addObserver('layersStatus', this, 'updateLayers');
    },

    onProjectActiveControllerStatus: function() {
        if (Footprint.projectActiveController.get('status') === SC.Record.READY_CLEAN) {
            var project = Footprint.projectActiveController.get('content');
            this.set('configuredExtent', this._polygonBoundingBox(project.getPath('bounds.coordinates')));
        }
    }.observes('Footprint.projectActiveController.status'),

    _polygonCenter: function(coordinates) {
        var pairs = [];
        for (var i=0; i<coordinates.length-2; i+=2) { // -2 to skip redundant polygon point
            pairs.push({lon:coordinates[i], lat:coordinates[i+1]})    ;
        }
        var avgLat = $.accumulate(pairs, function(pair, previous) { return pair.lat + previous;})/pairs.length;
        var avgLon = $.accumulate(pairs, function(pair, previous) { return pair.lon + previous;})/pairs.length;
        return {lat:avgLat, lon:avgLon};
    },


    _polygonBoundingBox: function(coordinates) {
        var longitudes = [];
        var latitudes = [];
        for (var i=0; i<coordinates.length-2; i+=2) { // -2 to skip redundant polygon point
            longitudes.push(coordinates[i]);
        }
        for (var j=1; j<coordinates.length-2; j+=2) {
            latitudes.push(coordinates[j]);
        }
        longitudes.sort(function(a, b) { return a - b });
        latitudes.sort(function(a, b) { return a - b });

        return [{lat:latitudes[0], lon:longitudes[0]},
            {lat:latitudes[latitudes.length - 1], lon:longitudes[longitudes.length - 1]}];
    },

    _oldLayerKeys:  [],
    _oldBackgroundLayerKeys:  [],
    /***
     * Iterates through the layers of the layers and configures each layer.
     * This is called whenever the layersController's content changes or one of its layers is added, edited,
     * or removed
     * @private
     */
    updateLayers:function() {
        if (!((this.get('layersStatus') & SC.Record.READY) && this.get('layers') ))
            return;
        if (!this.didChangeFor('layersDidChange', 'layers'))
            return;

        var map = this.get('map');
        // TODO temporary while I figure out how to wait for divs to size before creating the map
        map.resize();

        /***
         * Remove existing layers.
         * TODO this is inaccurate. This should be performed by the showing_map state when the content instance
         * changes. The problem here is if the foregroundLayerKeys change from one content instance to the next (which they
         * do), this won't remove everything.
         */
        map.remove(po.compass(map));
        if (this.get('mapLayerGroups')) {
            var mapLayerGroups = this.get('mapLayerGroups');
            this._oldLayerKeys.forEach(function(layerKey) {
                var mapLayerGroup = mapLayerGroups.get(layerKey);
                if (mapLayerGroup) {
                    mapLayerGroup.get('mapLayerGroupLayers').forEach(function(mapLayerName) {
                        if (mapLayerGroup.get(mapLayerName))
                            map.remove(mapLayerGroup.get(mapLayerName));
                    }, this);
                }
            }, this)
        }
        this._oldLayerKeys = this.get('layerKeys');

        // get active layers, create Polymaps objects for them
        // layerGroups are keyed by the DbEntity name
        var self = this;

        this.set('mapLayerGroups', mapToSCObject(this.get('layers').toArray(), function(layer) {

            if (self.get('foregroundLayers').contains(layer)) {
                var styleAttribute = layer.get('visible_attributes').firstObject();
                var baseLayerName = "layer_%@_%@".fmt(layer.get('id'), styleAttribute);
                var vectorLayerName = "%@_%@".fmt(baseLayerName, 'vector');
                var rasterLayerName = "%@_%@".fmt(baseLayerName, 'raster');

                // The selection layer is specific to the active user.
                var userId = self.getPath('user.id');
                var selectionLayerName = "layer_%@_%@_%@_selection".fmt(layer.get('id'), styleAttribute, userId);

                var coordString = "/{Z}/{X}/{Y}";
                var tileUrl = "http://%@/footprint/tiles/".fmt(window.location.hostname);
                var vectorUrl = tileUrl + vectorLayerName + coordString + ".geojson";
                var rasterUrl = tileUrl + rasterLayerName + coordString + ".png";
                var selectionUrl = tileUrl + selectionLayerName + coordString + ".geojson";

                var vectorLayer = po.geoJson()
                    .url(vectorUrl)
                    .zoom(function(z){
                        return z;
                    });

                var selectionLayerStyling = self.getPath('stylingLookup.selection_stylist');
                var selectionLayer = po.geoJson()
                    .url(selectionUrl)
                    .zoom(function(z){
                        return z;
                    })
                    .on("load", selectionLayerStyling)
                    .on('show', selectionLayerStyling);

                var rasterLayer = po.image()
                    .url(rasterUrl);

                return [layer.get('db_entity_key'), Footprint.MapLayerGroup.create({
                    map:map,
                    layer: layer,
                    vector: vectorLayer,
                    raster: rasterLayer,
                    selectionLayer: selectionLayer
                })];
            }
            else {
                var db_entity = layer.getPath('db_entity_interest.db_entity');
                var rasterLayer = po.image()
                    .id(layer.get('db_entity_key'))
                    .url(po.url(db_entity.get('url'))
                        .hosts(db_entity.get('hosts')))
                    .visible(layer.get('visible'));
                return [layer.get('db_entity_key'), Footprint.MapLayerGroup.create({
                    map:map,
                    layer: layer,
                    raster: rasterLayer
                })];
            }
        }, this));

        this.get('foregroundLayerKeys').forEach(function(layerKey) {
            var mapLayerGroup = this.get('mapLayerGroups').get(layerKey);

            // Attach styling to configured layers
            var stylist = this.get('stylingLookup').get(mapLayerGroup.getPath('layer.db_entity_key'));
            if (stylist) {
                mapLayerGroup.get('vector')
                    .on('load', stylist)
                    .on('show', stylist);
            }
            // Add all map layers to the map and set their visibility according to the mapLayerGroup's visibility
            mapLayerGroup.setVisibilityBasedOnZoom();
            mapLayerGroup.addLayersToMap();
        }, this);

        this.get('backgroundLayerKeys').forEach(function(layerKey) {
            var mapLayerGroup = this.get('mapLayerGroups').get(layerKey);
            mapLayerGroup.setVisibility();
            mapLayerGroup.addLayersToMap();
        }, this);

        map.add(po.compass(map));
    },

    setDefaultLayerFeatures: function(e) {
        var fields = [];
        if (this.id() == 'base_vector') { fields = new Array('parcel_id', 'pop', 'hh_avg_inc') }
        else if (this.id() == 'canvas_vector') { fields = new Array('parcel_id', 'placetype_id', 'painted') }
    },

    /***
     * Reacts to zooming and movement by showing and hiding the raster or vector layers of visible layer groups
     */
    mapLayersNeedUpdateObserver: function() {
        if (Footprint.mapController.get('mapLayersNeedZoomUpdate') && this.get('mapLayerGroups')) {
            if (this.get('layers') && this.get('foregroundLayerKeys')) {
                this.get('foregroundLayerKeys').forEach(function(layerKey) {
                    var mapLayerGroup = this.get('mapLayerGroups').get(layerKey);
                    mapLayerGroup.setVisibilityBasedOnZoom();
                }, this);
                Footprint.mapController.set('mapLayersNeedZoomUpdate', NO);
            }
        }
    }.observes('Footprint.mapController.mapLayersNeedZoomUpdate', '.mapLayerGroups', '.foregroundLayerKeys')
};

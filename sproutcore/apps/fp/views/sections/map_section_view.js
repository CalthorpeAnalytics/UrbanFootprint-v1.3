sc_require('resources/polymaps');
sc_require('views/presentation/map/polybrush');
sc_require('views/presentation/map/map_layer_group');
sc_require('views/presentation/map/map_controls');
sc_require('views/presentation/map/map_painting');
sc_require('views/presentation/map/map_styling');
sc_require('views/presentation/map/map_tools');
sc_require('views/sections/tool_section_view');

$(function() {
    window.po = org.polymaps;
});

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

Footprint.MapSectionView = SC.View.extend(Footprint.MapControls, Footprint.MapPainting, SC.ActionSupport, {

    classNames: 'footprint-map-section-view'.w(),
    childViews: 'mapView mapToolsView overlayView'.w(),
    icon: sc_static('footprint:images/zoom_to_extent.png'),

    /***
     * The Footprint.ConfigEntity or other mappable instance according to which the map is configured
     */
    content: null,
    contentBinding: SC.Binding.oneWay('Footprint.scenarioActiveController.content'),

    /***
     * All Footprint.Layer instances of the Footprint.ConfigEntity
     */
    layers: null,
    layersBinding: SC.Binding.oneWay('Footprint.layerLibraryActiveController.layers'),

    /***
     * The Footprint.Layer instance of the content which is active
     */
    activeLayerSelection: null,
    activeLayerSelectionBinding: SC.Binding.oneWay('Footprint.layerSelectionActiveController.content'),

    map:null,
    mapBinding: SC.Binding.oneWay('Footprint.mapController.content'),
    activeLayerGroup: null,
    activeLayerGroupBinding: SC.Binding.oneWay('Footprint.mapLayerGroupsController.activeLayerGroup'),

    layerGroup: null,
    layerGroupBinding: SC.Binding.oneWay('Footprint.mapController.content'),

    /***
     * The polymaps map instance attached to the map div element
    */
    createMap: function() {
        var map = po.mcmap()
//            .tileSize({X: 512, Y: 512})
            // Set the map container and add the svg element
            .container(this.get('mapNode').appendChild(po.svg("svg")))
            // Center the map in the middle of the active ConfigEntity and calculate the zoom based on the bounds
            .center(this.get('mapInitialCenter')).extent(this.get('projectExtent')).zoomRange(this.get('mapZoomRange')).zoom(this.get('mapInitialZoom'));

        // Set additional properties on the container
        map.container().setAttribute("id", "map-interface");
        map.container().setAttribute("width", "100%");
        map.container().setAttribute("height", "100%");

        // Create compass
        var compass = po.compass();
        map.add(compass);

        // Enable drag and mouse wheel
        map.add(po.drag(map));
        map.add(po.wheel(map));

        map.on('move', function() {
            Footprint.mapController.refreshMapLayerZoomVisibility()
        });

        // Center to the project bounds
        //this.set('configuredCenter', this.get('mapInitialCenter'));
        this.onProjectActiveControllerStatus();
        Footprint.mapController.set('content', map);
        Footprint.mapController.set('compass', compass);
    },

    /***
     * The current map zoom level
     */
    mapZoom: function () {
        return this.get('map').zoom();
    },

    /***
     * The current center of the map
     */
    mapCenter: function () {
        return this.get('map').center();
    },

    /***
     * The height of the map.
     * @returns {number}
     */
    mapHeight: function () {
        return this.mapNode().clientHeight();
    },
    /***
     * The width of the map
     * @returns {number}
     */
    mapWidth: function () {
        return this.mapNode().clientWidth();
    },

    init: function () {
        sc_super();

        var self = this;
        // add hotkeys for map controls
        Mousetrap.bind('s', function () {
            self.fireAction('doStartSelection');
        }, 'keydown');
        Mousetrap.bind('a', function () {
            self.fireAction('doStartSelection');
        }, 'keydown');
        Mousetrap.bind('esc', function () {
            self.fireAction('doClearSelection');
        }, 'keydown');

        // We set the mapTools here since they depend on the view for the map and to send actions to the view
        Footprint.mapToolsController.set('content', Footprint.MapTools.create({
            mapView: this
        }));
    },

    overlayView: Footprint.OverlayView.extend({
        contentBinding:SC.Binding.oneWay('Footprint.dbEntityInterestsAndLayersController.content'),
        statusBinding:SC.Binding.oneWay('Footprint.dbEntityInterestsAndLayersController.status')
    }),

    mapToolsView: Footprint.ToolSectionView.extend({
       classNames: ['footprint-tool-section-view', 'toolbar'],
       layout: {top: 0, height: 25}
    }),

    mapView: SC.View.extend({
        classNames: 'footprint-map'.w(),
        layout: {left: 0, top: 25, right: 0, bottom: 0},
        readyToCreateMap: NO,
        // We can create the map when the mapController indicates and the project is bound--the latter is needed for extents.
        readyToCreateMapBinding: SC.Binding.and('Footprint.mapController.readyToCreateMap', '.project'),
        /***
         * Create the map after this layer becomes ready
         */
        didCreateLayer: function () {
            SC.Timer.schedule({target: this, action: "afterDelay", interval: 1000})
        },
        afterDelay: function () {
            this.addObserver('readyToCreateMap', this, 'createMap');
            this.parentView.createMap();
        },
        createMap: function() {
            if (this.get('readyToCreateMap')) {
                this.removeObserver('readyToCreateMap', this, 'createMap');
                this.get('parentView').createMap();
            }
        }
    }),


    /***
     * Call this when the activeLayerSelection bounds has been updated to wait for a server update to complete
     * When the activeLayerSelection instance is READY_CLEAN the activeLayerGroup.selectionLayer is reloaded.
     */
    refreshSelectionLayer: function () {
        if (Footprint.mapController.get('selectionLayerNeedsRefresh')) {
            Footprint.mapController.set('selectionLayerNeedsRefresh', NO);
            if (this.get('activeLayerSelection')) {
                // Make this conditional in case the user switched layers in the meantime
                // TODO the target layer should be passed in to prevent this problem
                this.get('activeLayerSelection').addObserver('status', this, 'reloadSelectionLayerWhenReady');
                this.reloadSelectionLayerWhenReady();
            }
        }
    }.observes('Footprint.mapController.selectionLayerNeedsRefresh'),

    reloadSelectionLayerWhenReady: function () {
        if (this.getPath('activeLayerSelection.status') & SC.Record.READY) { // === SC.Record.READY_CLEAN) { LayerSelection problem
            var selectionLayer = this.getPath('activeLayerGroup.selectionLayer')
            if (selectionLayer)
                selectionLayer.reload();
            this.get('activeLayerSelection').removeObserver('status', this, 'reloadSelectionLayerWhenReady');
        }
    },

    project: null,
    projectBinding: SC.Binding.oneWay('*content.parent_config_entity'),
    projectExtent: function() {
        if (this.get('project'))
            return this._polygonBoundingBox(this.getPath('project.bounds.coordinates.firstObject.firstObject'));
    }.property('.project').cacheable(),

    resetExtentToProjectExtent: function () {
        if (Footprint.mapController.get('mapNeedsRezoomToProject')) {
            Footprint.mapController.set('mapNeedsRezoomToProject', NO);
            this.extent(this.get('projectExtent'));
        }
    }.observes('Footprint.mapController.mapNeedsRezoomToProject'),

    layerSelection: null,
    layerSelectionBinding: SC.Binding.oneWay('Footprint.layerSelectionActiveController.content'),
    /***
     * Returns the layerSelection's current extent. This is a single polygon.
     */
    layerSelectionExtent: function() {
        if (this.get('layerSelection'))
            return this._polygonBoundingBox(this.getPath('layerSelection.selection_extent.coordinates.firstObject'));
    }.property('.layerSelection').cacheable(),

    resetExtentToSelectionExtent: function () {
        if (Footprint.mapController.get('mapNeedsRezoomToSelection')) {
            Footprint.mapController.set('mapNeedsRezoomToSelection', NO);
            this.extent(this.get('layerSelectionExtent'));
        }
    }.observes('Footprint.mapController.mapNeedsRezoomToSelection'),


    refreshLayer: function () {
        if (Footprint.mapController.get('layerNeedsRefresh')) {
            Footprint.mapController.set('layerNeedsRefresh', NO);
            if (this.getPath('activeLayerGroup')) {
                this.getPath('activeLayerGroup.raster').reload();
                this.getPath('activeLayerGroup.vector').reload();
            }
        }
    }.observes('Footprint.mapController.layerNeedsRefresh'),


    /***
     * The initial center of the map, calculated based on the bounds of the content
     * For some reason polymaps needs an initial center in order to set extents.
     */
    mapInitialCenter: function() {
        return {lat: 38.5450, lon: -121.7394};
    }.property('content').cacheable(),


    /*
    configuredCenter: null,
    observeConfiguredCenter:function() {
        if (this.get('map') && this.get('configuredCenter')) {
            this.center(this.get('configuredCenter'));
        }
    }.observes('.configuredCenter'),
    */

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
        return [8, 18];
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
     * The DOM element where the map is found (used for dblclick and other browser signals to the map)
     */
    mapWindow: function() {
        return this.get('map').focusableParent();
    }.property('map'),

    /***
     * Reacts to a change in the current project by updating the configuredExtent
     */
    onProjectActiveControllerStatus: function() {
        if (Footprint.projectActiveController.get('status') === SC.Record.READY_CLEAN) {
            this.set('configuredExtent', this.get('projectExtent'));
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


    /***
     * Finds the bounding box for a simple 5 point array of coordinates, where the last point is redundant
     * @param coordinates
     * @returns {Array}
     * @private
     */
    _polygonBoundingBox: function(coordinates) {
        var longitudes = coordinates.map(function(coordinate) { return coordinate[0]});
        longitudes.sort(function(a, b) { return a - b });
        var latitudes = coordinates.map(function(coordinate) { return coordinate[1]});
        latitudes.sort(function(a, b) { return a - b });

        return [{lat:latitudes[0], lon:longitudes[0]},
            {lat:latitudes[latitudes.length - 1], lon:longitudes[longitudes.length - 1]}];
    }
});


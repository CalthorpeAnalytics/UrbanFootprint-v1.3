
 /* 
* UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
* 
* Copyright (C) 2013 Calthorpe Associates
* 
* This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
* 
* This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
* 
* You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
* 
* Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
*/

 /***
  * A lightweight controller for basic map functionality.
  * @type {Class}
  */
Footprint.mapController = SC.ObjectController.create({

    content:null,
    selectionLayerNeedsRefresh: NO,
    refreshSelectionLayer: function() {
        this.set('selectionLayerNeedsRefresh', YES);
    },
    layerNeedsRefresh:NO,
    refreshLayer: function() {
        this.set('layerNeedsRefresh', YES);
    },

    mapNeedsRezoomToProject:NO,
    resetExtentToProject: function(){
        this.set('mapNeedsRezoomToProject', YES);
    },

    mapNeedsRezoomToSelection:NO,
    resetExtentToSelection: function(){
        this.set('mapNeedsRezoomToSelection', YES);
    },

    mapLayersNeedZoomUpdate:NO,
    refreshMapLayerZoomVisibility: function() {
        this.set('mapLayersNeedZoomUpdate', YES);
    },

    readToCreateMap:NO,
    isReady:NO
});

 /***
  * A lightweight controller that manages the map tools properties
  * content is A Footprint.MapTools instance (singleton?) for painting, selection, etc. tools for the map
  * This is setup by the view so that the tools can access the map and send actions to the view
  * @type {Class}
  */
Footprint.mapToolsController = SC.ObjectController.create({

    activeMapToolKey:null,
    /**
     * The active paint tool according to activeMapToolKey
     */
    activePaintTool:null,
    activeMapToolKeyObserver: function() {
        var paintToolName = this.get('activeMapToolKey');
        var paintTool = paintToolName ? this.get(paintToolName) : null;
        if (this.get('activePaintTool') !== paintTool)
            this.set('activePaintTool', paintTool);
    }.observes('.activeMapToolKey')
});

Footprint.mapLayerGroupsController = SC.ObjectController.create({

    map: null,
    mapBinding: SC.Binding.oneWay('Footprint.mapController.content'),

    sortedLayers: null,
    sortedLayersBinding: SC.Binding.oneWay('Footprint.layerCategoriesTreeController.sortedNodes'),

    /***
     * The Footprint.User instance of the logged in user. Map selection layers are user specific, thus the
     * user id is used to form those layer names. In the future when the entire Presentation instance is
     * specific to a user, the user will be extracted from the map Presentation instance.
     */
    user: null,
    userBinding: SC.Binding.single('Footprint.userController.content'),

    /***
     * Non-background layers
     */
    foregroundLayers: function() {
        if (this.get('sortedLayers'))
            return this.get('sortedLayers').filter(function(layer) {
                return !layer.get('tags').mapProperty('tag').contains('background_imagery');
            }, this);
        return [];
    }.property('sortedLayers').cacheable(),

    /***
     * Background layers
     */
    backgroundLayers: function() {
        if (this.get('sortedLayers'))
            return this.get('sortedLayers').filter(function(layer) {
                return layer.get('tags').mapProperty('tag').contains('background_imagery');
            }, this) || [];
        return [];
    }.property('sortedLayers').cacheable(),

    /***
     * Each layer in layers has a unique db_entity_key that is used to identify it in mapLayerGroups
     * This returns all of them
     */
    foregroundLayerKeys: function() {
        if (this.get('foregroundLayers'))
            return this.get('foregroundLayers').mapProperty('db_entity_key');
    }.property('foregroundLayers').cacheable(),

    /***
     * Each layer in layers has a unique db_entity_key that is used to identify it in mapLayerGroups
     * This returns all of them
     */
    backgroundLayerKeys: function() {
        if (this.get('backgroundLayers'))
            return this.get('backgroundLayers').mapProperty('db_entity_key');
    }.property('backgroundLayers').cacheable(),

    /**
     * All layer keys
     */
    layerKeys: function() {
        if (this.get('sortedLayers'))
            return this.get('sortedLayers').mapProperty('db_entity_key');
    }.property('sortedLayers').cacheable(),

    /**
     * The Footprint.Layer instance of the content which is active
     */
    activeLayer: null,
    // This isn't working reliably, don't know why. Setting it in layer_selection_is_ready_state
    //activeLayerBinding: SC.Binding.oneWay('Footprint.layerActiveController.content'),

    /***
     * The activeLayerGroup based on the activeLayer
     * @returns {*}
     */
    activeLayerGroup: function() {
        if (this.getPath('activeLayer.db_entity_key'))
            return this.getPath(this.getPath('activeLayer.db_entity_key'));
    }.property('activeLayer').cacheable(),

    _layerKeys: null,
    _mapLayerGroups: null,
    /***
     * Iterates through the layers of the layers and configures each layer.
     * This is called whenever the layersController's content changes or one of its layers is added, edited,
     * or removed
     * @private
     */
    layersWillChange: function() {
        var map = this.get('map');
        // TODO temporary while I figure out how to wait for divs to size before creating the map
        map.resize();

        /***
         * Remove existing layers.
         */
        map.remove(po.compass(map));
        if (this.get('_mapLayerGroups')) {
            var mapLayerGroups = this.get('_mapLayerGroups');
            (this.get('_layerKeys') || []).forEach(function(layerKey) {
                var mapLayerGroup = mapLayerGroups.get(layerKey);
                if (mapLayerGroup) {
                    mapLayerGroup.get('mapLayerGroupLayers').forEach(function(mapLayerName) {
                        if (mapLayerGroup.get(mapLayerName))
                            map.remove(mapLayerGroup.get(mapLayerName));
                    }, this);
                }
            }, this)
        }
        this.set('_layerKeys', this.get('layerKeys'));
        this.set('content', null);
    },

    /***
     * An SC.Object of Footprint.MapLayerGroup instances, keyed by db_entity_key. Each layerGroup holds a vector, raster,
     * and layer_selection layer corresponding to a Footprint.Layer instance. Footprint.Layer instances are those
     * of the ConfigEntity's configured map Presentation instance.
     */
    updateMapLayerGroups: function() {
        var map = this.get('map');
        // get active layers, create Polymaps objects for them
        // layerGroups are keyed by the DbEntity name
        this.set('content', mapToSCObject(this.get('sortedLayers').toArray(), function(layer) {
            if (this.get('foregroundLayers').contains(layer)) {
                if (!(layer.get('visible_attributes') && layer.getPath('visible_attributes.length') > 0) )
                    return null;
                var styleAttribute = layer.get('visible_attributes').firstObject();
                var baseLayerName = "layer_%@_%@".fmt(layer.get('id'), styleAttribute);
                var vectorLayerName = "%@_%@".fmt(baseLayerName, 'vector');
                var rasterLayerName = "%@_%@".fmt(baseLayerName, 'raster');

                // The selection layer is specific to the active user.
                var userId = this.getPath('user.id');
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

                var selectionLayerStyling = po.stylist().attr('stroke', 'Yellow').attr('fill','Red;').attr('class', 'selected');
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
                    map: map,
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
                    .visible(layer.get('applicationVisible'));
                return [layer.get('db_entity_key'), Footprint.MapLayerGroup.create({
                    map: map,
                    layer: layer,
                    raster: rasterLayer
                })];
            }
        }, this));
        this.set('_mapLayerGroups', this.get('content'));
    },

    mapLayerGroupsDidUpdate: function() {
        (this.get('backgroundLayerKeys') || []).forEach(function(layerKey) {
            var mapLayerGroup = this.get(layerKey);
            mapLayerGroup.setVisibility();
            mapLayerGroup.addLayersToMap();
        }, this);

        (this.get('foregroundLayerKeys') || []).forEach(function(layerKey) {
            var mapLayerGroup = this.get(layerKey);

            if (mapLayerGroup) {
                // Add all map layers to the map and set their visibility according to the mapLayerGroup's visibility
                mapLayerGroup.setVisibilityBasedOnZoom();
                mapLayerGroup.addLayersToMap();
            }
            else {
                logWarning('Layer with key %@ does not have map layers associated with it. Does it have any visible attributes?'.fmt(layerKey) );
            }
        }, this);
        var map = this.get('map');
        if (map)
            map.add(po.compass(map));
    },

    /***
     * Reacts to zooming and movement by showing and hiding the raster or vector layers of visible layer groups
     */
    mapLayersNeedUpdateObserver: function() {
        if (!(Footprint.mapController.get('mapLayersNeedZoomUpdate') && this.get('content')))
            return;

        this.get('foregroundLayerKeys').forEach(function(layerKey) {
            var mapLayerGroup = this.get(layerKey);
            if (mapLayerGroup) {
                mapLayerGroup.setVisibilityBasedOnZoom();
            }
            else {
                logWarning('Layer with key %@ does not have map layers associated with it. Does it have any visible attributes?'.fmt(layerKey) );
            }
        }, this);
        Footprint.mapController.set('mapLayersNeedZoomUpdate', NO);
    }.observes('Footprint.mapController.mapLayersNeedZoomUpdate', '.content')
});


/* 
* UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
* 
* Copyright (C) 2014 Calthorpe Associates
* 
* This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
* 
* This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
* 
* You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
* 
* Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
*/

/**
 * Manages the full lifecycle of polymaps layers and the MapLayerGroup objects that hold
 * them. It also optimizes adding and removing layers from the map.
 *
 * A note on division of labor. This controller takes layer and visible-attribute data
 * as its input from the model/controller layers, and outputs MapLayerGroup objects as
 * output for the view layer. MapLayerGroup objects should be considered view objects,
 * and should not be manipulated except internally here and in the MapView itself. (In
 * fact, presently MapLayerGroup manipulation is split up arbitrarily between this object
 * and the map view; this could be consolidated in the view or here in the controller
 * if desired.)
 */
Footprint.mapLayerGroupsController = SC.Object.create({

    /**
     * The Footprint.Layer instance of the content which is active
     */
    activeLayer: null,
    activeLayerBinding: SC.Binding.oneWay('Footprint.layerActiveController.content'),

    /***
     * The activeLayerGroup based on the activeLayer
     * @returns {*}
     */
    activeLayerGroup: function() {
        var activeLayerKey = this.getPath('activeLayer.db_entity_key');
        if (activeLayerKey)
            return this._cache.get('%@-%@'.fmt(activeLayerKey, this.getPath('activeLayer.visible_attributes.firstObject')));
    }.property('activeLayer').cacheable(),

    refreshLayers: function(layerKeys) {

        layerKeys.forEach(function(layerKey) {
            var layer = F.layersForegroundController.find(function(layer) {
                return layer.get('db_entity_key') == layerKey
            });
            if (layer) {
                var layerGroup = this._cache.get('%@-%@'.fmt(
                    layerKey,
                    layer.getPath('visible_attributes.firstObject')
                ));
                if (layerGroup) {
                    var raster = layerGroup.get('raster');
                    if (raster) raster.reload();
                    var vector = layerGroup.get('vector');
                    if (vector) vector.reload();
                }
            }
        }, this)
    },

    // The private map layer group cache.
    _cache: SC.Object.create(),

    // A cache of the full list of Layers in the current scenario. Used to detect
    // and handle layer deletion.
    _foregroundLayerKeys: [],
    _backgroundLayerKeys: [],

    // Lists the key for every layer group object on this.
    _foregroundLayerGroupKeysByLayer: {},

    // A cached list of visible layer keys.
    _visibleBackgroundMapLayerGroupKeys: [],
    _visibleForegroundMapLayerGroupKeys: [],

    /***
     * Iterates through currently-showing background layers and foreground visible attributes. Creates, adds,
     * removes and destroys MapLayerGroups as needed.
     * 
     * This is called whenever the layersController's content changes or one of its layers is added, edited,
     * or removed.
     * 
     * The particulars of this method's optimizations are informed by the very unfortunate fact that map
     * layers can only be appended at the top of the stack, making simple internal rearranging is impossible.
     */
    updateMapLayerGroups: function() {
        // Background layer groups are stored locally at db_entity_key. Foreground layer
        // groups are stored locally at db_entity_key-visible_attribute_name.

        var map = Footprint.mapController.get('content');

        // Before we do anything, poke the map. (TODO: Temporary while Andy figures out how to wait
        // for divs to size before creating the map)
        map.resize();

        // First, we scan foreground and background layers, removing and destroying the map layer groups
        // for any that no longer exist.
        var currentLayerKeys, layerGroup, layerGroupKeys;
        // background layers: db_entity_key
        currentLayerKeys = F.layersBackgroundController.getEach('db_entity_key');
        if (currentLayerKeys.join() !== this._backgroundLayerKeys.join()) {
            this._backgroundLayerKeys.forEach(function(key) {
                // GATEKEEP: still around.
                if (currentLayerKeys.contains(key)) return;
                layerGroup = this._cache.get(key);
                // GATEKEEP: group never created.
                if (!layerGroup) return;
                layerGroup.removeLayersFromMap(map);
                layerGroup.destroy();
                this._cache.set(key, null);
                this._visibleBackgroundMapLayerGroupKeys.removeObject(key);
            }, this);
            this._backgroundLayerKeys = currentLayerKeys;
        }
        // foreground layers: db_entity_key-visible_attribute
        currentLayerKeys = F.layersForegroundController.getEach('db_entity_key');
        if (currentLayerKeys.join() !== this._foregroundLayerKeys) {
            this._foregroundLayerKeys.forEach(function(layerKey) {
                // GATEKEEP: still around.
                if (currentLayerKeys.contains(layerKey)) return;
                // Get the list of map layer group keys.
                layerGroupKeys = this._foregroundLayerGroupKeysByLayer[layerKey];
                // GATEKEEP: no map layer groups ever created for this layer.
                if (!layerGroupKeys || !layerGroupKeys.length) return;
                layerGroupKeys.forEach(function(key) {
                    layerGroup = this._cache.get(key);
                    layerGroup.removeLayersFromMap(map);
                    layerGroup.destroy();
                    this._cache.set(key, null);
                    this._visibleForegroundMapLayerGroupKeys.removeObject(key);
                }, this);
                delete this._foregroundLayerGroupKeysByLayer[layerKey];
            }, this);
            this._foregroundLayerKeys = currentLayerKeys;
        }

        // With deleted layers taken care of, we move on to compiling the current list of
        // should-be-visible map layer group keys.
        // visible background map layer group keys
        var visibleBackgroundLayers = F.layersVisibleBackgroundController.get('content'),
            visibleBackgroundMapLayerGroupKeys = visibleBackgroundLayers.getEach('db_entity_key') || SC.EMPTY_ARRAY;
        // visible foreground map layer group keys
        var visibleAttributes = F.visibleAttributesController.get('content') || SC.EMPTY_ARRAY,
            visibleForegroundMapLayerGroupKeys = [];
        visibleAttributes.forEach(function(attr) {
            visibleForegroundMapLayerGroupKeys.push('%@-%@'.fmt(attr.getPath('layer.db_entity_key'), attr.get('name')));
        }, this);

        // GATEKEEP: No change in visible keys.
        if (
            visibleBackgroundMapLayerGroupKeys.join() === this._visibleBackgroundMapLayerGroupKeys.join() &&
            visibleForegroundMapLayerGroupKeys.join() === this._visibleForegroundMapLayerGroupKeys.join()
        ) {
            return;
        }

        // Cycle through the background layers, removing items until we have the longest-possible
        // matching stack.
        var i = 0,
            key, compareKey;
        // remove background map layers 
        while (i < this._visibleBackgroundMapLayerGroupKeys.length) {
            key = this._visibleBackgroundMapLayerGroupKeys[i];
            compareKey = visibleBackgroundMapLayerGroupKeys[i];
            // They match! Check the next one.
            if (key === compareKey) {
                i++;
            }
            // They don't match. Remove this one.
            else {
                this._visibleBackgroundMapLayerGroupKeys.removeAt(i);
                layerGroup = this._cache.get(key);
                layerGroup.removeLayersFromMap(map);
            }
        }
        // If necessary, add new background layers. (If any new background layers are added, all
        // foreground layers must be removed.)
        var mapLayerWasAppendedToMap = NO,
            len = visibleBackgroundMapLayerGroupKeys.length;
        for (i; i < len; i++) {
            // If this is our first new layer, we need to do some preparation.
            if (!mapLayerWasAppendedToMap) {
                // Remove the compass.
                map.remove(Footprint.mapController.get('compass'));
                // Remove all foreground map layers.
                this._visibleForegroundMapLayerGroupKeys.forEach(function(foregroundLayerKey) {
                    layerGroup = this._cache.get(foregroundLayerKey);
                    layerGroup.removeLayersFromMap(map);
                }, this);
                // Clear the foreground map layer cache, as it's now useless.
                this._visibleForegroundMapLayerGroupKeys.length = 0;
                // Flag.
                mapLayerWasAppendedToMap = YES;
            }
            // Get the map layer group.
            key = visibleBackgroundMapLayerGroupKeys[i];
            layerGroup = this._cache.get(key);
            // If it's not available yet, create it.
            if (!layerGroup) {
                var layer = visibleBackgroundLayers.objectAt(i),
                    dbEntity = layer.getPath('db_entity_interest.db_entity'),
                    rasterUrl = po.url(dbEntity.get('url')).hosts(dbEntity.get('hosts')),
                    rasterLayer = po.image().id(key).url(rasterUrl);
                layerGroup = Footprint.MapLayerGroup.create({
                    raster: rasterLayer
                });
                this._cache.set(key, layerGroup);
            }
            // Append it to the map.
            layerGroup.addLayersToMap(map);
        }
        // (We're now done with the cached background list; replace it.)
        this._visibleBackgroundMapLayerGroupKeys = visibleBackgroundMapLayerGroupKeys;

        // We now cycle through the cached foreground map layers - if any remain -
        // and give them the same treatment, removing any until we have a longest-
        // possible matched stack, and adding on top.
        i = 0;
        // Remove un-matching map layers...
        while (i < this._visibleForegroundMapLayerGroupKeys.length) {
            key = this._visibleForegroundMapLayerGroupKeys[i];
            compareKey = visibleForegroundMapLayerGroupKeys[i];
            // They match! Check the next one.
            if (key === compareKey) {
                i++;
            }
            // They don't match. Remove this one.
            else {
                this._visibleForegroundMapLayerGroupKeys.removeAt(i);
                layerGroup = this._cache.get(key);
                layerGroup.removeLayersFromMap(map);
            }
        }
        // Append layers...
        len = visibleForegroundMapLayerGroupKeys.length;
        for (i; i < len; i++) {
            // If this is our first new layer, we need to do some preparation.
            if (!mapLayerWasAppendedToMap) {
                // Remove the compass.
                map.remove(Footprint.mapController.get('compass'));
                // Flag.
                mapLayerWasAppendedToMap = YES;
            }
            // Get the map layer group.
            key = visibleForegroundMapLayerGroupKeys[i];
            layerGroup = this._cache.get(key);
            // If it's not available yet, create it.
            if (!layerGroup) {
                var visibleAttribute = visibleAttributes.objectAt(i),
                    visibleAttributeName = visibleAttribute.get('name'),
                    layer = visibleAttribute.get('layer'),
                    layerId = layer.get('id'),
                    baseLayerName = 'layer_%@_%@'.fmt(layerId, visibleAttributeName),
                    vectorLayerName = '%@_%@'.fmt(baseLayerName, 'vector'),
                    rasterLayerName = '%@_%@'.fmt(baseLayerName, 'raster'),
                    userId = Footprint.userController.getPath('firstObject.id'),
                    selectionLayerName = "layer_%@_%@_%@_selection".fmt(layerId, visibleAttributeName, userId),
                    coordString = "/{Z}/{X}/{Y}",
                    tileUrl = "http://%@/footprint/tiles/".fmt(window.location.hostname),
                    vectorUrl = tileUrl + vectorLayerName + coordString + ".geojson",
                    rasterUrl = tileUrl + rasterLayerName + coordString + ".png",
                    selectionUrl = tileUrl + selectionLayerName + coordString + ".geojson",
                    vectorLayer = po.geoJson().url(vectorUrl).zoom(function(z) { return z; }),
                    rasterLayer = po.image().url(rasterUrl),
                    selectionLayerStyling = po.stylist().attr('stroke', 'Yellow').attr('fill','Red;').attr('class', 'selected'),
                    selectionLayer = po.geoJson().url(selectionUrl).zoom(function(z) { return z; }).on('load', selectionLayerStyling).on('show', selectionLayerStyling);
                layerGroup = Footprint.MapLayerGroup.create({
                    vector: vectorLayer,
                    raster: rasterLayer,
                    selectionLayer: selectionLayer
                });
                // Cache & index it.
                var layerKey = layer.get('db_entity_key')
                if (!this._foregroundLayerGroupKeysByLayer[layerKey]) this._foregroundLayerGroupKeysByLayer[layerKey] = [];
                this._foregroundLayerGroupKeysByLayer[layerKey].push(key);
                this._cache.set(key, layerGroup);
            }
            // Append it to the map.
            layerGroup.setVisibilityBasedOnZoom(map);
            layerGroup.addLayersToMap(map);
        }

        // (We're now done with the cached background list; replace it.)
        this._visibleForegroundMapLayerGroupKeys = visibleForegroundMapLayerGroupKeys;

        // If any new layers were appended, we need to add our compass back.
        if (mapLayerWasAppendedToMap) {
            map.add(Footprint.mapController.get('compass'));
        }

        // UPdate the activeLayerGroup property
        this.propertyDidChange('activeLayerGroup')
        // Done!
    },

    /***
     * Clears all layers from the map until the next call to updateMapLayerGroups.
     */
    clearMapLayers: function() {
        var map = Footprint.mapController.get('content');
        this._visibleBackgroundMapLayerGroupKeys.forEach(function(key) {
            var mapLayerGroup = this._cache.get(key);
            mapLayerGroup.removeLayersFromMap(map);
        }, this);
        this._visibleBackgroundMapLayerGroupKeys.length = 0;
        this._visibleForegroundMapLayerGroupKeys.forEach(function(key) {
            var mapLayerGroup = this._cache.get(key);
            mapLayerGroup.removeLayersFromMap(map);
        }, this);
        this._cache = SC.Object.create();
        this._foregroundLayerKeys =[];
        this._backgroundLayerKeys =[];
        this._visibleForegroundMapLayerGroupKeys.length = 0;
    },

    /***
     * Reacts to zooming and movement by showing and hiding the raster or vector layers of visible layer groups
     */
    mapLayersNeedUpdateObserver: function() {
        if (!Footprint.mapController.get('mapLayersNeedZoomUpdate')) return;
        var map = Footprint.mapController.get('content');
        this._visibleForegroundMapLayerGroupKeys.forEach(function(layerKey) {
            var mapLayerGroup = this._cache.get(layerKey);
            mapLayerGroup.setVisibilityBasedOnZoom(map);
        }, this);
        Footprint.mapController.set('mapLayersNeedZoomUpdate', NO);
    }.observes('Footprint.mapController.mapLayersNeedZoomUpdate')
});


/***
 * A configuration of the polymaps layer for a particular Footprint.Layer instance
 * @type {*}
 */
Footprint.MapLayerGroup = SC.Object.extend({

    /** @private
     *  This allows you to specify more map layers on a subclass, if that speaks to you.
     */
    concatenatedProperties: ['layerKeys'],

    /***
     * The attribute names of the three layers in each mapLayerGroup.
     * The vector and selectionLayer are both vector layers, the raster is ... a raster
     * raster and vector are different representations of the underlying geometries, whereas selectionLayer is a subset
     * of the geometries of raster/vector that the user has selected.
     */
    layerKeys: ['raster', 'vector', 'selectionLayer'],

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

    /***
     * Adds this group's map layers to the map.
     */
    addLayersToMap: function(map) {
        this.get('layerKeys').forEach(function(key) {
            var mapLayer = this.get(key);
            if (mapLayer)
                map.add(mapLayer);
        }, this);
    },

    /***
     * Removes this group's map layers from the map.
     */
    removeLayersFromMap: function(map) {
        this.get('layerKeys').forEach(function(key) {
            var mapLayer = this.get(key);
            if (mapLayer) map.remove(mapLayer);
        }, this)
    },

    /***
     * Sets visibility of each mapLayerGroupLayer based on overall visibility and zoom level. If
     * zoom is below the threshold, we use the raster layer; otherwise, we use the vector layer.
     */
    setVisibilityBasedOnZoom: function(map) {
        var zoom = map.zoom(),
            threshold = 19,
            useRaster = zoom < threshold,
            useVector = zoom >= threshold,
            layer;

        layer = this.get('raster');
        if (layer) layer.visible(useRaster);
        layer = this.get('vector');
        if (layer) layer.visible(useVector);
    }
});


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
    visibleBinding:SC.Binding.oneWay('*layer.applicationVisible'),

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
                mapLayer.visible(this.getPath('layer.applicationVisible') && this.visibleAtZoomLevel(name));
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

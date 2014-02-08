/***
 * The state that manages the map panel portion of the application
 * @type {Class}
 */
Footprint.ShowingMapState = SC.State.design({

    /***
     * Fired when a Scenario becomes active and the layers are ready
     * @param context
     */
    layersDidChange: function(context) {
        if (Footprint.mapController.get('isReady')) {
            SC.Timer.schedule({target: this, action: "doProcessLayers", interval: 1000})
        }
        return NO;
    },

    doProcessLayers: function() {
        Footprint.mapLayerGroupsController.layersWillChange();
        Footprint.mapLayerGroupsController.updateMapLayerGroups();
        Footprint.mapLayerGroupsController.mapLayerGroupsDidUpdate();
        this.invokeNext(function() {
            // Once everything is ready, set layer visibility
            Footprint.mapController.set('mapLayersNeedZoomUpdate', YES);
        })
    },

    /***
     * Fired when a Layer becomes active
     * @param context
     */
    layerDidChange: function(context) {
        // Re-enter the selectionHandlerState whenever the active layer changes
        // This will make sure our layerSelection/features loading happens
        // Clear the previous layer's selections
        Footprint.layerSelectionsController.set('content', null);
        // Make sure layerSelectionActiveController is cleared
        this.invokeLast(function() {
            this.gotoState('layerSelectionEditState', context);
        });
        return NO;
    },

    cancelSelection: function(layerContext) {
        // Start over the selectionHandlerState
        this.gotoState('layerSelectionEditState', layerContext);
    },

    /***
     * Activates the pencil (select individual features) tool
     * @param view
     */
    paintPoint: function(view) {
        // Prevent selection from beginning before the layerSelectionActiveController is ready
        // TODO this should be done instead by disabling the selection buttons
        if (Footprint.layerSelectionActiveController.get('status') & SC.Record.READY) {
            Footprint.mapToolsController.set('activeMapToolKey', 'pointbrush');
        }
    },

    /***
     * Activate the select (draw a shape to select) tool
     * @param view
     */
    paintBox: function(view) {
        // Prevent selection from beginning before the layerSelectionActiveController is ready
        // TODO this should be done instead by disabling the selection buttons
        if (Footprint.layerSelectionActiveController.get('status') & SC.Record.READY) {
            Footprint.mapToolsController.set('activeMapToolKey', 'rectanglebrush');
        }
    },

    /***
     * Activate the select (draw a shape to select) tool
     * @param view
     */
    paintPolygon: function(view) {
        // Prevent selection from beginning before the layerSelectionActiveController is ready
        // TODO this should be done instead by disabling the selection buttons
        if (Footprint.layerSelectionActiveController.get('status') & SC.Record.READY) {
            Footprint.mapToolsController.set('activeMapToolKey', 'polybrush');
        }
    },

    navigate: function(view) {
        Footprint.mapToolsController.set('activeMapToolKey', null);
    },

    /***
     * Undo last paint operation
     * @param view
     */
    doPaintUndo: function(view) {
        Footprint.statechart.sendAction('doFeaturesUndo');
    },

    /***
     * Redo last undid operation
     * @param view
     */
    doPaintRedo: function(view) {
        Footprint.statechart.sendAction('doFeaturesRedo');
    },

    /***
     * TODO unimplemented. Revert to the first state in the undo buffer.
     * @param view
     */
    doPaintRevert: function(view) {

    },

    /***
     * Responds to zoomToProjectExtent by calling resetExtentToProject on the mapController
     * @param view
     */
    zoomToProjectExtent: function(view) {
        Footprint.mapController.resetExtentToProject();
    },

    zoomToSelectionExtent: function(view) {
        Footprint.mapController.resetExtentToSelection();
    },

    substatesAreConcurrent: YES,

    // The entry to showingMapState. This is probably a good time to tell the mapController that it's ready
    // to show the maps
    enterState: function() {
        Footprint.mapController.get('readyToCreateMap', YES);
    },

    // All the substates for handling feature selection and updating the selection on the server. This state
    // is always active and ready to accept a new selection drawn or queried by the user (unless the active layerSelection is loading).
    layerSelectionEditState: SC.State.plugin('Footprint.LayerSelectionEditState')
});

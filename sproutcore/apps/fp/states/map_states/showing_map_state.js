/***
 * The state that manages the map panel portion of the application
 * @type {Class}
 */
Footprint.ShowingMapState = SC.State.design({

    /***
     * Fired when a Scenario becomes active and the layers and all of their dependencies are ready
     */
    layerDependenciesDidLoad: function() {
        this.gotoState('layersAreReadyForMapState');
        return NO;
    },

    /***
     * Fired when the user changes the selection or order of visible map layers.
     */
    visibleLayersDidChange: function() {
        this.invokeOnce('doScheduleMapUpdate');
    },

    // If we're ready, and there isn't already a timer ticking, schedule a map update.
    doScheduleMapUpdate: function() {
        if (!Footprint.mapController.get('isReady'))
            // If map or layers are not ready
            return;
        if (!this._updateTimer) {
            this._updateTimer = SC.Timer.schedule({target: this, action: "doProcessLayers", interval: 500})
        }
    },

    doProcessLayers: function() {
        this._updateTimer = null;
        Footprint.mapLayerGroupsController.updateMapLayerGroups();
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
    mapState: SC.State.extend({

        scenariosDidChange: function(context) {
            // Changing projects and scenario is the same to the map for now
            this.scenarioDidChange(context);
            return NO;
        },
        layersDidChange: function(context) {
            return NO;
        },
        scenarioDidChange: function(context) {
            // The map controller is not ready until the layers are ready
            Footprint.mapController.set('readyToCreateMapLayers', NO);
            // Catch a scenario change by leaving going to readyState
            this.gotoState('%@.readyState'.fmt(this.get('fullPath')), context);
            return NO;
        },

        initialSubstate: 'readyState',
        readyState: SC.State,

        enterState: function() {
            Footprint.mapController.setIfChanged('readyToCreateMap', YES);
        },
        exitState: function() {
            // Exit only happens with application unload
            Footprint.mapController.setIfChanged('readyToCreateMap', NO);
        },

        layersAreReadyForMapState: SC.State.extend({
            enterState: function() {
                // If it's our first time loading layers, allow initial map creation to happen
                Footprint.mapController.setIfChanged('readyToCreateMapLayers', YES);
                Footprint.mapLayerGroupsController.clearMapLayers();
                Footprint.statechart.sendAction('doScheduleMapUpdate');
            }
        })
    }),

    // All the substates for handling feature selection and updating the selection on the server. This state
    // is always active and ready to accept a new selection drawn or queried by the user (unless the active layerSelection is loading).
    layerSelectionEditState: SC.State.plugin('Footprint.LayerSelectionEditState')
});

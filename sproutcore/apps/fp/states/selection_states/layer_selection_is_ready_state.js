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
sc_require('controllers/features/feature_controllers');
sc_require('states/record_updating_state');
sc_require('states/selection_states/querying_state');

/***
 * Handles updating a layerSelection instance by drawing bounds or querying
 * The context is always a controller whose content is a layerSelection instance
 * @type {*|RangeObserver|Class|void}
 */
Footprint.LayerSelectionIsReadyState = Footprint.RecordsAreReadyState.extend({


    observer: function(key, value, foo) {
        logWarning(key);
    }.observes('Footprint.layerSelectionEditController.*'),

    recordsDidUpdateEvent: 'layerSelectionDidUpdate',
    recordsDidFailToUpdateEvent: 'layerSelectionDidFailToUpdate',
    updateAction: 'doLayerSelectionUpdate',
    undoAction: 'doLayerSelectionUndo',
    undoAttributes: ['query_strings', 'joins', 'bounds'],

    /***
     * Each layerSelection has an undoManager
     */
    undoManagerProperty: 'undoManager',

    doLayerSelectionUndo: function(context) {
        this.doRecordUndo(context);
    },
    doLayerSelectionRedo: function(context) {
        this.doRecordRedo(context);
    },

    /***
     * Update the layerSelection
     * @param context
     */
    doUpdateLayerSelection: function(context) {
        this.updateRecords(context);
    },

    /***
     * Clears the selection and saves the clear layerSelection to the server
     */
    doClearSelection: function() {
        // Clear the filter unless the modal feature pane is up. This should be moved somewhere called less
        Footprint.statechart.sendAction('doClearQueryAttributes');
        this.clearRecords(self._context);
    },


    /***
     * Creates an update context for layer_selections. Since layer_selections are updated by query form and selecting
     * bounds, this doesn't set any attributes to update.
     */
    updateContext: function(context) {
        var recordContext = SC.ObjectController.create({selectionWantsToEnd:context.get('selectionWantsToEnd')});
        return this.createModifyContext(recordContext, context);
    },

    /***
     * Creates an clear painting context for the selected features and the controller settings.
     */
    clearContext: function(context) {
        var recordContext = SC.ObjectController.create({
            bounds: null,
            query_strings: SC.Object.create({filter_string:null, aggregates_string:null, group_by_string:null}),
            joins: null
        });
        return this.createModifyContext(recordContext, context)
    },

    /***
     * Responds to a PaintTool beginning to draw selection shape on the map.
     * @param view
     */
    doStartSelection: function() {
        this.setBounds();
        // Clear the filter unless the modal feature pane is up. This should be moved somewhere called less
        Footprint.statechart.sendAction('doClearFilterUnlessModal');
    },

    /***
     * Responds to a PaintTool adding a coordinate to its selection shape.
     * The closed geometry of the new shape is assigned to the activeLayerSelection.bounds
     * Commits the selection continually.
     * @param view
     */
    doAddToSelection: function() {
        // Set the bounds to a new SC.Object so that we can observe changes in the UI
        this.setBounds();
        Footprint.statechart.sendAction('doTestSelectionChange', SC.ObjectController.create(
            {content:this._context.get('content'), selectionWantsToEnd:NO})
        );
    },

    /***
     * Responds to a PaintTool ending its selection shape.
     * The closed geometry of the final shape is assigned to the activeLayerSelection.bounds
     * @param view
     */
    doEndSelection: function() {
        // Set the bounds to a new SC.Object so that we can observe changes in the UI
        this.setBounds();
        // Pass the desire to end on the context
        Footprint.statechart.sendAction('doTestSelectionChange', SC.ObjectController.create(
            {content:this._context.get('content'), selectionWantsToEnd:YES})
        );
    },

    // Stores the most recently selected bounds so that when a new doTestSelectionChange happens we
    // can check to see if the bounds actually changed
    _bounds:null,
    _time:null,

    // Triggered by a timer (box) or points (polygon) or whatever. Is
    // also run when entering the state in case the layer selection is already set to something
    doTestSelectionChange: function(context) {
        var time = new Date().getTime();
        // Just do at end for now
        //(NO && time-this._time > 3000) ||
        if (context.get('selectionWantsToEnd')) {
            // If a change occurred since last save (geoms, query doesn't match, etc),
            // and a decent amount of time has passed or the selection wants to end,
            // goto the savingSelectionState substate in order to update the server
            // The context might include a selectionWantsToEnd, which savingSelectionState will handle
            this._time = time;
            this._bounds = context.get('bounds');
            // Save the bounds query
            if (context.get('selectionWantsToEnd')) {
                this._invokeContext = this._invokeContext || context;
                this.invokeOnce('onceUpdateLayerSelection');
            }
        }
    },
    onceUpdateLayerSelection: function() {
        Footprint.statechart.sendAction('doUpdateLayerSelection', this._invokeContext);
        this._invokeContext = null;
    },

    /***
     * Set the bounds to the painted geometry
     * @param bounds
     */
    setBounds: function() {
        if (!Footprint.mapToolsController.get('activePaintTool')) {
            logWarning('No active paint tool. This should not happen');
            return;
        }
        var bounds = SC.Object.create(Footprint.mapToolsController.get('activePaintTool').geometry());
        this._context.set('bounds', bounds);
    },

    /***
     * Execute the query defined in the layerSelection
     * @param context
     */
    doExecuteQuery: function(context) {
        this.gotoState('queryingState', SC.ObjectController.create({content:context.get('content')}));
    },

    /***
     * Open the query window
     * @param view
     */
    doFeatureQuery: function() {
        if (!((this._context.get('status') & SC.Record.READY) &&
            (Footprint.featuresActiveController.getPath('layerStatus') & SC.Record.READY))) {
            logWarning("doFeatureQuery called when dependant controllers were not ready. This should not be possible.");
            return;
        }
        // Trigger the modal state to open the query dialog
        this.statechart.sendAction('doQueryRecords',
            SC.ObjectController.create({
                recordType:Footprint.featuresActiveController.get('recordType'),
                infoPane: 'Footprint.FeatureInfoPane',
                nowShowing:'Footprint.FeatureQueryInfoView',
                recordsEditController:Footprint.featuresEditController
            })
        );
    },

    /***
     * Just clears the bounds without saving
     */
    doClearBounds: function() {
        this.clear(['bounds']);
    },
    /***
     * Just clears the filter without saving
     */
    doClearFilter: function() {
        this.clear(['query_strings.filter_string', 'filter']);
    },

    doClearJoins: function() {
        this.clear(['joins']);
    },

    /***
     * Just clears the aggregate fields without saving
     */
    doClearAggregates: function() {
        this.clear(['query_strings.aggregates_string', 'aggregates']);
    },

    /***
     * Just clears the aggregate fields without saving
     */
    doClearGroupBy: function() {
        this.clear(['query_strings.group_by_string', 'group_bys']);
    },

    /***
     * Clears given layer selection properties
     * @param properties - simple or chained property string
     * @returns {*}
     */
    clear: function(properties) {
        var context = this._context;
        if (context.getPath('store').readStatus(context.get('storeKey')) & SC.Record.BUSY) {
            logWarning("Attempt to clear layerSelection while it is busy");
            return;
        }
        properties.forEach(function(property) {
            context.setPath(property, null);
        });
    },

    // Tell the map controller whenever a new selection layer is ready
    layerSelectionDidUpdate:function(context) {
        Footprint.mapController.refreshSelectionLayer();
        if (context.get('selectionWantsToEnd')) {
            // Send the layerSelection as the context
            Footprint.statechart.sendEvent('selectionDidEnd', context);
        }
        else {
            this.gotoState('%@.readyState'.fmt(this.get('fullPath')), context);
        }
    },

    // Event thrown by substates when they've decided that we're ready to end selecting.
    selectionDidEnd: function(context) {
        // Start over
        this.gotoState(this.get('fullPath'), context);
    },

    layerSelectionDidFailToUpdate: function(context) {
        // If selection wants to end, throw an error message to the user.
        if (context && context.get('selectionWantsToEnd')) {
            SC.AlertPane.error({
                message: 'A selection error occurred',
                description: 'There was an error processing your selection. You can try selecting fewer features.'
            });
        }
        // Make sure all the bindings are correct

        // Either way, run selectionDidUpdate.
        // slight hack... an errored selection behaves the same as an updated selection + error message... so
        // we keep it internal here rather than routing it through an action call.
        this.layerSelectionDidUpdate(context);
    },

    enterState: function(context) {
        this._nestedStore = Footprint.store.chainAutonomousStore();
        this._content = this._nestedStore.materializeRecord(Footprint.layerSelectionActiveController.get('storeKey'));
        this._context = SC.ObjectController.create({content: this._content, selectionWantsToEnd: context.get('selectionWantsToEnd') || NO});
        sc_super()

        Footprint.toolController.set('selectionToolNeedsReset', YES);

        // Use the controller for ease of reference.
        Footprint.layerSelectionEditController.set('content', this._content);

        // No Feature Footprint.featuresActiveController.get('content'))inspection or updating is allowed until we have downloaded the features
        Footprint.toolController.set('featurerIsEnabled', NO);
        // Enable selector tools
        Footprint.toolController.set('selectorIsEnabled', YES);
    },

    /***
     * Override the parent state's readyState to advance us to the selectedFeaturesState whenever there are features
     * in the layerSelection
     */
    readyState: SC.State.extend({
        enterState: function(context) {
            // Clear the features. We will either load them next if there are some in the
            // layer_selection or do nothing
            if (context.getPath('features.length')) {
                // Features selected.
                Footprint.statechart.gotoState('selectedFeaturesState', this._context);
            }
            else {
                // Set it to empty so the query info window shows no results
                Footprint.featuresActiveController.set('content', []);
                // Still go to the featuresAreReadyState so that we can support undo/redo
                this.gotoState('featuresAreReadyState', Footprint.featuresActiveController);
            }
        }
    }),

    exitState: function() {
        if (this._nestedStore)
            this._nestedStore.destroy();
        this._nestedStore = null;
        this._content = null
        Footprint.layerSelectionEditController.set('content', null);
        this._context = null;
    },

    // TODO Overrriding parent version to force action handling
    updatingState: Footprint.RecordUpdatingState.extend({
        doStartSelection: function() {
            this.cancelUpdate();
            return NO;
        },
        doEndSelection: function() {
            this.cancelUpdate();
            return NO;
        },
        doAddToSelection: function() {
            this.cancelUpdate();
            return NO;
        },
        doExecuteQuery: function() {
            this.cancelUpdate();
            return NO;
        },
        doClearSelection: function() {
            this.cancelUpdate();
            return NO;
        },
        doQueryRecords: function() {
            this.cancelUpdate();
            return NO;
        },

        undoActionBinding: SC.Binding.oneWay('.parentState.undoAction'),
        updateActionBinding: SC.Binding.oneWay('.parentState.updateAction'),
        recordsDidUpdateEventBinding: SC.Binding.oneWay('.parentState.recordsDidUpdateEvent'),
        recordsDidFailToUpdateEventBinding: SC.Binding.oneWay('.parentState.recordsDidFailToUpdateEvent'),
        recordsDidUpdate:function() {
            // Do the default stuff
            sc_super();
        }
    }),

    // The state for querying for selections
    queryingState:Footprint.QueryingState.extend({
        queryDidValidate: function(context) {
            // Never send this stuff
            if (Footprint.layerSelectionEditController.getPath("query_string.group_by_string") ^
                Footprint.layerSelectionEditController.getPath("group_by")
            )
                logError('Out of sync state of groupby for layerSelection: %@'.fmt(Footprint.layerSelectionEditController.get('content').toString()))
            if (Footprint.layerSelectionEditController.getPath("query_string.aggregates_string") ^
                Footprint.layerSelectionEditController.getPath("aggregates")
                )
                logError('Out of sync state of aggregates for layerSelection: %@'.fmt(Footprint.layerSelectionEditController.get('content').toString()))
            Footprint.statechart.sendAction('doUpdateLayerSelection', SC.ObjectController.create(context));
        },
        queryDidFail: function(context) {
        }
    }),

    // When a selection is ready, we load the features and then allow the user to edit them (multiple
    // times).
    selectedFeaturesState:SC.State.extend({

        initialSubstate:'loadingFeaturesState',

        enterState: function(context) {
            this._context = context;
        },
        exitState: function() {
            this._context = null;
        },

        /***
         * Load the features stored in the layerSelection
         */
        loadingFeaturesState: Footprint.LoadingState.extend({

            didLoadEvent:'featuresDidLoad',
            loadingController:Footprint.featuresActiveController,
            setLoadingControllerDirectly: NO,

            enterState: function(context) {
                sc_super();
            },

            /***
             * Fetches the features in the Footprint.layerSelectionActive controller via a remote query
             * @returns {*}
             */
            recordArray: function() {
                return Footprint.store.find(SC.Query.create({
                    recordType:Footprint.layerSelectionEditController.getPath('selection_layer.featureRecordType'),
                    location:SC.Query.REMOTE,
                    parameters:{
                        // We use the layer_selection instead of listing all the feature ids, to prevent
                        // overly long URLs
                        layer:Footprint.layerSelectionEditController.get('selection_layer')
                    }
                }));
            },
            featuresDidLoad: function() {
                // Look over all in-flight saves. If any of them include features that overlap with the current set:
                this.gotoState('featuresAreReadyState', Footprint.featuresActiveController);
            }
        }),

        featuresAreReadyState: SC.State.plugin('Footprint.FeaturesAreReadyState')
    })
});

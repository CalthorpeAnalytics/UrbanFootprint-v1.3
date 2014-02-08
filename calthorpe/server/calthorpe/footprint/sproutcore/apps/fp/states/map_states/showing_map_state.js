
sc_require('states/record_updating_state');
sc_require('states/showing_map_state/selecting_bounds_state');
sc_require('states/showing_map_state/querying_state');
sc_require('states/showing_map_state/saving_selection_state');

/***
 * The state that manages the map panel portion of the application
 * @type {Class}
 */
Footprint.ShowingMapState = Footprint.State.design({

    /***
     * Fired when a Layer becomes active
     * @param context
     */
    doViewLayer: function(context) {
        // Disable selector tools
        Footprint.toolController.set('selectorIsEnabled', NO);
        // Re-enter the selectionHandlerState whenever the active layer changes
        // This will make sure our layerSelection/features loading happens
        this.gotoState('selectionHandlerState', context);
        return NO;
    },

    /***
     * Fired when a LayerSelection of the Layer is READY
     * @param context
     */
    doUseLayerSelection: function(context) {
        // Re-enter the selectionHandlerState whenever the active layer changes
        // This will make sure our layerSelection/features loading happens
        this.gotoState('selectionHandlerState', context);
    },

    /***
     * Responds to a PaintTool beginning to draw selection shape on the map.
     * A nested store is created to manage updates the view's activeLayerSelection
     * @param view
     */
    startSelection: function() {
        this.gotoState('selectingBoundsState');
    },

    /***
     * Responds to a PaintTool adding a coordinate to its selection shape.
     * The closed geometry of the new shape is assigned to the activeLayerSelection.bounds
     * Commits the selection continually.
     * @param view
     */
    addToSelection: function() {
        Footprint.statechart.sendAction('doTestSelectionChange', SC.Object.create({
            bounds: Footprint.mapToolsController.get('activePaintTool').geometry()
        }));
    },

    /***
     * Responds to a PaintTool ending its selection shape.
     * The closed geometry of the final shape is assigned to the activeLayerSelection.bounds
     * @param view
     */
    endSelection: function() {
        Footprint.statechart.sendAction('doTestSelectionChange', SC.Object.create({
            selectionWantsToEnd: YES,
            bounds: Footprint.mapToolsController.get('activePaintTool').geometry()
        }));
    },

    doQuerySelection: function(context) {
        this.gotoState('queryingState', context);
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
        if (!Footprint.layerSelectionActiveController.get('featureUndoManager'))
            throw Error("FeatureUndoManager not defined")
        // Calls the undoManager undo which will in turn send an action for the undoState to handle
        Footprint.layerSelectionActiveController.get('featureUndoManager').undo();
    },

    /***
     * Redo last undid operation
     * @param view
     */
    doPaintRedo: function(view) {
        if (!Footprint.layerSelectionActiveController.get('featureUndoManager'))
            throw Error("FeatureUndoManager not defined")
        Footprint.layerSelectionActiveController.get('featureUndoManager').redo()
    },

    /***
     * TODO unimplemented. Revert to the first state in the undo buffer.
     * @param view
     */
    doPaintRevert: function(view) {

    },

    /***
     * Responds to zoomToProjectExtent by calling resetExtent on the mapController
     * @param view
     */
    zoomToProjectExtent: function(view) {
        Footprint.mapController.resetExtent();
    },

    substatesAreConcurrent: YES,

    // The entry to showingMapState. This is probably a good time to tell the mapController that it's ready
    // to show the maps
    enterState: function() {
        Footprint.mapController.set('isReady', YES);
    },

    // All the substates for handling feature selection and updating the selection on the server. This state
    // is always active and ready to accept a new selection drawn or queried by the user (unless the active layerSelection is loading).
    selectionHandlerState: SC.State.extend({

        initialSubstate:'readyState',
        readyState:SC.State,

        /***
         * Query for features
         * TODO I don't know if this is needed
         * @param view
         */
        doFeatureQuery: function(context) {
            if (Footprint.layerSelectionActiveController.get('status') !== SC.Record.READY_CLEAN)
                return;
            this.statechart.sendAction('doQueryRecords',
                SC.Object.create({
                    activeRecord:Footprint.featuresActiveController.get('content'),
                    recordType:Footprint.featuresActiveController.get('activeRecordType')
                })
            );
        },

        /***
         * Clears the selection and saves the clear layerSelection to the server
         */
        doClearSelection: function() {
            Footprint.statechart.gotoState('selectingBoundsState', SC.Object.create({
                selectionWantsToEnd: YES,
                bounds: null
            }));
        },

        /***
         * Called by the undoManager. If the recordType of the context matches, this goes to the undoingState
         * @param context
         */
        doRecordUndo: function(context) {
            if (context.get('recordType').subclassOf(Footprint.Feature)) {
                this.gotoState('undoingState', context);
                return YES;
            }
            return NO;
        },

        /***
         * If a record update fails this handles the event.
         * @param context. This could be used to report what records failed
         */
        updateDidFail: function(context) {
            // Simply return to the readyToUpdateState so that the user can try updating again.
            this.gotoState('readyToUpdateState')
        },

        enterState: function(context) {
            // No Feature Footprint.featuresActiveController.get('content'))inspection or updating is allowed until we have downloaded the features
            Footprint.toolController.set('featurerIsEnabled', NO);

            if (!Footprint.layerSelectionActiveController.get('status') & SC.Record.READY)
                Footprint.statechart.gotoState('noSelectionLayerState');
            else
                // Enable selector tools
                Footprint.toolController.set('selectorIsEnabled', YES);

            if (!Footprint.layerSelectionActiveController.getPath('features.length'))
                // If we have no features in the selection goto the noSelectionState
                Footprint.statechart.gotoState('noSelectionState');
            else
                // Features exist. Goto the selectionIsReadyState which listens for selection updates or
                // the selection wanting to end (e.g. user finishes drawing a shape).
                Footprint.statechart.gotoState('selectionIsReadyState');
        },

        noSelectionLayerState:SC.State.extend({
            enterState: function() {
                Footprint.layerSelectionActiveController.addObserver('status', this, 'layerSelectionStatusDidChange');
            },
            layerSelectionStatusDidChange: function() {
                // Go back up a level and see where we are--either with or without features
                Footprint.statechart.gotoState('selectionHandlerState');
            },
            exitState: function() {
                Footprint.layerSelectionActiveController.removeObserver('status', this, 'layerSelectionStatusDidChange');
            }
        }),


        // If there's no selection, we just hang out and wait for the user to start selecting.
        noSelectionState:SC.State.extend({

            enterState: function() {
                Footprint.toolController.set('featurerIsEnabled', NO);
                // Active features correspond to the selection. No selection means no features
                Footprint.featuresActiveController.setPath('content', null);
            },

            // Listed for the doStartSelection action and goto selectingBoundsState
            doStartSelecting: function() {
                this.gotoState('selectingBoundsState');
            }
        }),

        queryingState:Footprint.QueryingState,


        // While the user is selecting, the statechart may update the server any number of times, including
        // while already mid-update. When the "done selecting" (or "cancel selecting") actions get sent, we
        // have to make sure that the final selection change has been saved before exiting the state.
        selectingBoundsState: Footprint.SelectingBoundsState,

        // When a selection is ready, we load the features and then allow the user to edit them (multiple
        // times).
        selectionIsReadyState:SC.State.extend({

            // The user may start a new selection at any time, meaning any of this state's substates
            // must be able to correctly handle being unexpectedly exited.
            doStartSelecting: function() {
                this.gotoState('selectingBoundsState');
            },

            initialSubstate:'loadingFeaturesState',

            enterState: function() {
                // Create the undoManager if it doesn't yet exist
                var featureUndoManager = Footprint.layerSelectionActiveController.get('featureUndoManager');
                if (!featureUndoManager)
                    Footprint.layerSelectionActiveController.set(
                        'featureUndoManager',
                        SC.UndoManager.create());

                // Create the array of saving Feature sets
                //this.get('savingFeatureSets');
            },

            loadingFeaturesState:Footprint.LoadingState.extend({

                didLoadEvent:'featuresDidLoad',
                loadingController:Footprint.featuresActiveController,

                enterState: function() {
                    // I would check for an empty selection here ... but just out of sheer paranoia. =)
                    // Might also be useful if you wanted to bypass the initial selection check made in
                    // selectionHandlerState.enterState and instead just always go here first. Lots of
                    // valid options.
                    if (!Footprint.layerSelectionActiveController.getPath('features.length')) {
                        this.gotoState('noSelectionState');
                        return;
                    }
                    sc_super();
                },
                /***
                 * Fetches the features in the Footprint.layerSelectionActive controller via a remote query
                 * @returns {*}
                 */
                recordArray: function() {
                    return Footprint.store.find(SC.Query.create({
                        recordType:Footprint.layerSelectionActiveController.getPath('selection_layer.featureRecordType'),
                        location:SC.Query.REMOTE,
                        parameters:{
                            // We use the layer_selection instead of listing all the feature ids, to prevent
                            // overly long URLs
                            layer_selection:Footprint.layerSelectionActiveController.get('content')
                        }
                    }));
                },
                featuresDidLoad: function() {
                    // Look over all in-flight saves. If any of them include features that overlap with the current set:
                    var featureSet = this.getPath('loadingController.content');
                    /*
                    var conflictingFeatureSets = this.getPath('parentState.savingFeatureSets').filter(function(savingFeatureSet) {
                        return savingFeatureSet.filter(function(savingFeature) {
                            return featureSet.contains(savingFeature);
                        }).length > 0
                    });
                    */
                    //if (conflictingFeatureSets.length > 0)
                    //    this.gotoState('notReadyToUpdateState', {conflictingFeatureSets:conflictingFeatureSets});
                    //else
                        this.gotoState('readyToUpdateState');
                }
            }),

            notReadyToUpdateFeaturesState:SC.State.extend({
                enterState: function(context) {
                    this._conflictingFeatureSets = context.conflictingFeatureSets;
                    // Wait until current selection set no longer overlaps with previous in-flight saves.
                    this._conflictingFeatureSets.forEach(function(conflictingFeatureSet) {
                        conflictingFeatureSet.addObserver('status', this, 'conflictingFeatureSetStatusDidChange');
                    })
                },
                conflictingFeatureSetStatusDidChange: function(sender) {
                    if (sender.get('status') & SC.Record.READY) {
                        sender.removeObserver('status', this, 'conflictingFeatureSetStatusDidChange');
                        this._conflictingFeatureSets.remove(sender)
                        if (this._conflictingFeatureSets.length() == 0) {
                            this.gotoState('readyToUpdateState');
                        }
                    }
                },
                exitState: function(context) {
                    // Remove any obserers that aren't already removed
                    this._conflictingFeatureSets.forEach(function(conflictingFeatureSet) {
                        conflictingFeatureSet.removeObserver('status', this, 'conflictingFeatureSetStatusDidChange');
                    });
                    this._conflictingFeatureSets = null;
                }
            })
        }),

        /***
         * Creates an active painting context for the selected features and the controller settings
         */
        activeFeaturePaintingContext: function() {
            var context = SC.Object.create({
                built_form: Footprint.builtFormActiveController.get('content'),
                dev_pct: Footprint.paintingController.get('developmentPercent'),
                density_pct: Footprint.paintingController.get('densityPercent'),
                total_redev: Footprint.paintingController.get('isFullRedevelopment')
            });
            return this._featureContext(context)
        }.property(),

        /***
         * Creates an clear painting context for the selected features and the controller settings.
         */
        clearFeaturePaintingContext: function() {
            var context = SC.Object.create({
                built_form: null,
                dev_pct: 1,
                density_pct: 1,
                total_redev: NO
            });
            return this._featureContext(context)
        }.property(),

        _featureContext: function(context) {
            return SC.Object.create({
                // The undoManager for features of the active layer selection
                undoManager: Footprint.layerSelectionActiveController.get('featureUndoManager'),
                // The same structure as this object but used to undo the features back to their previous state
                undoContext: this.get('undoFeatureContext'),
                // The Feature recordType
                recordType: Footprint.layerActiveController.get('featureRecordType'),
                // An array of each feature to be updated along with the values to update (context)
                // The resulting object is {feature:feature, attributeToUpdate:value, attributeToUpdate:value, ...}
                recordContexts:Footprint.featuresActiveController.map(function(feature) {
                    return SC.Object.create({
                            record:feature
                        },
                        context
                    )
                })
            });
        },

        /***
         * Creates a context for freezing a painting context of the current feature set for undo/redo
         */
        undoFeatureContext: function() {
            return SC.Object.create({
                // The undoManager for features of the active layer selection
                undoManager: Footprint.layerSelectionActiveController.get('featureUndoManager'),
                // The Feature recordType
                recordType: Footprint.layerActiveController.get('featureRecordType'),
                // An array of each feature to be undone along with the values to undo to (context)
                // The resulting object is {feature:feature, attributeToUpdate:value, attributeToUpdate:value, ...}
                recordContexts: Footprint.featuresActiveController.map(function(feature) {
                    return SC.Object.create(
                        {record:feature},
                        // extract the primitive attributes from the record to be target attribute values for undoing
                        $.mapToDictionary(['built_form', 'dev_pct', 'density_pct', 'total_redev'], function(attr) {
                            return [attr, feature.get(attr)];
                        })
                    )
                })
            })
        }.property(),

        readyToUpdateState:SC.State.extend({

            enterState: function() {
                Footprint.toolController.set('featurerIsEnabled', YES);
            },

            /***
             * Handles updating the features via painting
             */
            doPaintApply: function() {
                this.gotoState('updatingState', this.getPath('parentState.activeFeaturePaintingContext'));
            },

            /***
             * Handles clearing the features via painting
             */
            doPaintClear: function() {
                this.gotoState('updatingState', this.getPath('parentState.clearFeaturePaintingContext'));
            },

            /***
             * Identify and/or Edit features
             * @param view
             */
            doFeatureIdentify: function(view) {
                if (Footprint.layerSelectionActiveController.get('status') !== SC.Record.READY_CLEAN)
                    return;
                this.statechart.sendAction('doEditRecord',
                    SC.Object.create({
                        activeRecord:Footprint.featuresActiveController.get('content'),
                        recordType:Footprint.featuresActiveController.get('activeRecordType')
                    })
                );
            }
        }),
        updatingState:Footprint.RecordUpdatingState.extend({
            recordsDidUpdate:function() {
                // Do the default stuff
                sc_super();
                // Clear the selection
                Footprint.statechart.sendAction('doClearSelection');
            }
        }),
        // Undo is the same as update but it doesn't register an undo
        undoingState:Footprint.RecordUpdatingState.extend({
            recordsDidUpdate:function() {
                // Skip sc_super() so we don't register an undo
                // TODO maybe update layerSelection here
                Footprint.statechart.sendAction('doClearSelection');
            }
        })
    })
});

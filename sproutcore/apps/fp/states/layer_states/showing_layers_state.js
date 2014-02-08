sc_require('states/loading_scenario_dependencies_states');

/***
 * The state that manages the projects pane at the top of the application
 * @type {Class}
 */
Footprint.ShowingLayersState = SC.State.design({

    layerDidChange: function(context) {
        // Let this propagate through to other listeners
        return NO;
    },
    layersDidChange: function(context) {
        this.gotoState('layersAreReadyState', context)
    },

    /***
     * Sets the value property of the view to hidden if visible or visible if hidden
     * The value property is bound to some kind of visibility property of a model instance.
     * For instance visibilityView of LayerLibraryView has its value bound to '.parentView*content.visibility'
     * @param view
     */
    visibleAction: function(view) {
        Footprint.layerLibraryActiveController.set('solos', []);
        if (view.get('value') == Footprint.VISIBLE) {
            // hide if visible
            view.set('value', Footprint.HIDDEN);
        }
        else {
            // show if hidden
            view.set('value', Footprint.VISIBLE);
        }
    },

    initialSubstate: 'readyState',

    readyState: SC.State.extend({
        enterState: function() {
            // If already ready proceed, otherwise hang out here.
            if ([SC.Record.READY_CLEAN, SC.Record.READY_DIRTY].contains(Footprint.layersController.get('status'))) {
                this.gotoState('layersAreReadyState', Footprint.scenariosController);
            }
        },

        layerDidChange: function(context) {
            // Let the showing_map_state react too
            return NO;
        },

        doExportRecord: function(context) {
            if (context.get('content')) {
                var record = context.get('content');

                if (record.kindOf(Footprint.PresentationMedium)) {
                    var layer_id = context.get('content').get('id');
                    var api_key = Footprint.userController.getPath('content.firstObject.api_key');
                    var export_request = SC.Request.getUrl("/footprint/%@/export_layer/%@/".fmt(api_key, layer_id));
                    export_request.send();
                    alert("Exporting the currently selected layer - it will start downloading as soon as it is ready. \n\n " +
                        "Please do not close your UrbanFootprint session.");
                    return YES;
                }
                return NO;
            }
        },

        layersAreReadyState: Footprint.RecordsAreReadyState.extend({
            recordsDidUpdateEvent: 'layersDidUpdate',
            recordsDidFailToUpdateEvent: 'layersDidFailToUpdate',
            updateAction: 'doLayerUpdate',
            undoAction: 'doLayerUndo',
            undoAttributes: ['name', 'year', 'description'],
            crudParams: function() {
                // We need an existing layer to use as a template (for now)
                var template = Footprint.layersEditController.getPath('selection.firstObject');
                if (!template || template.get('id') < 0)
                    template = Footprint.layersEditController.filter(function(layer) { return layer.get('id') > 0 })[0];
                return {
                    infoPane: 'Footprint.LayerInfoPane',
                    recordType: Footprint.Layer,
                    recordsEditController: Footprint.layersEditController,
                    content:template
                };
            }.property().cacheable(),

            doCreateLayer: function() {
                Footprint.statechart.sendAction('doCreateRecord', this.get('crudParams'));
            },
            doCloneLayer: function() {
                Footprint.statechart.sendAction('doCloneRecord', this.get('crudParams'));
            },
            doCreateLayerFromSelection: function() {
                Footprint.statechart.sendAction('doCloneRecord', this.get('crudParams'));
            },
            doUpdateLayer: function() {
                Footprint.statechart.sendAction('doUpdateRecord', this.get('crudParams'));
            },
            doViewLayer: function() {
                Footprint.statechart.sendAction('doViewRecord', this.get('crudParams'));
            },

            // Layers are always created with a dbEntity, which is the more fundamental
            // record to the server. So we listen for socketIO updates about the dbEntity
            // save and post-save process
            postSaveDbEntityPublisherCompleted: function(context) {
                var combinedContext = toArrayController(context, {
                    keyPath:'db_entity_key',
                    postProcessingDidEnd: function(context) {
                        var parentStore = context.getPath('content.store.parentStore');
                        var store = context.getPath('content.store');
                        var records = Footprint.store.find(SC.Query.local(
                            Footprint.Scenario, {
                                conditions: 'id = {id}',
                                id: context.getPath('content.presentation.config_entity.id')
                            }
                        ));
                        store.get('parentStore').refreshRecords(
                            records.mapProperty('constructor'),
                            records.mapProperty('id'),
                            records.mapProperty('storeKey'),
                            function() {
                                // Sync the store to the updated parent store
                                store.reset();
                            }
                        );
                        records = [context.get('content')];
                        store.get('parentStore').refreshRecords(
                            records.mapProperty('constructor'),
                            records.mapProperty('id'),
                            records.mapProperty('storeKey')
                        );
                    }});
                Footprint.statechart.sendAction('doUpdateSaveProgress', combinedContext);
            },

            postSaveDbEntityPublisherFailed: function(context) {
                // The context (nee the socket event) gives us enough information to
                // get the DbEntityInterest. From there, we can query the corresponding
                // failed layer.
                if (context.get('class_name') !== 'DbEntityInterest') return NO;
                var failedRecord = F.store.find(F.DbEntityInterest, context.get('id')),
                    failedLayer = F.store.find(SC.Query.local(F.Layer, {
                        conditions: 'db_entity_interest = %@',
                        parameters: [failedRecord]
                    })).firstObject();
                if (!failedLayer) return NO;
                var failedLayerName = failedLayer.get('name'),
                    layerLibrary = failedLayer.get('presentation'),
                    layerLibraryStatus = layerLibrary.get('status');
                // Delete the failed layer, and remove it from its LayerLibrary.
                failedRecord.destroy();
                failedLayer.destroy();
                layerLibrary.get('layers').removeObject(failedLayer);
                F.store.writeStatus(layerLibrary.get('storeKey'), layerLibraryStatus);
                // Show an alert.
                SC.AlertPane.warn({
                    message: 'Layer Creation Failed',
                    description: 'There was an error processing "%@". Please try again, and if this continues, please report to your system administrator.'.loc(failedLayerName)
                });
                return NO;
            },

            enterState: function(context) {
                this._nestedStore = Footprint.store.chainAutonomousStore();
                this._content = this._nestedStore.find(SC.Query.local(
                    Footprint.Layer, {
                        conditions: '{storeKeys} CONTAINS storeKey',
                        storeKeys:context.mapProperty('storeKey')
                    })).toArray();
                this._context = SC.ArrayController.create({content: this._content, recordType:context.get('recordType')});
                Footprint.layersEditController.set('content', this._context.get('content'));
                sc_super();
            },

            /***
             *
             * The undoManager property on each layer
             */
            undoManagerProperty: 'undoManager',

            updateContext: function(context) {
                var recordCntext = SC.ObjectController.create();
                return this.createModifyContext(recordContext, context)
            }
        })
    }),

    errorState: SC.State.extend({
        enterState: function() {

        }
    })
});

sc_require('states/loading_scenario_dependencies_states');

/***
 * The state that manages the projects pane at the top of the application
 * @type {Class}
 */
Footprint.ShowingLayersState = SC.State.design({

    scenarioDidChange: function(context) {
        // Start over and wait for layers to load
        this.gotoState(this.readyState, context)
        return NO;
    },

    layersDidChange: function(context) {
        Footprint.layerCategoriesTreeController.deselectObjects(
            Footprint.layerCategoriesTreeController.get('selection')
        );
        Footprint.layerCategoriesTreeController.updateSelectionAfterContentChange();
        this.gotoState(this.loadingLayerDependenciesState, context);
        return NO;
    },

    initialSubstate: 'readyState',
    readyState: SC.State,

    loadingLayerDependenciesState: SC.State.extend({
        initialSubstate:'loadingDbEntityDependenciesState',

        /***
         * Force all child records to load before proceeding to recordsAreReadyState
         * We need to load the feature_behavior instances of each db_entity
         */
        loadingDbEntityDependenciesState: Footprint.LoadingState.extend({
            didLoadEvent: 'didLoadDbEntityInterests',
            checkRecordStatuses: YES,
            recordArray:function() {
                return Footprint.layersController.mapProperty('db_entity_interest');
            },
            didLoadDbEntityInterests: function() {
                this.gotoState('layersAreReadyState', this._context);
                // Now the layers are ready
                Footprint.statechart.sendEvent('layerDependenciesDidLoad', this._context);
            }
        })
    }),

    layersAreReadyState: Footprint.RecordsAreReadyState.extend({
        // DbEntityInterest is the main recordType being edited. Layers are just the veneer
        baseRecordType: Footprint.DbEntityInterest,
        _resolveContextRecord: function(context) {
            return context.getPath('content.firstObject.db_entity_interest');
        },
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
            }
            return NO;
        },

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

        /***
         * Handles picking a behavior from selector. Results in updating the FeatureBehavior behavior
         * @param context
         * @returns {window.NO|*}
         */
        doPickBehavior: function(context) {
            // Our context is the SourceListView from which the user selected an item
            var behavior = context.getPath('selection.firstObject');
            if (!behavior)
                return;
            var containerLayer = Footprint.layersEditController.getPath('selection.firstObject');
            var featureBehavior = containerLayer.getPath('db_entity_interest.db_entity.feature_behavior');

            // This should never happen, but does
            if (!featureBehavior.get('parentRecord')) {
                logWarning("featureBehavior had no parent! Can't write to it");
                return;
            }

            featureBehavior.setIfChanged('behavior', behavior);
            featureBehavior.setIfChanged('intersection', behavior.get('intersection'));

            if (!containerLayer.getPath('db_entity_interest.db_entity.feature_behavior')) {
                logWarning("featureBehavior had no parent! Can't write to it");
                return;
            }

            containerLayer.setPath('db_entity_interest.db_entity.feature_behavior.behavior', behavior);
        },

        /***
         * Handles picking a tag from the tag selector.
         * @param context
         * @returns {window.NO|*}
         */
        doPickTag: function(context) {
            // Our context is the SourceListView from which the user selected an item
            var tagToAdd = context.getPath('selection.firstObject');
            if (!tagToAdd)
                return;
            var containerLayer = Footprint.layersEditController.getPath('selection.firstObject');
            var tags = containerLayer.getPath('db_entity_interest.db_entity.feature_behavior.tags');
            tags.pushObject(tagToAdd);
        },
        /***
         * add a new tag to the current feature_behavior.tags list. Validation to prevent duplicates should already
         * @param context
         */
        doAddTag: function(context) {
            var value = context.get('value');
            // Check if the tag already exists
            var tagToAdd = Footprint.behaviorTagsEditController.find(function(tag) {
                return tag.get('tag') == value;
            });
            var containerLayer = Footprint.layersEditController.getPath('selection.firstObject');
            var tags = containerLayer.getPath('db_entity_interest.db_entity.feature_behavior.tags');
            if (tagToAdd) {
                // Add the tag to the list if it's not already there
                tags.pushObject(tagToAdd);
            }
            else {
                tags.createNestedRecord({
                    tag:value
                });
            }
        },

        // --------------------------
        // Post-processing
        //

       /***
        * Update the layerLibrary of the layer to insert or remove the layer if needed
        * @param layer
        * @param layerLibrary
        */
        _updateLayerLibrary: function (layer, layerLibrary) {
            var masterRecord = F.store.materializeRecord(layer.get('storeKey'));
            if (masterRecord.get('status') & SC.Record.DESTROYED || masterRecord.get('deleted')) {
                layerLibrary.get('layers').removeObject(masterRecord);
            }
            else {
                if (!layerLibrary.get('layers').contains(masterRecord)) {
                    layerLibrary.get('layers').pushObject(masterRecord);
                }
            }
        },

        /***
         * Override to add the layer to the layerLibrary
         * @param context
        */
        crudDidFinish: function(context) {
            var handled = sc_super();
            if (!handled)
                return;

            // In the case of a layer, we need to ensure that its layer
            // library has been updated. This happens automatically and
            // deterministically on the server, so this saves us a round
            // trip.
            var layerLibrary = F.store.materializeRecord(context.getPath('content.firstObject.presentation.storeKey')),
                layerLibraryStatus = layerLibrary.get('status');
            context.get('content').forEach(function(record) {
                this._updateLayerLibrary(record, layerLibrary);
            }, this);
            // Restore the layerLibrary status, presumably to READY_CLEAN
            F.store.writeStatus(layerLibrary.get('storeKey'), layerLibraryStatus);
        },

        /***
         * Refreshes the layer since it will pick up new attributes during post save
         * @param context
         */
        postSavePublishingFinished: function(context) {
            // Handle anything DbEntityInterest-related here
            // Send this event for analysis tools
            Footprint.statechart.sendEvent('dbEntityInterestDidUpdate', context);
        },

        // Override
        postSavePublisherProportionCompleted: function(context) {
            // Call the base method to check for DbEntityInterest, then check for the Layer recordType below
            if (sc_super())
                return YES;

            var eventHandler = function() {
                var recordType = SC.objectForPropertyPath('Footprint.%@'.fmt(context.get('class_name')));
                if (!recordType.kindOf(Footprint.Layer)) {
                    SC.Logger.debug("Not handled");
                    return NO;
                }
                // Post save layer publishing only has one signal, indicating completion.
                var layer = Footprint.store.find(SC.Query.local(Footprint.Layer, {
                    // Use $ to compare ids since the layer's version is nested and
                    // the incoming is not, so they won't share storeKeys
                    conditions: 'id = %@',
                    parameters: [context.get('id')]
                })).firstObject();

                if (layer) {
                    // This is the layer that was just created/updated
                    this.commitConflictingNestedStores([layer]);
                    layer.refresh();
                    Footprint.mapLayerGroupsController.refreshLayers([layer.get('db_entity_key')]);
                }
                else {
                    // This layer was just created/updated for another scenario because the main
                    // layer was created at project scope. Load the layer remotely to get it in the store.
                    var layerQuery = Footprint.store.find(SC.Query.create({
                        recordType:Footprint.Layer,
                        location:SC.Query.REMOTE,
                        parameters:{
                            // We use the layer_selection instead of listing all the feature ids, to prevent
                            // overly long URLs
                            id:context.get('id')
                        }
                    }));
                    layerQuery.addObserver('status', this, 'layerQueryStatusDidChange')
                }
            };
            if (this._crudFinished)
                // Run the handler immediately if CRUD is already finished
                eventHandler.apply(this);
            else
                // Queue it up
                this._eventHandlerQueue.pushObject(eventHandler);
            return YES
        },

        layerQueryStatusDidChange: function(layerQuery) {
            if (layerQuery.get('status') === SC.Record.READY_CLEAN) {
                var layer = layerQuery.get('firstObject');
                var layerLibrary = F.store.materializeRecord(layer.getPath('presentation.storeKey'));
                if (layerLibrary.get('status') & SC.Record.READY) {
                    // If the LayerLibrary already in the store, update it. Otherwise do nothing.
                    this._updateLayerLibrary(layer, layerLibrary);
                }
            }
        },

        postSavePublishingFailed: function(context) {
            // Override the parent class
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
            var nestedStore = F.statechart.getState('showingAppState.crudState.modalState')._nestedStore
            if (nestedStore && nestedStore.locks[layer.get('storeKey')])
                nestedStore.commitChanges();
            failedRecord.destroy();
            failedLayer.destroy();
            layerLibrary.get('layers').removeObject(failedLayer);
            F.store.writeStatus(layerLibrary.get('storeKey'), layerLibraryStatus);
            // Show an alert.
            SC.AlertPane.warn({
                message: 'Layer Creation Failed',
                description: 'There was an error processing "%@". Please try again, and if this continues, please report to your system administrator.'.loc(failedLayerName)
            });
            this._postSavePublisherFailed(context);
            return YES;
        },

        // Internal support
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
        existState: function() {
            this._nestedStore.destroy();
            this._nestedStore = null;
            sc_super();
        },

        /***
         *
         * The undoManager property on each layer
         */
        undoManagerProperty: 'undoManager',

        updateContext: function(context) {
            var recordContext = SC.ObjectController.create();
            return this.createModifyContext(recordContext, context)
        }
    }),

    errorState: SC.State.extend({
        enterState: function() {

        }
    })
});

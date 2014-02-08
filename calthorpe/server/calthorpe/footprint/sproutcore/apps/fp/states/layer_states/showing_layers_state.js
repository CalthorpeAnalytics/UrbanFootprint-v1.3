/***
 * The state that manages the projects pane at the top of the application
 * @type {Class}
 */
Footprint.ShowingLayersState = Footprint.State.design({

    /***
     * Sets the value property of the view to solo if not solo or back to its previous property (visible or hidden) if solo
     * It also adds the view's content property to the Footprint.layerLibraryActiveController.solos array if soloing or clears that array if unsoloing
     * The value property is bound to some kind of visibility property of a model instance.
     * For instance visibilityView of LayerLibraryView has its value bound to '.parentView*content.visibility'
     * The view's content property should be bound to the content, such as '.parentView*content'
     * @param view
     */
    soloAction: function(view) {
        logProperty(view.get('value'), '%@.value'.fmt(view.toString()), '%@.soloAction'.fmt(this.toString()));
        if (view.get('value') == Footprint.SOLO) {
            // If already soloing, disable soloing by setting the view back to its pre-solo visible value
            view.set('value', view.get('visible') );
            // Clear the controller's solos property
            Footprint.layerLibraryActiveController.set('solos', [])
        }
        else {
            view.set('value', Footprint.SOLO);
            // Start soloing. Tell the controller so that other items are hidden. This could support multiple "soloists" in the future
            Footprint.layerLibraryActiveController.set('solos', [view.get('content')])
        }
    },

    /***
     * Sets the value property of the view to hidden if visible or visible if hidden
     * The value property is bound to some kind of visibility property of a model instance.
     * For instance visibilityView of LayerLibraryView has its value bound to '.parentView*content.visibility'
     * @param view
     */
    visibleAction: function(view) {
        logProperty(view.get('value'), '%@.value'.fmt(view.toString()), '%@.visibleAction'.fmt(this.toString()));
        // Clear all solos
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

    substatesAreConcurrent:YES,

    /***
     * Fired when a Scenario becomes active
     * @param context
     */
    doViewLayers: function() {
        Footprint.layerSelectionsController.set('content', null);
    },

    doViewLayer: function(context) {
        this.gotoState('showingActiveLayerState', context);
        return NO;
    },

    doExportRecord: function(context) {
        if (context.get('activeRecord')) {
            var record = context.get('activeRecord');

        if (record.kindOf(Footprint.PresentationMedium)) {
            var layer_id = context.get('activeRecord').get('id');
            var api_key = Footprint.userController.getPath('content.firstObject.api_key');
            var export_request = SC.Request.getUrl("%@/export_layer/%@/".fmt(api_key, layer_id));
            export_request.send();
            alert("Exporting the currently selected layer - it will start downloading as soon as it is ready. \n\n " +
                "Please do not close your UrbanFootprint session.");
            return YES;
        }
        return NO;
    }
    },

    editingState:Footprint.EditInfoState.extend({
        editPanePath:'layerInfoView', // TODO doesn't yet exist as class
        editController:Footprint.layerEditController
    }),

    showingActiveLayerState: SC.State.extend({

        // Whenever we re-enter this state (when the selected Scenario changes) load the Scenario layerSelections
        initialSubstate: 'loadingLayerSelectionsState',

        /***
         * Load the LayerSelection instances of the active Scenario
         */
        loadingLayerSelectionsState: Footprint.LoadingState.extend({
            recordType:Footprint.LayerSelection,
            loadingController: Footprint.layerSelectionsController,
            didLoadEvent:'layerSelectionsControllerIsReady',
            didFailEvent:'layerSelectionsControllerDidFail',

            delayedLoad: function() {
                var loadingController = this.get('loadingController');
                loadingController.set('content', this.recordArray());
            },

            // # Hack to slow loading of layer_selections to avoid db deadlock
            enterState: function(context) {
                this._layer = context && context.get('content');
                var loadingController = this.get('loadingController');
                var listController = this.get('listController');
                // Don't observe until we enter the state
                loadingController.addObserver('status', this, 'loadingControllerStatusDidChange');

                // Need to fetch the content
                SC.Timer.schedule({
                    target: this, action: 'delayedLoad', interval: 200
                });

                // Call the observer immediately in case the content is already ready
                this.loadingControllerStatusDidChange();
            },

            recordArray:function() {
                // TODO there's no need to load the LayerSections every time we enter the state
                // They should be cached once loaded--it's unlikely they will be updated outside this app in the meantime
                //var configEntity = Footprint.scenarioActiveController.get('content');
                var layer = this._layer;
                if (layer) {
                    return Footprint.store.find(SC.Query.create({
                        recordType: this.get('recordType'),
                        location: SC.Query.REMOTE,
                        parameters: {
                            layer:layer
                        }
                    }));
                }
            }
        }),

        layerSelectionsControllerIsReady:function() {
            this.gotoState('loadingLayerSelectionsState.readyState');
        },

        readyState: SC.State,

        exitState: function() {
        }
    })
});

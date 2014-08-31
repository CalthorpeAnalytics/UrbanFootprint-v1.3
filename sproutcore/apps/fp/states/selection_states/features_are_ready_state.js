/***
 * Updates features
 * @type {*|RangeObserver|Class|void}
 */
Footprint.FeaturesAreReadyState = Footprint.RecordsAreReadyState.extend({

    baseRecordType: Footprint.Feature,
    recordsDidUpdateEvent: 'featuresDidUpdate',
    recordsDidFailToUpdateEvent: 'featuresDidFailToUpdate',
    updateAction: 'doFeaturesUpdate',
    undoAction: 'doFeaturesUndo',
    // TODO these are just the attributes we update when painting.
    // Obviously if editing full features is enabled, more attributes have to be undoable
    // In that case its probably easiest to know all attributes and try to undo all of them.
    undoAttributes: ['built_form', 'dev_pct', 'density_pct', 'clear_base_flag', 'gross_net_pct', 'redevelopment_flag'],
    /***
     *
     * The undoManager for the features of the current layerSelection
     */
    undoManagerController: Footprint.layerSelectionActiveController,
    undoManagerProperty: 'featureUndoManager',

    doFeaturesUpdate: function(context) {
        this.updateRecords(context);
    },

    doFeaturesUndo: function(context) {
        this.doRecordUndo(context);
    },
    doFeaturesRedo: function(context) {
        this.doRecordRedo(context);
    },

    featuresDidUpdate: function(context) {
        Footprint.statechart.sendAction('doClearSelection', Footprint.layerSelectionEditController);
    },

    /***
     * Responds to identify by calling doQueryRecords
     */
    doFeatureIdentify: function() {
        // Trigger the modal state to open the query dialog
        this.statechart.sendAction('doQueryRecords',
            SC.ObjectController.create({
                recordType:Footprint.featuresActiveController.get('recordType'),
                infoPane: 'Footprint.FeatureInfoPane',
                nowShowing:'Footprint.FeatureSummaryInfoView',
                recordsEditController:Footprint.featuresEditController
            })
        );
    },

    /***
     * Handles updating the features via painting
     */
    doPaintApply: function() {
        this.updateRecords();
    },

    /***
     * Handles clearing the features
     */
    doPaintClear: function() {
        this.clearRecords();
    },

    enterState: function(context) {
        this._nestedStore = Footprint.store.chainAutonomousStore();
        if (context.get('length') > 0) {
            // When there are features we loaded the nested store versions
            this._content = this._nestedStore.find(SC.Query.local(
                    context.get('recordType'), {
                    conditions: '{storeKeys} CONTAINS storeKey',
                    storeKeys:context.mapProperty('storeKey')
                }));
            // Enable the info, apply, clear, etc buttons
            Footprint.toolController.set('featurerIsEnabled', YES);
        }
        else {
            // If no features, we are just here to support undo/redo
            this._content = [];
        }
        this._context = SC.ArrayController.create({content: this._content, recordType: context.get('recordType'), layer: context.get('layer')});
        Footprint.featuresEditController.set('content', this._context.get('content'));
        sc_super()
    },

    exitState: function() {
        this._nestedStore.destroy();
        this._neetedStore = null;
    },

    /***
     * Creates an active painting context for the selected features and the controller settings
     */
    updateContext: function(context) {
        var recordContext = SC.ObjectController.create({
            built_form: Footprint.builtFormActiveController.get('content'),
            dev_pct: Footprint.paintingController.get('developmentPercent'),
            density_pct: Footprint.paintingController.get('densityPercent'),
            clear_base_flag: Footprint.paintingController.get('isClearBase'),
            redevelopment_flag: Footprint.paintingController.get('isRedevelopment'),
            gross_net_pct: Footprint.paintingController.get('grossNetPercent')
        });
        return this.createModifyContext(recordContext, context);
    },

    /***
     * Creates an clear painting context for the selected features and the controller settings.
     */
    clearContext: function() {
        var recordContext = SC.ObjectController.create({
            built_form: null,
            dev_pct: 1,
            density_pct: 1,
            gross_net_pct: 1,
            clear_base_flag: NO,
            redevelopment_flag: NO
        });
        return this.createModifyContext(recordContext,
            this._context || SC.ObjectController.create({content:this._content}));
    }
});

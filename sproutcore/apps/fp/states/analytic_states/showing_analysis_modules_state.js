/***
 * The state that manages the projects pane at the top of the application
 * @type {Class}
 */
Footprint.ShowingAnalysisModulesState = SC.State.design({

    initialSubstate: 'analysisModulesPrepareState',

    scenarioDidChange: function() {
        // Hack to close the crud_state on scenario switch. This allows the nestedStore
        // to be reset on the recordsEditController, which we require to load the new analysis_modules locally
        Footprint.analysisModulesController.set('content', null);
        this.gotoState(this.analysisModulesPrepareState);
        return NO;
    },

    analysisModulesPrepareState: SC.State.plugin('Footprint.AnalysisModulesPrepareState'),

    analysisModulesAreReadyState: Footprint.RecordsAreReadyState.extend({
        baseRecordType: Footprint.AnalysisModule,
        recordsDidUpdateEvent: 'analysisModulesDidUpdate',
        recordsDidFailToUpdateEvent: 'analysisModulesDidFailToUpdate',
        updateAction: 'doAnalysisModuleUpdate',
        undoAction: 'doAnalysisModuleUndo',
        crudParams: function() {
            return {
                recordType: Footprint.AnalysisModule,
                recordsEditController: Footprint.analysisModulesEditController
            };
        }.property().cacheable(),

        doUpdateAnalysisModule: function(context) {
            // We need to explicitly make the active analysisModule dirty to get save to work
            changeRecordStatus(
                Footprint.analysisModulesEditController.get('nestedStore'),
                Footprint.analysisModulesEditController.getPath('selection.firstObject'),
                SC.Record.READY_CLEAN,
                SC.Record.READY_DIRTY);

            this.updateRecords($.extend(
                this.get('crudParams'),
                {content:Footprint.analysisModulesEditController.getPath('selection.firstObject')}));
        },
        // Post-processing
        //

        // Override success message. We return null for the core to suppress the message on painting
        successMessage: function(context) {
            if (['core', 'agriculture'].contains(context.get('key')))
                return null;
            var recordType = context.get('recordType');
            return "Successfully completed %@ Module".fmt(context.get('key').capitalize());
        },
        failureMessage: function(context) {
            var recordType = context.get('recordType');
            return "Failed to run analysis %@ Module".fmt(context.get('key').capitalize());
        },

        postSavePublishingFinished: function(context) {
            var analysisModule = context.get('record');
            if (['core', 'agriculture'].contains(context.get('key'))) {
                // TODO we still react to core differently than the other modules. It will all coalesce soon
                var scenarios = Footprint.scenariosController.filter(function(scenario) {
                    return scenario.get('id')==context.get('config_entity_id');
                });

                scenarios.forEach(function(scenario) {
                    SC.Logger.debug('Core Complete for Scenario: %@'.fmt(scenario.name));
                    scenario.getPath('presentations.results').forEach(function(resultLibrary) {
                        SC.run(function() {
                            (resultLibrary.get('results') || []).forEach(function(result) {
                                result.refresh(YES);
                            });
                        });
                    }, this);
                }, this);
                // Refresh
                if (context.get('key')=='core')
                    Footprint.mapLayerGroupsController.refreshLayers(['end_state', 'increments']);
                else if (context.get('key')=='agriculture')
                    Footprint.mapLayerGroupsController.refreshLayers(['future_agriculture_feature']);
            }
            else {
                // Update the progress.
                analysisModule.set('progress', Math.min(1, analysisModule.get('progress') + context.get('proportion')));
                // If progress is complete, refresh everybody.
                if (analysisModule.get('progress') == 1) {

                    if (context.get('key') == 'vmt') {
                        Footprint.mapLayerGroupsController.refreshLayers(['vmt_feature']);
                    }

                    var result_key = 'result__%@'.fmt(context.get('key'));
                    var results = Footprint.resultsController.get('content').filter(function (result) {
                        return result.getPath('db_entity_key') == result_key;
                    });
                    results.forEach(function(result) {
                        result.refresh();
                    });
                    //analysisModule.refresh();
                }
            }
            return NO;
        },

        enterState: function(context) {
            this._context = toArrayController(context, this.get('crudParams'));
            this._recordsEditController = Footprint.analysisModulesEditController;
            this._nestedStore = Footprint.store.chainAutonomousStore();
            this._recordsEditController.set('nestedStore', this._nestedStore);
            this._content = this._recordsEditController.get('content');
            sc_super();
        },
        exitState: function() {
            this._recordsEditController = null;
            this._nestedStore.destroy();
            this._nestedStore = null;
            sc_super()
        },

        /***
         *
         * The undoManager property on each analysis_module
         */
        undoManagerProperty: 'undoManager',

        updateContext: function(context) {
            var recordContext = SC.ObjectController.create();
            return this.createModifyContext(recordContext, context)
        }
    })
});

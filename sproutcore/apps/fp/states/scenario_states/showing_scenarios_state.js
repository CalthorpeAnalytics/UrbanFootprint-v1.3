/***
 * The state that manages the projects pane at the top of the application
 * @type {Class}
 */

Footprint.ShowingScenariosState = SC.State.extend({

    scenarioDidChange: function(context) {
        // Let this propagate through to other listeners
        return NO;
    },
    scenariosDidChange: function(context) {
        this.gotoState('scenariosAreReadyState', context)
    },

    /***
     * Export the Scenario record in the context.
     * @param context - context.activeRecord contains the Scenario to export
     * @returns {*} YES if the context contains a Scenario, else NO
     */
    doExportRecord: function(context) {
        if (context.get('activeRecord')) {
            if (context.get('activeRecord').kindOf(Footprint.Scenario)) {
                // TODO export something!
                return YES;
            }}
        return NO;
    },
    /***
     * Called when the server-side analytic modules complete, instructing the ResultLibrary instance
     * and the mapController to refresh
     * @param context
     */
    analysisDidComplete: function(context) {

        var scenarios = Footprint.scenariosController.filter(function(scenario) {
            return scenario.get('id')==context.get('config_entity_id');
        });

        scenarios.forEach(function(scenario) {
            scenario.getPath('presentations.results').forEach(function(resultLibrary) {
                resultLibrary.refresh();
                (resultLibrary.get('results') || []).forEach(function(result) {
                    SC.RunLoop.begin();
                    result.refresh();
                    SC.RunLoop.end();
                });
            }, this);
        }, this);
        // It works better to do this here than in the FeatureUpdatingState.
        // Polymaps gets angry if we do it there
        Footprint.mapController.refreshLayer();
    },

    initialSubstate: 'readyState',
    readyState: SC.State.extend({
        enterState: function() {
            if ([SC.Record.READY_CLEAN, SC.Record.READY_DIRTY].contains(Footprint.scenariosController.get('status'))) {
                this.gotoState('scenariosAreReadyState', Footprint.scenariosController);
            }
        }
    }),

    scenariosAreReadyState: Footprint.RecordsAreReadyState.extend({
        recordsDidUpdateEvent: 'scenariosDidChange',
        recordsDidFailToUpdateEvent: 'scenariosDidFailToUpdate',
        updateAction: 'doScenarioUpdate',
        undoAction: 'doScenarioUndo',
        undoAttributes: ['name', 'year', 'description'],

        crudParams: function() {
            return {
                infoPane: 'Footprint.ScenarioInfoPane',
                recordsEditController: Footprint.scenariosEditController,
                recordType: Footprint.Scenario
            };
        }.property().cacheable(),

        doManageScenarios: function() {
            this.doViewScenario();
        },
        doCreateScenario: function() {
            Footprint.statechart.sendAction('doCreateRecord', this.get('crudParams'));
        },
        doCloneScenario: function() {
            Footprint.statechart.sendAction('doCloneRecord',  this.get('crudParams'));
        },
        doEditScenario: function() {
            Footprint.statechart.sendAction('doUpdateRecord',  this.get('crudParams'));
        },
        doViewScenario: function() {
            Footprint.statechart.sendAction('doViewRecord',  this.get('crudParams'));
        },

        editScenarioDidChange: function(context) {
            // Send the generic action. The modal_crud_state will respond and
            // check that the context equals the recordsEditController
            Footprint.statechart.sendAction('selectedEditRecordDidChange', context);
        },

        // Saving update events
        // Each update sends a 'proportion' value. When this proportion hits 100% the save is
        // completed. We use proportion both to show status and because concurrent publishers
        // on the server make it impossible to know otherwise when everything is complete.
        postSaveConfigEntityPublisherCompleted: function(context) {
            if (!['Scenario', 'BaseScenario', 'FutureScenario'].contains(context.get('config_entity_class_name')))
                // We only care about Scenarios in this state
                return NO;

            var combinedContext = toArrayController(context, {
                postProcessingDidEnd: function(context) {
                    var parentStore = context.getPath('content.store.parentStore');
                    [context.get('content')].forEach(function(record) {
                        record.refresh();
                    })
                }});
            Footprint.statechart.sendAction('doUpdateSaveProgress', combinedContext)
        },
        postSaveConfigEntityPublisherFailed: function(context) {
            if (!['Scenario', 'BaseScenario', 'FutureScenario'].contains(context.get('config_entity_class_name')))
            // We only care about Scenarios in this state
                return NO;
            Footprint.statechart.sendAction('postProcessRecordsDidFail', context)
        },


        undoManagerProperty: 'undoManager',

        /***
         * Scenarios have a basic update context. No flags are passed in for bulk updates
         * @returns {*}
         */
        updateContext: function(context) {
            var recordContext = SC.ObjectController.create();
            return this.createModifyContext(recordContext, context);
        },

        enterState: function(context) {
            // Do nothing here for now. Don't call the parent method
        }
    }),

    /***
     * Called by socketIO when asynchronous creation of the instance's components completes
     */
    scenarioCreationDidComplete: function(context) {
        // Refresh the Scenario ArrayController to sync the new record
        Footprint.scenariosController.get('content').refresh();
    }
});

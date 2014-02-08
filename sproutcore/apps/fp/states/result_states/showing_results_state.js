/***
 * The state that manages the projects pane at the top of the application
 * @type {Class}
 */
sc_require('states/loading_scenario_dependencies_states');

Footprint.ShowingResultsState = SC.State.design({

    initialSubstate:'readyState',

    readyState: SC.State,

    doViewScenario: function(context) {
        Footprint.statechart.sendAction('doViewResults', SC.Object.create({
            content:Footprint.scenarioActiveController
        }));
        return NO
    },

    errorState: SC.State.extend({
        enterState: function() {

        }
    })
});

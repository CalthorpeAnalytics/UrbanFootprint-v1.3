
/***
 * The Footprint Statechart. This extends SC.Statechart, which is a simple class that mixes in SC.StatechartManager
 * See SC.StatechartManager to understand or add functionality to this class.
 * @type {*}
 */
Footprint.Statechart = SC.Statechart.extend({
    trace: YES,

    rootState: SC.State.extend({
        initialSubstate: 'applicationReadyState',

        // Initial load state
        applicationReadyState: SC.State.plugin('Footprint.ApplicationReadyState'),
        // Login state
        loggingInState: SC.State.plugin('Footprint.LoggingInState'),
        // Loading state, which loads all configuration data required to show the app
        loadingAppState: SC.State.plugin('Footprint.LoadingAppState'),
        // Main application state, which delegates different sections of the application to substates
        showingAppState: SC.State.plugin('Footprint.ShowingAppState'),
        // For test
        testAppState: SC.State.plugin('Footprint.TestAppState'),
        /***
         * Communication to all the statechart's current states, which are handled by the first state that expects
         * that event, and otherwise sent to the state's child states until a handler is found.
         * We broadcasting events of a controller's status
         * The event name is always in the form controllerInstanceNameIsStatusString where status string is capital camel case
         */
        sendStatusEvent: function(controller, controllerName) {
            this.sendEvent('%@Is%@'.fmt(controllerName, getStatusString(controller.get('status')).toLowerCase().camelize().capitalize()));
        },

        doLogout: function() {
            Footprint.userController.destroyCookie();
            Footprint.mainPage.get('mainPane').remove();
            // TODO, we could keep stuff around that is user agnostic to save time
            Footprint.store.reset();
            Footprint.loadingStatusController.set('content', null);
            this.gotoState('loggingInState')
        }
    })
});

Footprint.statechart = Footprint.Statechart.create();

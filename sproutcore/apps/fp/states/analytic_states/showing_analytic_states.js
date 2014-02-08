/***
 * The state that manages the projects pane at the top of the application
 * @type {Class}
 */
Footprint.ShowingAnalyticState = SC.State.design({

    initialSubstate: 'readyState',
    readyState: SC.State,

    showFiscalModule: function() {
        Footprint.showingAnalyticModuleController.set('nowShowing', 'Footprint.FiscalModuleManagementView');
    },

    showVMTModule: function() {
        Footprint.showingAnalyticModuleController.setPath('nowShowing', 'Footprint.VmtModuleManagementView');
    }

});

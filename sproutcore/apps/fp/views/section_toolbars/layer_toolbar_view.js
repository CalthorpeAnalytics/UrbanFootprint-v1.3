/***
 * Displays a list of titlebars above the scenarios and the various analytic columns.
 * Clicking on the titlebars themselves changes the state of the application. The default state is the general view, achieved by clicking on the Scenarios bar. Clicking on an analytical changes to the detail state of that analytical category.
 * @type {Class}
 */


Footprint.LayerToolbarView =  Footprint.EditingToolbarView.extend({
    titleViewLayout: {height: 17},
    controlSize: SC.SMALL_CONTROL_SIZE,
    contentBinding: SC.Binding.oneWay('Footprint.scenarioActiveController.content'),
    recordType: Footprint.Layer,
    activeRecordBinding: SC.Binding.oneWay('Footprint.layerActiveController.content'),
    title: 'Layers',
    menuItems: [
        SC.Object.create({ title: 'Manage Layers', action: 'doViewLayer' }),
        SC.Object.create({ title: 'Export Selected', action: 'doExportRecord' }),
    ]
});


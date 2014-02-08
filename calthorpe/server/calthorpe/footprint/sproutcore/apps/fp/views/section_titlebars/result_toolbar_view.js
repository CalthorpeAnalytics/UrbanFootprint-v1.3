/***
 * Displays a list of titlebars above the scenarios and the various analytic columns.
 * Clicking on the titlebars themselves changes the state of the application. The default state is the general view, achieved by clicking on the Scenarios bar. Clicking on an analytical changes to the detail state of that analytical category.
 * @type {Class}
 */
Footprint.ResultToolbarView = Footprint.EditingToolbarView.extend({
    classNames: 'footprint-result-toolbars-view'.w(),
    recordType: Footprint.Layer,
    titleViewLayout: {height: 17},
    controlSize: SC.SMALL_CONTROL_SIZE,
    titles: SC.Object.create({
        titleView: 'Results'
    })
});

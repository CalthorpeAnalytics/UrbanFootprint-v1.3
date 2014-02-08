/***
 * Displays a list of titlebars above the scenarios and the various analytic columns.
 * Clicking on the titlebars themselves changes the state of the application. The default state is the general view, achieved by clicking on the Scenarios bar. Clicking on an analytical changes to the detail state of that analytical category.
 * @type {Class}
 */


Footprint.ScenarioToolbarView = Footprint.EditingToolbarView.extend({
    titleViewLayout: {left: 0, right: 270, height: 17},
    classNames: "footprint-scenario-toolbar-view".w(),
    contentBinding: SC.Binding.oneWay('Footprint.scenarioActiveController.content'),
    controlSize: SC.SMALL_CONTROL_SIZE,
    // Make the title Scenarios for [property name]
    contentNameProperty: 'parent_config_entity.name',
    title: 'Scenarios',
    titles: SC.Object.create({
        stats1View: 'Population',
        stats2View: 'Dwelling Units',
        stats3View: 'Employment'
    }),

    // TODO stats title bars must be dynamic
    childViews: 'titleView stats1View stats2View stats3View'.w(),

    recordType: Footprint.Scenario,
    activeRecordBinding: SC.Binding.oneWay('Footprint.scenarioActiveController.content'),
    menuItems: [
        SC.Object.create({ title: 'Manage Scenarios', keyEquivalent: 'ctrl_i', action: 'doManageScenarios' }),
        SC.Object.create({ isSeparator: YES }),
        SC.Object.create({ title: 'Export Selected', keyEquivalent: 'ctrl_e', action: 'doExportRecord', isEnabled:NO }),
        SC.Object.create({ title: 'Remove Selected', keyEquivalent: ['ctrl_delete', 'ctrl_backspace'], action: 'doRemoveRecord', isEnabled:NO })
    ],

    stats1View: SC.ToolbarView.extend({
        childViews: ['label'],
        layout: {right:180, width: 90, height: 17},
        anchorLocation: SC.ANCHOR_TOP,
        label: SC.LabelView.extend({
            valueBinding: SC.Binding.oneWay(parentViewPath(2, '.titles.stats1View'))
        })
    }),
    stats2View: SC.ToolbarView.extend({
        childViews: ['label'],
        layout: {right:90, width: 90, height: 17},
        anchorLocation: SC.ANCHOR_TOP,
        label: SC.LabelView.extend({
            valueBinding: SC.Binding.oneWay(parentViewPath(2, '.titles.stats2View'))
        })
    }),
    stats3View: SC.ToolbarView.extend({
        childViews: ['label'],
        layout: {right:0, width: 90, height: 17},
        anchorLocation: SC.ANCHOR_TOP,
        layoutBinding: SC.Binding.oneWay(parentViewPath(1, '.layouts.stats3View')),
        label: SC.LabelView.extend({
            valueBinding: SC.Binding.oneWay(parentViewPath(2, '.titles.stats3View'))
        })
    })
});


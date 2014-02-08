sc_require('views/section_titlebars/editing_toolbar_view');

/***
 * Displays a list of titlebars above the scenarios and the various analytic columns.
 * Clicking on the titlebars themselves changes the state of the application. The default state is the general view, achieved by clicking on the Scenarios bar. Clicking on an analytical changes to the detail state of that analytical category.
 * @type {Class}
 */


Footprint.ScenarioToolbarView = Footprint.EditingToolbarView.extend({
    titleViewLayout: {left: 0, width: .55, height: 17},
    classNames: "footprint-scenario-toolbar-view".w(),
    contentBinding: SC.Binding.oneWay('Footprint.scenarioActiveController.content'),
    controlSize: SC.SMALL_CONTROL_SIZE,
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
        SC.Object.create({ title: 'Undo', action: 'doUndo', isEnabledBinding:'Footprint.projectActiveController*childrenUndoManager.canUndo'}),
        SC.Object.create({ title: 'Redo', action: 'doRedo', isEnabledBinding:'Footprint.projectActiveController*childrenUndoManager.canRedo'}),
        SC.Object.create({ isSeparator: YES}),
        SC.Object.create({ title: 'Get Info', keyEquivalent: 'ctrl_i', action: 'doGetInfo'}),
        SC.Object.create({ title: 'Create New', action: 'doNewRecord'}),
        SC.Object.create({ title: 'Clone Selected', action: 'doAddRecord'}),
        SC.Object.create({ isSeparator: YES}),
        SC.Object.create({ title: 'Export Selected', keyEquivalent: 'ctrl_e', action: 'doExportRecord', isEnabled:NO}),
        SC.Object.create({ title: 'Remove Selected', keyEquivalent: ['ctrl_delete', 'ctrl_backspace'], action: 'doRemoveRecord', isEnabled:NO}),
    ],

    stats1View: SC.ToolbarView.extend({
        childViews: ['label'],
        layout: {left: .55, width: .15, height: 17},
        anchorLocation: SC.ANCHOR_TOP,
        label: SC.LabelView.extend({
            valueBinding: SC.Binding.oneWay(parentViewPath(2, '.titles.stats1View'))
        })
    }),
    stats2View: SC.ToolbarView.extend({
        childViews: ['label'],
        layout: {left: .7, width: .15, height: 17},
        anchorLocation: SC.ANCHOR_TOP,
        label: SC.LabelView.extend({
            valueBinding: SC.Binding.oneWay(parentViewPath(2, '.titles.stats2View'))
        })
    }),
    stats3View: SC.ToolbarView.extend({
        childViews: ['label'],
        layout: {left: .85, width: .15, height: 17},
        anchorLocation: SC.ANCHOR_TOP,
        layoutBinding: SC.Binding.oneWay(parentViewPath(1, '.layouts.stats3View')),
        label: SC.LabelView.extend({
            valueBinding: SC.Binding.oneWay(parentViewPath(2, '.titles.stats3View'))
        })
    })
});


/***
 * Displays a list of titlebars above the scenarios and the various analytic columns.
 * Clicking on the titlebars themselves changes the state of the application. The default state is the general view, achieved by clicking on the Scenarios bar. Clicking on an analytical changes to the detail state of that analytical category.
 * @type {Class}
 */


Footprint.ScenarioToolbarView = SC.ToolbarView.extend({
    titleViewLayout: {left: 0, right: 270, height: 17},
    classNames: "footprint-scenario-toolbar-view".w(),
    childViews: ['titleView', 'stats1View', 'stats2View', 'stats3View'],
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
    titleView: SC.LabelView.extend({
        layout: { height: 17, right: 35 },
        valueBinding: SC.Binding.transform(function(name) {
            if (!name)
                return 'Scenarios';
            else return 'Scenarios for %@'.fmt(name);
        }).oneWay('Footprint.scenarioActiveController.name')
    }),

    stats1View: SC.ToolbarView.extend({
        childViews: ['label'],
        layout: {right:180, width: 90, height: 18},
        anchorLocation: SC.ANCHOR_TOP,
        label: SC.LabelView.extend({
            valueBinding: SC.Binding.oneWay(parentViewPath(2, '.titles.stats1View'))
        })
    }),
    stats2View: SC.ToolbarView.extend({
        childViews: ['label'],
        layout: {right:90, width: 90, height: 18},
        anchorLocation: SC.ANCHOR_TOP,
        label: SC.LabelView.extend({
            valueBinding: SC.Binding.oneWay(parentViewPath(2, '.titles.stats2View'))
        })
    }),
    stats3View: SC.ToolbarView.extend({
        childViews: ['label'],
        layout: {right:0, width: 90, height: 18},
        anchorLocation: SC.ANCHOR_TOP,
        layoutBinding: SC.Binding.oneWay(parentViewPath(1, '.layouts.stats3View')),
        label: SC.LabelView.extend({
            valueBinding: SC.Binding.oneWay(parentViewPath(2, '.titles.stats3View'))
        })
    })
});


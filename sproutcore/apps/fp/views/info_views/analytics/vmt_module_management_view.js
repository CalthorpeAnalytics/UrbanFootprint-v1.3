/**
 * Created with PyCharm.
 * User: calthorpe
 * Date: 11/15/13
 * Time: 11:56 AM
 * To change this template use File | Settings | File Templates.
 */
sc_require('views/info_views/analytics/label_result_views');
sc_require('views/info_views/analytics/analytic_module_views');
sc_require('views/menu_render_mixin');

Footprint.VmtModuleManagementView = SC.View.extend({

    classNames: "footprint-vmt-module-management-view".w(),
    childViews: ['manageModuleView', 'moduleResultsView'],

    allResultsStatus: null,
    allResults: null,

    title: 'VMT Module',
    executeModuleAction: 'doRunVMT',
    editAssumptionsAction: 'doEditVMTPolicy',

    allResultsBinding: SC.Binding.oneWay('Footprint.resultsController.content'),
    allResultsStatusBinding: SC.Binding.oneWay('Footprint.resultsController.status'),

    content: function () {
        if (this.get('allResultsStatus') & SC.Record.READY)
            return this.get('allResults').filter(function (result) {
                return result.getPath('db_entity_key') == 'result__vmt';
            });
    }.property('allResults', 'allResultsStatus').cacheable(),

    contentFirstObject: null,
    contentFirstObjectBinding : SC.Binding.oneWay('*content.firstObject'),

    manageModuleView: Footprint.ManageModuleView,

    moduleResultsView: SC.View.extend({
        classNames: "footprint-module-results-view".w(),
        childViews: ['scenarioTitleView', 'dailyVmtResultView', 'annualVmtResultView', 'dailyPerHhVmtResultView', 'annualPerCapitaVmtResultView', 'dailyPerEmployeeVmtResultView'],
        layout: {top: 120},

        content: null,
        contentBinding: SC.Binding.oneWay('.parentView.contentFirstObject'),

        scenarioTitleView: SC.LabelView.extend({
            layout: {top: 10, left: 10, right: 10, height: 24},
            scenarioName: null,
            scenarioNameBinding: SC.Binding.oneWay('Footprint.scenarioActiveController.name'),
            value: function() {
            return '%@:'.fmt(this.get('scenarioName'));
        }.property('scenarioName')
        }),

        dailyVmtResultView: Footprint.TopLabeledResultView.extend({
            layout: {height: 40, top: 40, left: 40, right: 40, width: 200},
            result: null,
            resultBinding: SC.Binding.oneWay('.parentView*content.query'),
            columnName: 'daily_vmt__sum',
            title: 'Total Daily VMT'
        }),

        annualVmtResultView: Footprint.TopLabeledResultView.extend({
            layout: {height: 40, top: 90, left: 40, right: 40, width: 200},
            result: null,
            resultBinding: SC.Binding.oneWay('.parentView*content.query'),
            columnName: 'annual_vmt__sum',
            title: 'Total Annual VMT'
        }),

        dailyPerHhVmtResultView: Footprint.TopLabeledResultView.extend({
            layout: {height: 40, top: 140, left: 40, right: 40, width: 200},
            result: null,
            resultBinding: SC.Binding.oneWay('.parentView*content.query'),
            columnName: 'daily_vmt_per_hh__sum',
            title: 'Daily VMT Per HH'
        }),

        annualPerCapitaVmtResultView: Footprint.TopLabeledResultView.extend({
            layout: {height: 40, top: 190, left: 40, right: 40, width: 200},
            result: null,
            resultBinding: SC.Binding.oneWay('.parentView*content.query'),
            columnName: 'annual_vmt_per_capita__sum',
            title: 'Annual VMT Per Capita'
        }),

        dailyPerEmployeeVmtResultView: Footprint.TopLabeledResultView.extend({
            layout: {height: 40, top: 240, left: 40, right: 40, width: 200},
            result: null,
            resultBinding: SC.Binding.oneWay('.parentView*content.query'),
            columnName: 'daily_vmt_per_emp__sum',
            title: 'Daily VMT Per Employee'
        })
    })
})
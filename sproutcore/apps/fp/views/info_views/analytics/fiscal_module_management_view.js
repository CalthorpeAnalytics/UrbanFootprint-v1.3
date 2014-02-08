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

Footprint.FiscalModuleManagementView = SC.View.extend({

    classNames: "footprint-fiscal-module-management-view".w(),
    childViews: ['manageModuleView', 'moduleResultsView'],

    allResultsStatus: null,
    allResults: null,

    title: 'Fiscal Module',
    executeModuleAction: 'doRunFiscal',
    editAssumptionsAction: 'doEditFiscalPolicy',

    allResultsBinding: SC.Binding.oneWay('Footprint.resultsController.content'),
    allResultsStatusBinding: SC.Binding.oneWay('Footprint.resultsController.status'),

    content: function () {
        if (this.get('allResultsStatus') & SC.Record.READY)
            return this.get('allResults').filter(function (result) {
                return result.getPath('db_entity_key') == 'result__fiscal';
            });
    }.property('allResults', 'allResultsStatus').cacheable(),

    contentFirstObject: null,
    contentFirstObjectBinding : SC.Binding.oneWay('*content.firstObject'),

    manageModuleView: Footprint.ManageModuleView,

    moduleResultsView: SC.View.extend({
        classNames: "footprint-module-results-view".w(),
        childViews: ['scenarioTitleView', 'capitalCostResultView', 'operationsResultView', 'revenueResultView'],
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

        capitalCostResultView: Footprint.TopLabeledResultView.extend({
            layout: {height: 40, top: 40, left: 40, right: 40, width: 200},
            result: null,
            resultBinding: SC.Binding.oneWay('.parentView*content.query'),
            columnName: 'residential_capital_costs__sum',
            title: 'Capital Costs ($)'
        }),

        operationsResultView: Footprint.TopLabeledResultView.extend({
            layout: {height: 40, top: 90, left: 40, right: 40, width: 200},
            result: null,
            resultBinding: SC.Binding.oneWay('.parentView*content.query'),
            columnName: 'residential_operations_maintenance_costs__sum',
            title: 'Operations/Maintenance Costs ($)'
        }),

        revenueResultView: Footprint.TopLabeledResultView.extend({
            layout: {height: 40, top: 140, left: 40, right: 40, width: 200},
            result: null,
            resultBinding: SC.Binding.oneWay('.parentView*content.query'),
            columnName: 'residential_revenue__sum',
            title: 'Revenue ($)'
        })
    })
})
/**
 * Created with PyCharm.
 * User: calthorpe
 * Date: 11/15/13
 * Time: 11:56 AM
 * To change this template use File | Settings | File Templates.
 */
sc_require('views/info_views/analysis_module/label_result_views');
sc_require('views/info_views/analysis_module/analysis_module_view');

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
    analysisModule: null,
    analysisModuleBinding: SC.Binding.oneWay('Footprint.analysisModulesEditController*selection.firstObject'),

    content: function () {
        if (this.get('allResultsStatus') & SC.Record.READY)
            return this.get('allResults').filter(function (result) {
                return result.getPath('db_entity_key') == 'result__vmt';
            });
    }.property('allResults', 'allResultsStatus').cacheable(),

    contentFirstObject: null,
    contentFirstObjectBinding : SC.Binding.oneWay('*content.firstObject'),

    manageModuleView: Footprint.AnalysisModuleView.extend({
        contentBinding:SC.Binding.oneWay('.parentView.analysisModule')
    }),

    moduleResultsView: SC.View.extend({
        classNames: "footprint-module-results-view".w(),
        childViews: ['scenarioTitleView', 'totalVmtResultView', 'perhhVmtResultView', 'perCapitaVmtResultView', 'perEmployeeVmtResultView'],
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

        totalVmtResultView: Footprint.TwoValueLabeledResultView.extend({
            layout: {height: 45, top: 40, left: 10, right: 10},
            resultBinding: SC.Binding.oneWay('.parentView*content.query'),
            column1Name: 'daily_vmt__sum',
            column2Name: 'annual_vmt__sum',
            title: 'Total VMT (Miles)',
            subTitle1: 'Daily',
            subTitle2: 'Annual'
        }),

        perhhVmtResultView: Footprint.TwoValueLabeledResultView.extend({
            layout: {height: 45, top: 110, left: 10, right: 10},
            resultBinding: SC.Binding.oneWay('.parentView*content.query'),
            column1Name: 'daily_vmt_per_hh__sum',
            column2Name: 'annual_vmt_per_hh__sum',
            title: 'Per Household VMT (Miles)',
            subTitle1: 'Daily',
            subTitle2: 'Annual'
        }),

        perCapitaVmtResultView: Footprint.TwoValueLabeledResultView.extend({
            layout: {height: 45, top: 180, left: 10, right: 10},
            resultBinding: SC.Binding.oneWay('.parentView*content.query'),
            column1Name: 'daily_vmt_per_capita__sum',
            column2Name: 'annual_vmt_per_capita__sum',
            title: 'Per Capita VMT (Miles)',
            subTitle1: 'Daily',
            subTitle2: 'Annual'
        }),

        perEmployeeVmtResultView: Footprint.TwoValueLabeledResultView.extend({
            layout: {height: 45, top: 250, left: 10, right: 10},
            resultBinding: SC.Binding.oneWay('.parentView*content.query'),
            column1Name: 'daily_vmt_per_emp__sum',
            column2Name: 'annual_vmt_per_emp__sum',
            title: 'Per Employee VMT (Miles)',
            subTitle1: 'Daily',
            subTitle2: 'Annual'
        })
    })
})
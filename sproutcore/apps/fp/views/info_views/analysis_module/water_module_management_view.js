/**
 * Created with PyCharm.
 * User: calthorpe
 * Date: 11/15/13
 * Time: 11:56 AM
 * To change this template use File | Settings | File Templates.
 */
sc_require('views/info_views/analysis_module/label_result_views');
sc_require('views/info_views/analysis_module/analysis_module_view');

Footprint.WaterModuleManagementView = SC.View.extend({

    classNames: "footprint-water-module-management-view".w(),
    childViews: ['manageModuleView', 'moduleResultsView'],

    allResultsStatus: null,
    allResults: null,

    title: 'Water Module',
    executeModuleAction: 'doRunWater',
    editAssumptionsAction: 'doEditWaterPolicy',

    analysisModule: null,
    analysisModuleBinding: SC.Binding.oneWay('Footprint.analysisModulesEditController*selection.firstObject'),

    allResultsBinding: SC.Binding.oneWay('Footprint.resultsController.content'),
    allResultsStatusBinding: SC.Binding.oneWay('Footprint.resultsController.status'),

    content: function () {
        if (this.get('allResultsStatus') & SC.Record.READY)
            return this.get('allResults').filter(function (result) {
                return result.getPath('db_entity_key') == 'result__water';
            });
    }.property('allResults', 'allResultsStatus').cacheable(),

    contentFirstObject: null,
    contentFirstObjectBinding : SC.Binding.oneWay('*content.firstObject'),

    manageModuleView: Footprint.AnalysisModuleView.extend({
        contentBinding:SC.Binding.oneWay('.parentView.analysisModule')
    }),

    moduleResultsView: SC.View.extend({
        classNames: "footprint-module-results-view".w(),
        childViews: ['scenarioTitleView', 'totalWaterResultView', 'totalResidentialWaterResultView',
                     'totalCommercialWaterResultView', 'residentialWaterResultView', 'commercialWaterResultView'],
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

        totalWaterResultView: Footprint.TopLabeledResultView.extend({
            layout: {height: 40, top: 40, left: 10, right: 10},
            resultBinding: SC.Binding.oneWay('.parentView*content.query'),
            columnName: 'total_water_use__sum',
            title: 'Total Annual Water Use (gal)'
        }),

        totalResidentialWaterResultView: Footprint.TopLabeledResultView.extend({
            layout: {height: 40, top: 90, left: 10, right: 10},
            resultBinding: SC.Binding.oneWay('.parentView*content.query'),
            columnName: 'residential_water_use__sum',
            title: 'Annual Residenital Water Use (gal)'
        }),

        totalCommercialWaterResultView: Footprint.TopLabeledResultView.extend({
            layout: {height: 40, top: 140, left: 10, right: 10},
            resultBinding: SC.Binding.oneWay('.parentView*content.query'),
            columnName: 'commercial_water_use__sum',
            title: 'Annual Commercial Water Use (gal)'
        }),

        residentialWaterResultView: Footprint.TwoValueLabeledResultView.extend({
            layout: {height: 45, top: 200, left: 10, right: 10},
            resultBinding: SC.Binding.oneWay('.parentView*content.query'),
            column1Name: 'residential_indoor_water_use__sum',
            column2Name: 'residential_outdoor_water_use__sum',
            title:  'Annual Residential Water Use',
            subTitle1:'Indoor (gal',
            subTitle2: 'Outdoor (gal)'
        }),

        commercialWaterResultView: Footprint.TwoValueLabeledResultView.extend({
            layout: {height: 45, top: 260, left: 10, right: 10},
            resultBinding: SC.Binding.oneWay('.parentView*content.query'),
            column1Name: 'commercial_indoor_water_use__sum',
            column2Name: 'commercial_outdoor_water_use__sum',
            title:  'Annual Commercial Water Use',
            subTitle1:'Indoor (gal',
            subTitle2: 'Outdoor (gal)'
        })
    })
})
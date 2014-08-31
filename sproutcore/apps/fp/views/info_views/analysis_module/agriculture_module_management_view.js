/**
 * Created with PyCharm.
 * User: calthorpe
 * Date: 11/15/13
 * Time: 11:56 AM
 * To change this template use File | Settings | File Templates.
 */
sc_require('views/info_views/analysis_module/label_result_views');
sc_require('views/info_views/analysis_module/analysis_module_view');

Footprint.AgricultureModuleManagementView = SC.View.extend({

    classNames: "footprint-agriculture-module-management-view".w(),
    childViews: ['manageModuleView', 'moduleResultsView'],

    allResultsStatus: null,
    allResults: null,

    title: 'Agriculture Module',
    executeModuleAction: 'doRunAgriculture',
//    editAssumptionsAction: 'doEditEnergyPolicy',

    allResultsBinding: SC.Binding.oneWay('Footprint.resultsController.content'),
    allResultsStatusBinding: SC.Binding.oneWay('Footprint.resultsController.status'),

    analysisModule: null,
    analysisModuleBinding: SC.Binding.oneWay('Footprint.analysisModulesEditController*selection.firstObject'),

    content: function () {
        if (this.get('allResultsStatus') & SC.Record.READY)
            return this.get('allResults').filter(function (result) {
                return result.getPath('db_entity_key') == 'result__agriculture';
            });
    }.property('allResults', 'allResultsStatus').cacheable(),

    contentFirstObject: null,
    contentFirstObjectBinding : SC.Binding.oneWay('*content.firstObject'),

    manageModuleView: Footprint.AnalysisModuleView.extend({
        contentBinding:SC.Binding.oneWay('.parentView.analysisModule')
    }),

    moduleResultsView: SC.View.extend({
        classNames: "footprint-module-results-view".w(),
        childViews: ['scenarioTitleView', 'marketValueView', 'cropProductionView', 'productionCostView',
            'laborForceView', 'waterUseView', 'truckTripsView'],
        layout: {top: 120},

        content: null,
        contentBinding: SC.Binding.oneWay('.parentView.contentFirstObject'),

        scenarioTitleView: SC.LabelView.extend({
            layout: {top: 5, left: 10, right: 10, height: 24},
            scenarioName: null,
            scenarioNameBinding: SC.Binding.oneWay('Footprint.scenarioActiveController.name'),
            value: function() {
            return '%@:'.fmt(this.get('scenarioName'));
        }.property('scenarioName')
        }),

        // crop yield
        cropProductionView: Footprint.TopLabeledResultView.extend({
            layout: {height: 40, top: 30, left: 10, right: 10},
            resultBinding: SC.Binding.oneWay('.parentView*content.query'),
            columnName: 'crop_yield__sum',
            title: 'Crop Yield (tons)'
        }),

        // market value ($)
        marketValueView: Footprint.TopLabeledResultView.extend({
            layout: {height: 40, top: 75, left: 10, right: 10},
            resultBinding: SC.Binding.oneWay('.parentView*content.query'),
            columnName: 'market_value__sum',
            title: 'Market Value ($)'
        }),

        // production cost ($)
        productionCostView: Footprint.TopLabeledResultView.extend({
            layout: {height: 40, top: 120, left: 10, right: 10},
            resultBinding: SC.Binding.oneWay('.parentView*content.query'),
            columnName: 'production_cost__sum',
            title: 'Production Cost'
        }),

        // labor force (FTE's)
        laborForceView: Footprint.TopLabeledResultView.extend({
            layout: {height: 40, top: 165, left: 10, right: 10},
            resultBinding: SC.Binding.oneWay('.parentView*content.query'),
            columnName: 'labor_force__sum',
            title: "Labor Input (FTE's)"
        }),

        // water use (acre feet)
        waterUseView: Footprint.TopLabeledResultView.extend({
            layout: {height: 40, top: 210, left: 10, right: 10},
            resultBinding: SC.Binding.oneWay('.parentView*content.query'),
            columnName: 'water_consumption__sum',
            title: 'Annual Water Use (Acre Feet)'
        }),

        // truck trips (# of trips)
        truckTripsView: Footprint.TopLabeledResultView.extend({
            layout: {height: 40, top: 255, left: 10, right: 10},
            resultBinding: SC.Binding.oneWay('.parentView*content.query'),
            columnName: 'truck_trips__sum',
            title: 'Truck Trips (# of trips)'
        })
    })
})
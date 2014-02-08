/*
 * UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
 * 
 * Copyright (C) 2012 Calthorpe Associates
 * 
 * This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
 * 
 * This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * 
 * Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
 */

sc_require('views/section_titlebars/result_toolbar_view');
sc_require('views/list_views/horizontal_list_view');
sc_require('views/presentation/result/chart_stacking_toggle_view');
sc_require('views/presentation/result/chart_view');

Footprint.ResultSectionViewCharts = {};
Footprint.ResultSectionView = SC.View.extend({
    classNames: 'footprint-result-section-view'.w(),
    childViews: 'resultToolbarView resultsView'.w(),
    isEnabled: SC.Binding.oneWay('Footprint.resultsController').matchesStatus(SC.Record.READY_CLEAN),

    resultToolbarView: Footprint.ResultToolbarView.extend({
        controller: Footprint.scenariosController
    }),

    resultsView: Footprint.ResultsView = SC.ScrollView.extend({
        layout: { top: 16 },
        contentView: SC.HorizontalListView.extend({
            classNames: ['result-view'],

            allResults: null,
            allResultsBinding: SC.Binding.oneWay('Footprint.resultsController.content'),
            allResultsStatus: null,
            allResultsStatusBinding: SC.Binding.oneWay('Footprint.resultsController.status'),
            content: function () {
                if (this.get('allResultsStatus') & SC.Record.READY)
                    return this.get('allResults').filter(function (result) {
                        return result.getPath('configuration.result_type') != 'analytic_bars';
                    });
            }.property('allResults', 'allResultsStatus'),
            isSelectable: NO,

            /***
             * A 2 Dimensional Bar Chart
             * The 'samples' of the chart are Scenarios
             * The 'series' of the chart are an accumulated result for each Scenario (e.g. dwelling_units, employment, and population)
             * The content o`f the Example is the Result of the active Scenario. It is used to find the Result of the same key of all Scenarios in the scenarios property
             *
             * Naming conventions:
             * One query column in the series, which has a datapoint per sample, is a 'group'
             * The default presentation is to put the group samples side by side.
             * The alternative presentation is to stack the series of each sample, which is only enabled when the each series result is related (e.g. a series different types of dwelling_units)
             *
             * Example
             * Query columns: du_house__sum, du_apt__sum, du_condo__sum, i.e. the aggregate dwelling units of each housing type
             * Samples: 'smart (a)','trend (b)','dumb (c)'
             * Series: 'sum du house (x)','sum du apt (y)','sum du condo (z)',
             *
             * Grouped Presentation (Default):
             *   x  y
             *   xx y
             *  xxx yyy zzz
             *  ___________
             *  abc abc abc
             *
             *  Note that each series' items are separated and the common series datum of each sample grouped
             *
             * Stacked Presentation
             *
             *     z
             *  z  y  z
             *  y  x  y
             *  y  x  x
             *  x  x  x
             * ________
             *  a  b  c
             *
             *   Note that the series' items are together and the series of each sample are stacked.
             */

                //TODO: put chartStackingToggleView back in!
            exampleView: SC.View.extend({
                // Note: legendView and radioButtonView are isolated in the mixins TODO change to view classes
                childViews: 'labelView chartView chartStackingToggleView'.w(),

                isStacked: null,
                isStackedBinding: SC.Binding.oneWay('*content.configuration').transform(function (value) {
                    // @TODO The API should return one boolean, but sometimes it returns an array of one boolean
                    return Array.isArray(value.is_stacked) ? value.is_stacked[0] : value.is_stacked;
                }),

                isStackable: null,
                isStackableBinding: SC.Binding.oneWay('*content.configuration').transform(function (value) {
                    return value.stackable;
                }),

                // The Chart title View
                labelView: SC.LabelView.extend({
                    layout: { left: 10, top: 2, height: 20  },
                    valueBinding: SC.Binding.oneWay('.parentView*content.db_entity_interest.db_entity.name'),
                    tagName: 'h1',
                    classNames: ['results-chart-title'],


                }),

                chartStackingToggleView: Footprint.ChartStackingToggleView.extend({
                    valueBinding: '.parentView.isStacked',
                    isStackableBinding:SC.Binding.oneWay('.parentView.isStackable')
                }),

                chartView: Footprint.ChartView.extend({
                    contentBinding: SC.Binding.oneWay('.parentView.content'),
                    resultLibraryKeyBinding: SC.Binding.oneWay('Footprint.resultLibraryActiveController.key'),

                    isStackableBinding:SC.Binding.oneWay('.parentView.isStackable'),
                    isStackedBinding: SC.Binding.from('.parentView.isStacked'),

                    // Used to compare multiple scenarios
                    // TODO this should come from the multiple selected scenarios in the future
                    scenariosBinding: SC.Binding.oneWay('Footprint.scenariosController.content')
                })
            })
        })
    })
});

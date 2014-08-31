/*
 * UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
 *
 * Copyright (C) 2014 Calthorpe Associates
 *
 * This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
 *
 * This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
 */

sc_require('views/info_views/query_info_view');
sc_require('views/info_views/feature_table_info_view');

/***
 * The pane used to edit the settings of a new or existing Feature and the DbEntity to which it is associated (if any). The saving order of this will have to first save a created DbEntity and then the Feature if a DbEntity is being created here
 * @type {*}
 */
Footprint.FeatureSummaryInfoView = SC.View.extend({
    childViews: 'contentView'.w(),
    classNames: "footprint-summary-info-view".w(),
    recordType: null,
    selection: null,
    content: null,

    // TODO ideally these are in the declaration of the view subclass
    contentBinding: SC.Binding.oneWay('Footprint.featuresActiveController.content'),
    status: null,
    statusBinding: SC.Binding.oneWay('Footprint.featuresActiveController.status'),
    recordTypeBinding: SC.Binding.oneWay('.parentView.parentView.recordType'),
    selectionBinding: '.parentView.parentView.selection',
    layerSelection: null,
    layerSelectionBinding: SC.Binding.oneWay('Footprint.layerSelectionActiveController.content'),

    contentView: Footprint.ContentView.extend({
        childViews: 'resultsView commitButtonsView'.w(),
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        status: null,
        statusBinding: SC.Binding.oneWay('.parentView.status'),
        selection: null,
        selectionBinding: '.parentView.selection',
        recordTypeBinding: SC.Binding.oneWay('.parentView.recordType'),
        layerSelection: null,
        layerSelectionBinding: SC.Binding.oneWay('.parentView.layerSelection'),

        resultsView: Footprint.FeatureTableInfoView.extend({
            layout: {top: 10, bottom: 0},
            contentBinding: SC.Binding.oneWay('.parentView.content'),
            statusBinding: SC.Binding.oneWay('.parentView.status'),
            selectionBinding: '.parentView.selection',
            layerSelectionBinding: SC.Binding.oneWay('.parentView.layerSelection')
        }),

        commitButtonsView: Footprint.InfoPaneButtonsView
    })

});

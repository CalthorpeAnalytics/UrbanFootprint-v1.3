/*
 * UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
 *
 * Copyright (C) 2013 Calthorpe Associates
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
sc_require('views/info_views/features/feature_summary_info_view');
sc_require('views/info_views/features/feature_query_info_view');
sc_require('views/info_views/features/feature_edit_info_view');

/***
 * The pane used to edit the settings of a new or existing Feature and the DbEntity to which it is associated (if any). The saving order of this will have to first save a created DbEntity and then the Feature if a DbEntity is being created here
 * @type {*}
 */


Footprint.FeatureInfoPane = Footprint.InfoPane.extend({
    classNames: "footprint-feature-info-view opaque".w(),
    // context passed in upon creation. This may contain 'nowShowing'
    context: null,

    recordType: null,
    recordTypeBinding: SC.Binding.oneWay('Footprint.layerActiveController.featureRecordType'),
    content:null,
    contentBinding: SC.Binding.oneWay('Footprint.featuresActiveController.content'),
    selection: null, // TODO always null for now
    summaryContent:null,
    summaryContentBinding: SC.Binding.oneWay('Footprint.featureSummariesActiveController.content'),
    summarySelection: null, // TODO always null for now
    layerSelection: null,
    layerSelectionBinding: SC.Binding.oneWay('Footprint.layerSelectionEditController.content'),

    layout: { top: 0, width: 950, right: 0, height: 550 },

    /***
     * This checks context for nowShowing. You can override this property with a hard-coded nowShowing
     */
    nowShowing:function() {
        return this.getPath('context.nowShowing') || 'Footprint.FeatureSummaryInfoView';
    }.property('context').cacheable(),

    contentView: SC.TabView.design({
        content: null,
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        selection: null,
        selectionBinding: '.parentView.selection',
        recordType: null,
        recordTypeBinding: SC.Binding.oneWay('.parentView.recordType'),

        summaryContent: null,
        summaryContentBinding: SC.Binding.oneWay('.parentView.summaryContent'),
        summarySelection: null,
        summarySelectionBinding: '.parentView.summarySelection',

        layerSelection: null,
        layerSelectionBinding: SC.Binding.oneWay('.parentView.layerSelection'),

        layout: {top: 10},
        itemTitleKey: 'title',
        itemValueKey: 'value',
        items: [
            {title: 'Summary', value: 'Footprint.FeatureSummaryInfoView'},
            {title: 'Query', value: 'Footprint.FeatureQueryInfoView'},
            {title: 'Edit', value: 'Footprint.FeatureEditInfoView'}
        ],
        // Two way binding so that the view can receive the initial value from the parent but also change it
        nowShowingBinding: '.parentView.nowShowing'
    })


});

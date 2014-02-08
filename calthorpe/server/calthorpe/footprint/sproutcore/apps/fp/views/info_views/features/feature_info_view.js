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

sc_require('views/info_views/features/feature_info_view');
sc_require('views/info_views/content_view');
sc_require('views/info_views/feature_summary_view');
sc_require('views/info_views/number_info_view');
sc_require('views/info_views/query_info_view');
sc_require('views/info_views/description_info_view');
sc_require('views/info_views/select_info_view');
sc_require('models/scenario_built_form_feature_model');
sc_require('views/info_views/info_pane');
sc_require('views/info_views/features/feature_summary_info_view');
sc_require('views/info_views/features/feature_query_info_view');
sc_require('views/info_views/features/feature_edit_info_view');

/***
 * The pane used to edit the settings of a new or existing Feature and the DbEntity to which it is associated (if any). The saving order of this will have to first save a created DbEntity and then the Feature if a DbEntity is being created here
 * @type {*}
 */


Footprint.FeatureInfoView = Footprint.InfoPane.extend({
    classNames: "footprint-feature-info-view".w(),
    recordType: Footprint.Feature,
    content:null,
    contentBinding: SC.Binding.oneWay('Footprint.featuresActiveController.content'),
    selection: null,
    layout: { top: 0, width: 950, right: 0, height: 550 },
    nowShowing:null,
    contentView: SC.TabView.design({
        content: null,
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        selection: null,
        selectionBinding: '.parentView.selection',
        recordType: null,
        recordTypeBinding: SC.Binding.oneWay('.parentView.recordType'),
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

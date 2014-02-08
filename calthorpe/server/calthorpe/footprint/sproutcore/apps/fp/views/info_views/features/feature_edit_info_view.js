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
sc_require('views/info_views/feature_edit_view');
sc_require('views/info_views/number_info_view');
sc_require('views/info_views/query_info_view');
sc_require('views/info_views/description_info_view');
sc_require('views/info_views/select_info_view');
sc_require('models/scenario_built_form_feature_model');
sc_require('views/info_views/info_pane');
sc_require('views/client/scag/info_views/scag_primary_parcel_feature_info_view');
sc_require('views/client/scag/info_views/scag_general_plan_parcels_feature_info_view');
sc_require('views/client/scag/info_views/scag_primary_spz_feature_info_view');

/***
 * The pane used to edit the settings of a new or existing Feature and the DbEntity to which it is associated (if any). The saving order of this will have to first save a created DbEntity and then the Feature if a DbEntity is being created here
 * @type {*}
 */
Footprint.FeatureEditInfoView = SC.View.extend({
    classNames: "footprint-feature-edit-info-view".w(),
    childViews: 'contentView'.w(),
    recordType: null,
    selection: null,
    content: null,


    // TODO ideally these are in the declaration of the view subclass
    contentBinding: SC.Binding.oneWay('*parentView.parentView.content'),
    recordTypeBinding: SC.Binding.oneWay('*parentView.parentView.recordType'),
    selectionBinding: '*parentView.parentView.selection',

    contentView: Footprint.ContentView.extend({
        childViews: 'queryView summaryView editPrimaryParcelView editGeneralPlanView editSpzView commitButtonsView'.w(),
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        selection: null,
        selectionBinding: '.parentView.selection',
        recordTypeBinding: SC.Binding.oneWay('.parentView.recordType'),

        queryView: Footprint.QueryInfoView.extend({
            layout: {top:10, height: 102},
            contentBinding: SC.Binding.oneWay('Footprint.layerSelectionActiveController.content'),
            recordTypeBinding: SC.Binding.oneWay('.parentView.recordType')
        }),

        summaryView: Footprint.FeatureSummaryView.extend({
            layout: {top: 114, bottom: 0, width: 0.65},
            contentBinding: SC.Binding.oneWay('.parentView.content'),
            selectionBinding: '.parentView.selection',
            countBinding: SC.Binding.oneWay('.parentView.content').lengthOf(),
            recordTypeBinding: SC.Binding.oneWay('.parentView.recordType')
        }),

        /*
        viewOfRecordType:function() {
            if (this.get('recordType')) {
                var infoView = Footprint.InfoView.prototype.get('recordTypeToInfoView').get(this.get('recordType'));
                if (!infoView) {
                    throw Error("No Footprint.InfoView subclass was found to represent recordType: %@. You must create a descendant of Footprint.InfoView with a recordType property matching this recordType").fmt(this.get('recordType'));
                }
                return Footprint.ScagPrimaryParcelFeatureInfoView;
                return infoView
                    .extend({
                    layout: {top:0, bottom:0, right:0, left:0},
                    contentBinding: 'Footprint.recordEditController.content'
                });
            }
        }.property('recordType').cacheable()
        */
        //editView: SC.ContainerView.extend({

        editView:Footprint.ScagPrimaryParcelFeatureInfoView.extend({
            layout: {top: 114, bottom: 0, left: 0.65, right:0},
            //nowShowingBinding: SC.Binding.oneWay('.parentView.viewOfRecordType'),
            isVisible: function() {
                return this.get('recordType') && this.get('recordType') == Footprint.ScagPrimaryParcelFeatureInfoView.prototype.get('recordType');
            }.property('recordType')
        }),

        editGeneralPlanView:Footprint.ScagGeneralPlanParcelFeatureInfoView.extend({
            layout: {top: 114, bottom: 0, left: 0.65, right:0},
            //nowShowingBinding: SC.Binding.oneWay('.parentView.viewOfRecordType'),
            isVisible: function() {
                return this.get('recordType') && this.get('recordType') == Footprint.ScagGeneralPlanParcelFeatureInfoView.prototype.get('recordType');
            }.property('recordType')
        }),

        editSpzView:Footprint.ScagPrimarySpzFeatureInfoView.extend({
            layout: {top: 114, bottom: 0, left: 0.65, right:0},
            //nowShowingBinding: SC.Binding.oneWay('.parentView.viewOfRecordType'),
            isVisible: function() {
                return this.get('recordType') && this.get('recordType') == Footprint.ScagPrimarySpzFeatureInfoView.prototype.get('recordType');
            }.property('recordType')
        }),

        commitButtonsView: Footprint.InfoPaneButtonsView
    })

});
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

    layerSelection: null,
    layerSelectionBinding: SC.Binding.oneWay('.parentView.parentView.layerSelection'),

    contentView: Footprint.ContentView.extend({
        childViews: 'queryView summaryView editView commitButtonsView'.w(),
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        selection: null,
        selectionBinding: '.parentView.selection',
        recordTypeBinding: SC.Binding.oneWay('.parentView.recordType'),

        layerSelection: null,
        layerSelectionBinding: SC.Binding.oneWay('.parentView.layerSelection'),

        queryView: Footprint.QueryInfoView.extend({
            layout: {top:10, height: 102},
            contentBinding: SC.Binding.oneWay('.parentView.layerSelection'),
            recordTypeBinding: SC.Binding.oneWay('.parentView.recordType'),
            showSummaryFields: NO
        }),

        summaryView: Footprint.TableInfoView.extend({
            layout: {top: 114, bottom: 0, width: 0.65},
            contentBinding: SC.Binding.oneWay('.parentView.content'),
            selectionBinding: '.parentView.selection',
            countBinding: SC.Binding.oneWay('.parentView.content').lengthOf(),
            recordTypeBinding: SC.Binding.oneWay('.parentView.recordType'),
            layerSelectionBinding: SC.Binding.oneWay('.parentView.layerSelection')
        }),

        editView: SC.ContainerView.extend({
            layout: {top: 114, bottom: 0, left: 0.65, right:0},

            recordTypeBinding: SC.Binding.oneWay('.parentView.recordType'),
            contentBinding: SC.Binding.oneWay('.parentView.content'),

            nowShowingDefault:'defaultEditView',
            nowShowing: function() {
                if (this.get('recordType')) {
                    // Look for a view matching the recordType that adds the suffix InfoView to the record type name
                    var view = SC.objectForPropertyPath('%@InfoView'.fmt(this.get('recordType')));
                    if (view) {
                        return view.extend({
                           contentBinding: SC.Binding.oneWay('.parentView.content')
                        })
                    }
                }
                return this.get('nowShowingDefault');
            }.property('recordType').cacheable(),
            defaultEditView:SC.View
        }),

        commitButtonsView: Footprint.InfoPaneButtonsView
    })

});
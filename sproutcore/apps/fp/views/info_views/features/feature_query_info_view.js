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
Footprint.FeatureQueryInfoView = SC.View.extend({
    classNames: "footprint-feature-query-info-view".w(),
    childViews: 'contentView'.w(),
    recordType: null,
    selection: null,
    content: null,
    summarySelection: null,
    summaryContent: null,

    // TODO ideally these are in the declaration of the view subclass
    contentBinding: SC.Binding.oneWay('Footprint.featuresActiveController.content'),
    status: null,
    statusBinding: SC.Binding.oneWay('Footprint.featuresActiveController.status'),
    recordTypeBinding: SC.Binding.oneWay('.parentView.parentView.recordType'),
    selectionBinding: '.parentView.parentView.selection',

    summaryContentBinding: SC.Binding.oneWay('.parentView.parentView.summaryContent'),
    summarySelectionBinding: '.parentView.parentView.summarySelection',

    layerSelection: null,
    layerSelectionBinding: SC.Binding.oneWay('.parentView.parentView.layerSelection'),

    contentView: Footprint.ContentView.extend({
        childViews: 'queryView resultsView summaryResultsView commitButtonsView bufferView'.w(),
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        statusBinding: SC.Binding.oneWay('.parentView.status'),
        selection: null,
        selectionBinding: '.parentView.selection',

        summaryContent: null,
        summarySelection: null,
        summaryContentBinding: SC.Binding.oneWay('.parentView.summaryContent'),
        summarySelectionBinding: '.parentView.summarySelection',

        recordTypeBinding: SC.Binding.oneWay('.parentView.recordType'),

        layerSelection: null,
        layerSelectionBinding: SC.Binding.oneWay('.parentView.layerSelection'),

        queryView: Footprint.QueryInfoView.extend({
            layout: {top:10, height: 110},
            contentBinding: SC.Binding.oneWay('.parentView.layerSelection'),
            featuresStatus: null,
            featuresStatusBinding: SC.Binding.oneWay('Footprint.featuresActiveController.status'),
            layerSelectionStatus: null,
            layerSelectionStatusBinding: SC.Binding.oneWay('*content.status'),
            // For now don't let the user change any query options until everything is loaded
            isEnabled: function() {
                return (!(this.get('featuresStatus') & SC.Record.BUSY)) && (this.get('layerSelectionStatus') & SC.Record.READY);
            }.property('layerSelectionStatus', 'featuresStatus').cacheable(),

            recordTypeBinding: SC.Binding.oneWay('.parentView.recordType')
        }),

        resultsView: Footprint.FeatureTableInfoView.extend({
            contentBinding: SC.Binding.oneWay('.parentView.content'),
            statusBinding: SC.Binding.oneWay('.parentView.status'),
            selectionBinding: '.parentView.selection',
            layerSelectionBinding: SC.Binding.oneWay('.parentView.layerSelection')
        }),

        summaryResultsView: Footprint.TableInfoView.extend({
            classNames: "footprint-query-info-summary-results-view".w(),
            layout: {top: 125, bottom:.05, left:0.62, right: 0},
            title: 'Feature Summary',
            contentBinding: SC.Binding.oneWay('.parentView.summaryContent'),
            layerSelection: null,
            layerSelectionBinding: SC.Binding.oneWay('.parentView.layerSelection'),
            statusBinding: SC.Binding.oneWay('*layerSelection.status'),

            // The overlay is visible if layerSelection status is BUSY
            overlayStatus: function() {
                return this.get('status');
            }.property('status').cacheable(),

            columns: function() {
                if (!(this.get('status') & SC.Record.READY))
                    return [];
                var layerSelection = this.get('layerSelection');
                return (layerSelection.get('summary_fields') || []).map(function(field) {
                    return layerSelection.getPath('summary_field_title_lookup.%@'.fmt(field));
                });
            }.property('status').cacheable(),
            mapProperties: function() {
                if (!(this.get('status') & SC.Record.READY))
                    return SC.Object.create();
                return mapToSCObject(
                    Footprint.layerSelectionEditController.getPath('summary_fields') || [],
                    function(field) {
                        return [Footprint.layerSelectionEditController.getPath('summary_field_title_lookup.%@'.fmt(field)), field];
                    },
                    this
                );
            }.property('status').cacheable(),
            selectionBinding: '.parentView.summarySelection',
            countBinding: SC.Binding.oneWay('.parentView.summaryContent').lengthOf()
        }),

        commitButtonsView: Footprint.InfoPaneButtonsView.extend({
            layout: {left: .04, top: .92, width: 0.2}
        }),

        bufferView: SC.SegmentedView.extend({
            layout: { top:.94, height: 26, right: 0.01, width: 100 },
            selectSegmentWhenTriggeringAction: NO,
            itemActionKey: 'action',
            itemTitleKey: 'title',
            itemKeyEquivalentKey: 'keyEquivalent',
            itemValueKey: 'title',
            itemIsEnabledKey: 'isEnabled',

            items: [
                // View and edit the selected item's attributes
                SC.Object.create({ title: 'Undo', keyEquivalent: 'ctrl_u', action: 'doLayerSelectionUndo', isEnabledBinding: SC.Binding.oneWay('Footprint.layerSelectionActiveController*undoManager.canUndo').bool(), type: 'chronicler'}),
                SC.Object.create({ title: 'Redo', keyEquivalent: 'ctrl_r', action: 'doLayerSelectionRedo', isEnabledBinding: SC.Binding.oneWay('Footprint.layerSelectionActiveController*undoManager.canRedo').bool(), type: 'chronicler'})
            ]
        })
    })

});
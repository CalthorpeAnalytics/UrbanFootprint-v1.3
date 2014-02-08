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
sc_require('views/info_views/presentation/presentation_medium_info_view');
sc_require('views/sections/section_view');
sc_require('views/section_toolbars/layer_toolbar_view');


Footprint.LayerSectionView = Footprint.SectionView.extend({
    classNames: ['footprint-layer-section-view'],

    isEnabled: SC.Binding.oneWay('Footprint.layerCategoriesTreeController.status').matchesStatus(SC.Record.READY_CLEAN),

    overlayView: Footprint.OverlayView.extend({
        contentBinding: SC.Binding.from('Footprint.layerCategoriesTreeController'),
        statusBinding:SC.Binding.oneWay('Footprint.layerCategoriesTreeController.status')
    }),

    toolbarView: Footprint.LayerToolbarView,

    listView: SC.ScrollView.extend({
        layout: {top: 16, bottom: 0},

        contentView: SC.SourceListView.extend({
            layout: { top: 0 },
            rowHeight: 18,
            actOnSelect: NO,
            canReorderContent: NO,
            showAlternatingRows: YES,

            // An icon indicating the DbEntity type: layer, table, query, view, etc
            // Bind to the PresentationMedium instances of the active Scenario's default Library
            contentBinding: SC.Binding.from('Footprint.layerCategoriesTreeController.arrangedObjects'),
            selectionBinding: SC.Binding.from('Footprint.layerCategoriesTreeController.selection'),

            editControllerContent: null,
            editControllerContentBinding: SC.Binding.from('Footprint.layersEditController.content'),

            exampleView: SC.View.extend(SC.Control, {
                childViews: ['titleView', 'visibilityView', 'progressOverlayView'],

                editControllerContent: null,
                editControllerContentBinding: SC.Binding.from('.parentView.editControllerContent'),

                visibilityView: Footprint.VisibilityPickerView.extend({
                    layout: { left: 8, width: 18, height: 18 },
                    contentBinding: SC.Binding.oneWay('.parentView*content'),
                    valueBinding: '.parentView*content.visibility'
                }),
                titleView: SC.LabelView.extend({
                    layout: { left: 34 },
                    valueBinding: SC.Binding.oneWay('.parentView*content.name')
                }),
                progressOverlayView: Footprint.ProgressOverlayForMainStoreView.extend({
                    layout: { right: 0, width:100, centerY: 0, height: 16},
                    mainStoreContentBinding: SC.Binding.oneWay('.parentView.content'),
                    nestedStoreContentArrayBinding: SC.Binding.oneWay('.parentView.editControllerContent')
                })
            }),
            groupExampleView: SC.View.extend(SC.ContentDisplay, {
                contentDisplayProperties: ['name'],
                render: function(context) {
                    var title = this.getPath('content.name') || '';
                    title = title.titleize();
                    var themeClassNames = this.getPath('theme.classNames');
                    context = context.begin()
                                     .addClass(themeClassNames)
                                     .addClass(['sc-view', 'footprint-layer-group-view']);

                    context.begin()
                           .addClass(themeClassNames)
                           .addClass(['sc-view', 'footprint-layer-group-label-view'])
                           .push(title)
                           .end();

                    context = context.end();
                },
                update: function($context) {
                    var title = this.getPath('content.name') || '';
                    title = title.titleize();
                    $context.find('.footprint-layer-group-label-view').text(title);
                }
            })
        })
    })
});


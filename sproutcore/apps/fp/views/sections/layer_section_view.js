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

    overlayView: Footprint.OverlayView.extend({
        contentBinding:SC.Binding.oneWay('Footprint.dbEntityInterestsAndLayersController.content'),
        statusBinding:SC.Binding.oneWay('Footprint.dbEntityInterestsAndLayersController.status')
    }),

    toolbarView: SC.ToolbarView.extend({
        layout: { height: 20 },
        childViews: ['titleView', 'menuButtonView', 'expandButtonView'],
        titleView: SC.LabelView.extend({
            layout: { height: 16, centerY: 0, right: 35 },
            valueBinding: SC.Binding.transform(function(name) {
                if (!name) return 'Layers';
                else return 'Layers for %@'.fmt(name);
            }).oneWay('Footprint.scenarioActiveController.name')
        }),
        menuButtonView: Footprint.EditButtonView.extend({
            layout: { right: 38, width: 26 },
            icon: sc_static('fp:images/section_toolbars/pulldown.png'),
            activeRecordBinding: SC.Binding.oneWay('Footprint.layerCategoriesTreeController*selection.firstObject'),
            menuItems: [
                SC.Object.create({ title: 'Manage Layers', action: 'doViewLayer' }),
                SC.Object.create({ title: 'Export Selected', action: 'doExportRecord' })
            ]
        }),
        expandButtonView: SC.ButtonView.extend({
            layout: { right: 6, width: 26 },
            classNames: ['theme-button-gray', 'theme-button', 'theme-button-shorter'],
            icon: function() {
                if (this.get('value')) return sc_static('fp:images/section_toolbars/pullleft.png');
                else return sc_static('fp:images/section_toolbars/pullright.png')
            }.property('value').cacheable(),
            buttonBehavior: SC.TOGGLE_BEHAVIOR,
            valueBinding: 'F.layersVisibleController.layersMenuSectionIsVisible'
        })
    }),

    listView: SC.ScrollView.extend({
        layout: {top: 20, bottom: 0},

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

                // TODO: This is failing to map changes back to the record.
                // visibilityView: Footprint.VisibilityPickerView.extend({
                //     layout: { left: 8, width: 18, height: 18 },
                //     contentBinding: SC.Binding.oneWay('.parentView*content'),
                //     valueBinding: '.parentView*content.visibility'
                // }),
                visibilityView: SC.CheckboxView.extend({
                    layout: { left: 8, width: 16, height: 16, centerY: 0 },
                    valueBinding: '.parentView*content.applicationVisible'
                }),
                titleView: SC.LabelView.extend({
                    layout: { left: 34 },
                    valueBinding: SC.Binding.oneWay('.parentView*content.name')
                }),
                progressOverlayView: Footprint.ProgressOverlayView.extend({
                    layout: { left: 34, width:100, centerY: 0, height: 16},
                    contentBinding: SC.Binding.oneWay('.parentView*content.db_entity_interest')
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


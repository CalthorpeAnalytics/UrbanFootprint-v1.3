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
sc_require('views/visibility_picker_view');
sc_require('views/info_views/presentation/presentation_medium_info_view');
sc_require('views/sections/section_view');


Footprint.LayerSectionView = Footprint.SectionView.extend({
    classNames: "footprint-layer-section-view".w(),

    isEnabled: SC.Binding.oneWay('Footprint.layerCategoriesTreeController.status').matchesStatus(SC.Record.READY_CLEAN),

    toolbarView: Footprint.EditingToolbarView.extend({
        titleViewLayout: {height: 17},
        controlSize: SC.SMALL_CONTROL_SIZE,
        controller: Footprint.scenarioActiveController,

        recordType: Footprint.Layer,
        activeRecordBinding: SC.Binding.oneWay('Footprint.layerActiveController.content'),

        title: 'Layers'
        /*
         keyTitleView: SC.ToolbarView.extend({
         childViews:['title'],
         anchorLocation: SC.ANCHOR_TOP,
         layout: Footprint.layerSectionLayouts.key,
         title: SC.LabelView.extend({
         value: 'Key'
         })
         }),*/
    }),

    listView: SC.ScrollView.extend({
        layout: {top: 16, bottom: 0},

        contentView: SC.SourceListView.extend({
            isEnabledBindng: SC.Binding.oneWay('content').bool(),
            layout: { top: 8 },
            rowHeight: 18,
            actOnSelect: NO,
            classProperties: 'contentIndexIsEvent'.w(),
            canReorderContent: YES,


            // An icon indicating the DbEntity type: layer, table, query, view, etc
            // Bind to the PresentationMedium instances of the active Scenario's default Library
            contentBinding: SC.Binding.oneWay('Footprint.layerCategoriesTreeController.arrangedObjects'),
            selectionBinding: SC.Binding.from('Footprint.layerCategoriesTreeController.selection'),

            contentIndexIsEven:function() {
                return this.get('contentIndex') % 2 == 0;
            }.property('contentIndex').cacheable(),

            exampleView: SC.View.extend(SC.Control, {
                childViews: 'titleView visibilityView'.w(), //'icon keyLayout visibilityPicker popupButtonLayout'.w(),

                // The view that can be edited by double-clicking
                editableChildViewKey: 'nameView',

                visibilityView: Footprint.VisibilityPickerView.extend({
                    layout: {left: .02, width: 18, height: 18},
                    contentBinding: '.parentView*content',
                    valueBinding: '.parentView*content.visibility',
                    isVisibleBinding: SC.Binding.oneWay('.content').notContentKind(Footprint.TreeItem)
                }),

                titleView: Footprint.EditableModelStringView.extend({
                    isEditable: NO,
                    layout: {left: 0.1, width: .8 },
//                    valueBinding: '.parentView*content.db_entity_interest.db_entity.name',
                    contentBinding: '.parentView*content',
                    value: function() {
                        if (this.get('content').kindOf(Footprint.TreeItem)) {
                            return this.getPath('content.name').titleize();
                            }else {
                            return this.getPath('content.db_entity_interest.db_entity.name');
                        }

                    }.property('content').cacheable()
                })

                // Views to assign a key to the layer and to indicate if the layer is the selected layer for that key
//                keyEditView: Footprint.KeyEditView.extend({
//                      layoutBinding: SC.Binding.from(parentViewPath(1, '.layers.keyEditView')),
//                    contentBinding:'.parentView*content.db_entity_interest',
//                    itemsByKeyBinding: SC.Binding.oneWay('Footprint.layerLibraryActiveController.dbEntityInterestsByKey'),
//                    // Bind all DbEntities so we can see if this one is automatically the default or not
//                    selectedItemByKeyBinding: SC.Binding.oneWay('Footprint.layerLibraryActiveController.selectedDbEntityInterestsByKey'),
//                    // All keys that exist in the configEntity context
//                    keysBinding: SC.Binding.oneWay('Footprint.layerLibraryActiveController.keys'),
//                    keyItemPath: 'db_entity.key'
//                }),

            })
        })
    })
});


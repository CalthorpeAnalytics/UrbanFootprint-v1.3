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
 *
 */

sc_require('views/info_views/geography_info_view');
sc_require('views/info_views/tags_info_view');
sc_require('views/info_views/medium_info_view');
sc_require('views/sections/built_form_section_view');
sc_require('views/info_views/color_info_view');
sc_require('models/built_form_models');
sc_require('views/info_views/built_form/editable_building_attributes_view');
sc_require('views/info_views/built_form/editable_building_use_percents_view');
sc_require('views/info_views/built_form/editable_built_form_top_view');
sc_require('views/info_views/built_form/built_form_summary_attributes_view');
sc_require('views/info_views/built_form/built_form_items_scroll_view');
sc_require('views/info_views/built_form/editable_building_types_tagged_buildings_view');


/***
 * The pane used to edit the settings of a new or existing BuiltForm and the DbEntity to which it is associated (if any). The saving order of this will have to first save a created DbEntity and then the BuiltForm if a DbEntity is being created here
 * @type {*}
 */
Footprint.ManageBuildingView = SC.View.extend({
    classNames: ['footprint-add-building-view'],
    layout: {top:27},

    childViews:['overlayView', 'builtFormTopView', 'editableBuildingUsePercentView', 'editableBuildingAttributesView', 'buildingSummaryAttributesView', 'buildingTagView', 'buildingListView', 'buttonsView'],

    recordType: Footprint.PrimaryComponent,

    content: null,
    contentBinding: SC.Binding.oneWay('Footprint.buildingsEditController.content'),

    selection: null,
    selectionBinding: SC.Binding.from('Footprint.buildingsEditController.selection'),

    selectedItem: null,
    selectedItemBinding: SC.Binding.from('*selection.firstObject'),

    overlayView: Footprint.OverlayView.extend({
        layout: { left:10, width:330, bottom: 40, top: 20, zIndex:9999},
        contentBinding: SC.Binding.from('.parentView.content'),
        statusBinding:SC.Binding.oneWay('*content.status')
    }),

    builtFormTopView: Footprint.EditableBuiltFormTopView.extend({
        recordTypeBinding: SC.Binding.oneWay('.parentView.recordType'),
        contentBinding: SC.Binding.oneWay('.parentView.selectedItem'),
        titleValue: 'Building Name:'
    }),
    editableBuildingUsePercentView: Footprint.EditableBuildingUsePercentView.extend({
        contentBinding: SC.Binding.oneWay('.parentView.selectedItem')
    }),
    editableBuildingAttributesView: Footprint.EditableBuildingAttributesView.extend({
        contentBinding: SC.Binding.oneWay('.parentView.selectedItem')
    }),
    buildingSummaryAttributesView: Footprint.BuiltFormSummaryAttributesView.extend({
        contentBinding: SC.Binding.oneWay('.parentView.selectedItem')
    }),

    buildingTagView: Footprint.EditableBuildingTypesTaggedBuildingsView.extend({
        contentBinding: SC.Binding.oneWay('.parentView.selectedItem'),
        selectionBinding: SC.Binding.from('.parentView.selection')
    }),

    buildingListView: Footprint.BuiltFormItemsScrollView.extend({
        layout: { left:10, width:330, bottom: 40, top: 0, zIndex: 1},
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        recordTypeBinding: SC.Binding.oneWay('.parentView.recordType'),
        selectionBinding: SC.Binding.from('.parentView.selection')
    }),

    buttonsView: SC.View.extend({
        layout: { bottom: 0, right: 0, height: 40 },
        childViews: 'closeButtonView saveButtonView'.w(),
        classNames: ['footprint-add-building-buttons-view'],
        closeButtonView: SC.ButtonView.design({
            layout: {bottom: 5, left: 20, height:24, width:80},
            title: 'Close',
            action: 'doCancel',
            isCancel: YES
         }),
        saveButtonView: SC.ButtonView.design({
            layout: {bottom: 5, left: 360, height:24, width:80},
            title: 'Save',
            action: 'doSave'
         })
    })
})
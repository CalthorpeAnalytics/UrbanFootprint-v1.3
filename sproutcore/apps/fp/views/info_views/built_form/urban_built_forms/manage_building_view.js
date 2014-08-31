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
sc_require('views/info_views/built_form/urban_built_forms/editable_building_attribute_set_view');
sc_require('views/info_views/built_form/urban_built_forms/editable_building_use_percents_view');
sc_require('views/info_views/built_form/urban_built_forms/editable_building_top_view');
sc_require('views/info_views/built_form/urban_built_forms/building_summary_attributes_view');
sc_require('views/info_views/built_form/editable_built_forms_select_view');
sc_require('views/info_views/built_form/placetype_components_using_primary_component_view');
sc_require('views/info_views/built_form/built_form_buttons_view');
sc_require('views/info_views/built_form/manage_built_form_view');

/***
 * The pane used to edit the settings of a new or existing BuiltForm and the DbEntity to which it is associated (if any). The saving order of this will have to first save a created DbEntity and then the BuiltForm if a DbEntity is being created here
 * @type {*}
 */
Footprint.ManageBuildingView = Footprint.ManageBuiltFormView.extend({
    classNames: ['footprint-add-building-view'],
    layout: {top:27},
    // Tells the pane elements that a save is underway, which disables user actions
    isSaving: null,
    isSavingBinding: SC.Binding.oneWay('Footprint.buildingsEditController.isSaving'),
    childViews:['editableBuiltFormsSelectView', 'overlayView', 'builtFormTopView', 'editableBuildingUsePercentView', 'editableBuildingAttributesView', 'buildingSummaryAttributesView', 'buildingTypesUsingBuildingView', 'buttonsView', 'buildingUseLabelSelectView'],

    recordType: Footprint.Building,
    recordsEditControllerBinding: SC.Binding.oneWay('Footprint.buildingsEditController'),

    editableBuiltFormsSelectView: Footprint.EditableBuiltFormsFullListView.extend({
        layout: { left:10, width:330, bottom: 40, top: 0, zIndex: 1},
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        recordTypeBinding: SC.Binding.oneWay('.parentView.recordType'),
        selectionBinding: SC.Binding.from('.parentView.selection')
    }),

    overlayView: Footprint.OverlayView.extend({
        layout: { left:10, width:330, bottom: 40, top: 20, zIndex:9999},
        contentBinding: SC.Binding.from('.parentView.content'),
        statusBinding:SC.Binding.oneWay('*content.status')
    }),

    builtFormTopView: Footprint.EditableBuildingTopView.extend({
        layout: {left: 330, height:52, top: 0, width: 650},
        recordTypeBinding: SC.Binding.oneWay('.parentView.recordType'),
        contentBinding: SC.Binding.oneWay('.parentView.selectedItem')
    }),
    editableBuildingAttributesView: Footprint.EditableBuildingAttributeSetView.extend({
        layout: {left: 330, height:310, top: 52, width: 650},
        contentBinding: SC.Binding.oneWay('.parentView*selectedItem.building_attribute_set'),
        selectedItemBinding: SC.Binding.oneWay('.parentView.selectedItem')
    }),
    editableBuildingUsePercentView: Footprint.EditableBuildingUsePercentView.extend({
        layout: {left: 330, bottom:40, top:350, width: 650},
        // Bind the list of BuildingUsePercent instances
        contentBinding: SC.Binding.oneWay('.parentView*selectedItem.building_attribute_set.building_use_percents')
    }),
    buildingSummaryAttributesView: Footprint.BuildingSummaryAttributesView.extend({
        layout: {left: 970, height: 0.7},
        contentBinding: SC.Binding.oneWay('.parentView*selectedItem')
    }),
    buildingTypesUsingBuildingView: Footprint.PlacetypeComponentsUsingPrimaryComponentView.extend({
        title: "Building Types Using Building",
        layout: {left: 970, top: 0.7, bottom: 40},
        contentBinding: SC.Binding.oneWay('.parentView*selectedItem')
    }),
    buttonsView: Footprint.BuiltFormButtonsView.extend({
        layout: { bottom: 0, height: 40, left: 0, width: 350 },
        contentBinding: SC.Binding.oneWay('.parentView.content')
    }),

    buildingUseLabelSelectView: Footprint.LabelSelectView.extend({
        layout: {left: 440, bottom: 15, height: 24, right: 440},
        contentBinding: SC.Binding.oneWay('Footprint.buildingUseDefinitionsController.arrangedObjects'),
        itemTitleKey: 'name',
        selectionAction: 'doPickComponentPercent',
        nullTitle: 'Add New Building Use'
    })

})
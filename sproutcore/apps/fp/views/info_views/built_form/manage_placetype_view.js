/**
 * Created with PyCharm.
 * User: calthorpe
 * Date: 12/5/13
 * Time: 9:53 AM
 * To change this template use File | Settings | File Templates.
 */
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
sc_require('views/info_views/built_form/editable_built_form_top_view');
sc_require('views/info_views/built_form/editable_placetype_attributes_view');
sc_require('views/info_views/built_form/built_form_summary_attributes_view');
sc_require('views/info_views/built_form/built_form_items_scroll_view');


Footprint.ManagePlacetypeView = SC.View.extend(SC.ActionSupport,{

    childViews:['overlayView', 'builtFormTopView', 'editablePlacetypeAttributesView', 'placetypeSummaryAttributesView', 'placetypeListView', 'buttonsView'],
    layout: {top:27},

    recordType: Footprint.Placetype,

    content: null,
    contentBinding: SC.Binding.oneWay('Footprint.placetypesEditController.content'),

    selection: null,
    selectionBinding: SC.Binding.from('Footprint.placetypesEditController.selection'),

    selectedItem: null,
    selectedItemBinding: SC.Binding.from('*selection.firstObject'),

    overlayView: Footprint.OverlayView.extend({
        layout: { left:10, width:330, bottom: 40, top: 20, zIndex: 9999},
        contentBinding: SC.Binding.from('.parentView.content'),
        statusBinding:SC.Binding.oneWay('*content.status')
    }),

    builtFormTopView: Footprint.EditableBuiltFormTopView.extend({
        recordTypeBinding: SC.Binding.oneWay('.parentView.recordType'),
        contentBinding: SC.Binding.oneWay('.parentView.selectedItem'),
        titleValue: 'Placetype:'
    }),
    editablePlacetypeAttributesView: Footprint.EditablePlacetypeAttributesView.extend({
    }),
    placetypeSummaryAttributesView: Footprint.BuiltFormSummaryAttributesView.extend({
        contentBinding: SC.Binding.oneWay('.parentView.selectedItem')
    }),

    placetypeListView: Footprint.BuiltFormItemsScrollView.extend({
        layout: { left:10, width:330, bottom: 40, top: 0, zIndex: 1},
        contentBinding: SC.Binding.oneWay('.parentView.content'),
        recordTypeBinding: SC.Binding.oneWay('.parentView.recordType'),
        selectionBinding: SC.Binding.from('.parentView.selection')
    }),

    buttonsView: SC.View.extend({
        layout: { bottom: 0, right: 0, height: 40 },
        childViews: 'closeButtonView saveButtonView saveAsButtonView'.w(),
        classNames: ['footprint-add-built-form-buttons-view'],
        closeButtonView: SC.ButtonView.design({
            layout: {bottom: 5, left: 20, height:24, width:80},
            title: 'Close',
            action: 'doCancel',
            isCancel: YES
         }),
        saveButtonView: SC.ButtonView.design({
            layout: {bottom: 5, left: 360, height:24, width:80},
            title: 'Save',
            action: ''
         }),
        saveAsButtonView: SC.ButtonView.design({
            layout: {bottom: 5, left: 450, height:24, width:80},
            title: 'Save As',
            action: ''
         })
    })
})
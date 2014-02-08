/*
 *UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
 *
 *Copyright (C) 2013 Calthorpe Associates
 *
 *This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
 *
 *This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
 *
 *You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 *Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
 */

sc_require('views/section_titlebars/editing_toolbar_view');
sc_require('views/section_titlebars/edit_title_view');
sc_require('views/label_select_view');

/**
 * Replaces the awful SC.SelectView with a label and a menu button
 * @type {Class}
 * TODO SC.PopupButtonView.extend({ init: function() { sc_super(); this.menu.set('anchor', this) } })
 * This will set anchor and allow binding to the "parentView"
 */
Footprint.LabelSelectToolbarView = Footprint.EditingToolbarView.extend({
    layout: {height: 24},
    classNames: "footprint-label-select-toolbar-view".w(),
    icon: null,
    selection:null,

    titleView: Footprint.EditTitleView.extend({

//        editViewLayout: {height: 24, width: 0.1, right: 0},
        layoutBinding: SC.Binding.oneWay('.parentView.titleViewLayout'),
        recordTypeBinding: SC.Binding.oneWay('.parentView.recordType'),
        activeRecordBinding: SC.Binding.oneWay('.parentView.activeRecord'),
        menuItemsBinding: SC.Binding.oneWay('.parentView.menuItems'),
        controlSizeBinding: SC.Binding.oneWay('.parentView.controlSize'),
        titleBinding: SC.Binding.oneWay('.parentView.title'),
        iconBinding: SC.Binding.oneWay('.parentView.icon'),

        contentBinding: SC.Binding.oneWay('.parentView.content'),
        selection: null,
        selectionBinding: SC.Binding.oneWay('.parentView.selection'),

        itemTitleKey: null,
        itemTitleKeyBinding: SC.Binding.oneWay('.parentView.itemTitleKey'),

        labelView: Footprint.LabelSelectView.extend({
            contentBinding: SC.Binding.oneWay('.parentView.content'),
            selection: null,
            selectionBinding: SC.Binding.oneWay('.parentView.selection'),
            selectedItemBinding: '.parentView.selection.firstObject',
            itemTitleKeyBinding: SC.Binding.oneWay('.parentView.itemTitleKey')
        })
    })
});

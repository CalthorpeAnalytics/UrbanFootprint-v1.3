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

sc_require('views/section_titlebars/label_select_toolbar_view');
sc_require('views/button_layout_view');

/***
 * The BuiltFormTitlebarView enables selecting of the active BuiltFormSet as well as clone/edit of BuiltForms and BuiltFormSets
 * The default buttons operate on the selected BuiltForm, sine this operation is more common than manipulating BuiltFormSets
 * BuiltFormSets can be manipulated via the menu button
 * @type {*}
 */
Footprint.BuiltFormToolbarView = Footprint.LabelSelectToolbarView.extend({
    classNames: "footprint-built_form-toolbar-view".w(),
    titleViewLayout: {height: 24},
    controlSize: SC.REGULAR_CONTROL_SIZE,
    icon: function () {
        var image_path = 'images/section_titlebars/pulldown.png';
        return Footprint.STATIC.fmt(image_path);
    }.property('key').cacheable(),

    contentBinding: 'Footprint.builtFormSetsController.content',
    selectionBinding: 'Footprint.builtFormSetsController',
    recordType: Footprint.BuiltForm,
    activeRecordBinding: SC.Binding.oneWay('Footprint.builtFormActiveController.content'),

    title: null,
    itemTitleKey: 'name',

    menuItems: [
        // View and edit the selected item's attributes
        { title: 'Get Info', keyEquivalent: 'ctrl_i', action: 'doGetInfo'},
        { title: 'Visualize', keyEquivalent: 'ctrl_v', action: 'doVisualize'},
        { title: 'Export Selected', keyEquivalent: 'ctrl_e', action: 'doExportRecord'},
        { title: 'Remove Selected', keyEquivalent: ['ctrl_delete', 'ctrl_backspace'], action: 'doRemove'},
        { isSeparator: YES},
        { title: 'Clone BuiltForm Set', action: 'doAddSet'},
        { title: 'Get Info for BuiltForm Set', action: 'doGetSetInfo'}
    ]
});

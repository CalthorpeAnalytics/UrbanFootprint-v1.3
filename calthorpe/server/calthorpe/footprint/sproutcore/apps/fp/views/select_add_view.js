
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

sc_require('views/label_select_view');
sc_require('views/section_titlebars/edit_button_view');
sc_require('views/info_views/name_info_view');

/***
 * Extends Footprint.SelectView to add the ability to add/edit an item inline
 * @type {SC.RangeObserver}
 */
Footprint.SelectAddView = SC.View.extend({

    classNames: "footprint-select-add-view".w(),
    childViews:'selectView addButtonView'.w(),
    itemTitleKey: null,
    showCheckbox: YES,
    items:null,
    values:null,
    value:null,
    showAddView: YES,
    emptyName:null,

    /**
     * The Record type being selected, edited or added
     */
    recordType:null,

    selectView: Footprint.LabelSelectView.extend({
        layout:{left:0, width:.5},
        emptyNameBinding: parentViewPath(1,'*emptyName'),

        itemTitleKeyBinding: parentViewPath(1, '.itemTitleKey'),
        showCheckboxBinding: parentViewPath(1, '.showCheckbox'),
        itemsBinding: parentViewPath(1, '.items'),
        valuesBinding: parentViewPath(1, '.values'),
        valueBinding: parentViewPath(1, '.value')
    }),

    addButtonView: Footprint.AddButtonView.extend({
        controlSize: SC.SMALL_CONTROL_SIZE,
        layout:{left:.5, width:.2, centerY:0.001, height:.5},
        recordTypeBinding: parentViewPath(1, '.recordType'),
        action: 'cloneSelected'
    }),

    toString: function() {
        return "%@:\n%@".fmt(sc_super(), this.toStringAttributes('recordType itemTitleKey items values value'.w()));
    }
});


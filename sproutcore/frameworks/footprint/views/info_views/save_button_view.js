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

Footprint.SaveButtonView = SC.View.extend({
    layout: {height: 30, width: 100},
    classNames: "footprint-save-button-view".w(),

    childViews: 'saveButton'.w(),
    // The content
    content: null,
    status: null,
    statusBinding: SC.Binding.oneWay('*content.status'),
    // Indicates whether or not the content of the pane is editable
    isEditable: NO,
    // Indicates whether or not the content of the pane is editable and has changed--thus can be saved or cancelled
    isChanged: function() {
        return this.get('status') & SC.Record.READY_DIRTY
    }.property('status'),


    /***
     * The save button transfers the edited data from the nestedStore to the main store and commits it to the server
     * It is only enabled when the controller indicates that the contentIsChanged
     */
     saveButton: SC.ButtonView.design({
         layout: {height:24, width:80},
         title: 'Save',
         action: 'doSave',
         isDefault: YES,
         isVisibleBinding: SC.Binding.oneWay('.parentView.isEditable'),
         isEnabledBinding: SC.Binding.oneWay('.parentView.isChanged')
     })
});

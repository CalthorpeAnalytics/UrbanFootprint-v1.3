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

Footprint.InfoPaneButtonsView = SC.View.extend({
    layout: {left: .04, top: .9, width: 0.2},
    classNames: "footprint-info-pane-buttons-view".w(),

    childViews: 'saveButton closeButton'.w(),
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

    /*
     savingImage: SC.ImageView.design({
     layout: { bottom: 15, left: 175, height:16, width: 16 },
     value: sc_static('images/loading'),
     useImageCache: NO,
     isVisibleBinding: SC.Binding.from('parentView.editController*savingRecords.status').transform(
     function(value, isForward) {
     return value !== SC.Record.READY_CLEAN
     }
     )
     }),

     savingMessage: SC.LabelView.design({
     layout: { bottom: 8, left: 195, height:24, width: 100 },
     value: 'Saving ...',
     classNames: ['saving-message'],
     isVisibleBinding: SC.Binding.from('parentView.editController*savingRecords.status').transform(
     function(value, isForward) {
     return value !== SC.Record.READY_CLEAN
     }
     )
     }),

     deleteButton: SC.ButtonView.design({
     layout: {bottom: 10, left: 20, height:24, width:80},
     title: 'Delete',
     action: 'deleteRecord',
     isVisibleBinding: SC.Binding.from('.parentView.editController.contentIsChanged').bool().transform(
     function(value, isForward) {
     return !value;
     }
     )
     }),
     */

    /***
     * The save button transfers the edited data from the nestedStore to the main store and commits it to the server
     * It is only enabled when the controller indicates that the contentIsChanged
     */
     saveButton: SC.ButtonView.design({
         layout: {bottom: 10, right: 20, height:24, width:80},
         title: 'Save',
         action: 'doSave',
         isDefault: YES,
         isVisibleBinding: SC.Binding.oneWay('.parentView.isEditable'),
         isEnabledBindng: SC.Binding.oneWay('.parentView.isChanged')
     }),

    /***
     * Closes the view, discarding edited values that haven't been saved.
     */
    closeButton: SC.ButtonView.design({
        layout: {bottom: 10, height: 24, left: 20, width: 80},
        title: 'Close',
        action: 'doCancel',
        isCancel: YES,
        isVisibleBinding: SC.Binding.oneWay('.parentView.isEnabled')
    })
});

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

sc_require('views/info_views/info_pane_buttons_view');

/***
 * Abstract PickerPane to extend for editing an object.
 * @type {Class}
 */
Footprint.InfoPane = SC.PalettePane.extend(SC.ActionSupport, {

    classNames:'footprint-info-pane'.w(),

    /*** Required properties ***/
    recordType: null,

    selectionList: null,

    content: null,

    /***
     * This view should be added to the contentView childViews to enabling save, delete, and cancel
     */
    toggleButtonsView: Footprint.InfoPaneButtonsView.extend(),

    /**
     * Save changes
     * Note that the save button is only visible if there has been changes in the current user record
     */
    save: function () {
        this.get('editController').save(this, this.saveComplete);
    },

    /**
     * Check if saving has finished
     */
    saveComplete: function (errorObject) {
        if (SC.none(errorObject)) {
            if (this.get('refreshTarget'))
                findViewsByKind(this.get('refreshTarget')).forEach(function (view) {
                    view.set('layerNeedsUpdate', YES);
                });
            var self = this;
            this.invokeLater(function () {
                if (self.get('refreshAction'))
                    self.fireAction(self.get('refreshAction'));
            });
            SC.AlertPane.info('Save Completed');
        } else {
            this.showError(errorObject);
        }
        // Reset the controller update the item that was just created or updated
        // so the user can continue editing if desired
        this.get('editController').updateCurrent();
    },

    /**
     * Show an error message
     * @param e Error object to show
     */
    showError: function (e) {
        if (SC.instanceOf(e, SC.Error)) {
            SC.AlertPane.error(e.message);
            if (!SC.empty(e.label)) {
                var view = this.get('contentView').getPath(e.label);
                if (view) {
                    view.field.becomeFirstResponder();
                }
            }
        } else {
            logError(e);
            //SC.AlertPane.error(e.message);
        }
    },

    savingImage: SC.ImageView.design({
        layout: { bottom: 15, left: 175, height: 16, width: 16 },
        value: sc_static('images/loading'),
        useImageCache: NO,
        isVisibleBinding: SC.Binding.from('.editController.savingRecords.status').transform(
            function (value, isForward) {
                return value !== SC.Record.READY_CLEAN
            })
    }),

    /*
     savingMessage: SC.LabelView.design({
     layout: { bottom: 8, left: 195, height:24, width: 100 },
     value: 'Saving ...',
     classNames: ['saving-message'],

     isVisibleBinding: SC.Binding.from('.contenteditController.savingRecords.status').transform(
     function(value, isForward) {
     return value !== SC.Record.READY_CLEAN
     })
     }),
     */

    toString: function () {
        return "%@:\n%@".fmt(sc_super(), this.toStringAttributes('recordType controllers'.w()));
    }
});


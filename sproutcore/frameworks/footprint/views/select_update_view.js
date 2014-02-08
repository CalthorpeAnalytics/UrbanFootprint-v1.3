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
sc_require('views/editable_model_string_view');
sc_require('views/menu_button_view');


/***
 * Extends Footprint.SelectView to update all specified attributes of another record to the selected item
 * @type {SC.RangeObserver}
 */
Footprint.SelectUpdateView = Footprint.LabelSelectView.extend({
    classNames: "footprint-select-update-view".w(),

    // The record to update whenever the selection changes. No update happens when the identical item is selected
    target:null,

    /***
     * If specified this indicates a relative property path from the content and each item to get to the source
     * and target of the data that should be copied. Otherwise the top level objects will be used.
     * Make sure to specify a '.' or '*' at the start of the path
     */
    objectPath:null,
    targetPath: function() {
        '.target%@'.fmt(this.get('objectPath'))
    }.property('objectPath'),
    valuePath: function() {
        '.value%@'.fmt(this.get('objectPath'))
    }.property('objectPath'),

    // This handles a bug that may or may not still exist: https://groups.google.com/forum/?fromgroups=#!searchin/sproutcore/SelectView/sproutcore/oMkzyjiBdH0/dzLLsjUmWAQJ
    itemsDidChange: function() {
        this.set('layerNeedsUpdate', YES);
    }.observes('*items.length'),

    observeValue: function() {
        var value = this.get('value');
        var target = this.get('target');
        if (value === SC.Record.READY_CLEAN) {
            if (value.constructor!=target.constructor)
                throw("target is not the same class as selected item in list. Target:%@. Selected Item:%@".fmt(target, value))
            // Clone the value and copy its properties to the target.
            if (value != target) {
                this.getPath(this.get('valuePath')).cloneAndTransferProperties(
                    Footprint.Store,
                    this.getPath(this.get('targetPath')), function() {
                    // TODO we might need to update a parent view
                    // this.setPath('parentView.layerNeedsUpdate', YES);
                });
            }
        }
    }.observes('value')
});




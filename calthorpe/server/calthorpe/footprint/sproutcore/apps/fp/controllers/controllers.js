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
sc_require('object_extensions');

/***
 * The standardized packaging of controllers for use by views for editing and cloning
 */
Footprint.ControllerConfiguration = SC.Object.extend({

    /***
     * An SC.ObjectController that edits one or more objects
     */
    editController:null,
    /***
     * A list controller, such as an ListController or TreeController that manages the objects
     */
    itemsController:null,
    /***
     * A controller with additional computed properties about the objects, otherwise the same as itemsController
     */
    recordSetController:null,

    toString: function() {
        return "%@:\n%@".fmt(sc_super(), this.toStringAttributes('editController itemsController recordSetController'.w()));
    }
});

Footprint.SingleSelectionSupport = {

    // Whenever something changes the mixer's selection, notify the singleSelection property
    // so that it updates immediate for those that are bound to/observing it
    selectionObserver: function() {
        this.notifyPropertyChange('singleSelection');
    }.observes('.selection'),

    /***
     * Property to read and write a single value from/to the selection property
     * @param keyProp
     * @param value
     */
    singleSelection: function(keyProp, value) {
        //Clear the selection and add the selected set of the controller
        if (value !== undefined) {
            this.selectObject(value);
        }
        else {
            var selection = this.get('selection');
            return selection._objects ? selection._objects[0] : null;
        }
    }.property('selection').cacheable()
};


Footprint.ArrayContentSupport = {
    contentHasChangedObserver: function() {
        if (this.getPath('content.status') & SC.Record.READY) {
            this.notifyPropertyChange('firstObject');
            this._scac_contentDidChange();
            this.updateSelectionAfterContentChange();
            if (this.firstObject() !== this.get('firstObject'))
                throw "firstObject did not invalidate. Should be %@ but got %@".fmt(this.firstObject(), this.get('firstObject'))
        }
    }.observes('*content.status')
};

Footprint.ArrayController = SC.ArrayController.extend(Footprint.ArrayContentSupport, {
    allowsEmptySelection:NO,
    allowsMultipleSelection:NO,
    canDeleteContent:YES,
    // Sometimes we'll destroy the item on the server if its removed from the Array.
    // For some lists we'll just want to remove the item from the list, especially for Libraries
    destroyOnRemoval:NO,

    toString: function() {
        return this.toStringAttributes('content'.w(), {content: function(content) {
            return content && content.map(function(item) {
                return item.toString()
            }, this).join("\n---->");
        }});
    }

});


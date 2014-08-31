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
        return this.getPath('selection.firstObject');
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

/***
 * Helps an editController stay up to date with the non-edit controller selection
 * @type {{selectionDidChange: Function}}
 */
Footprint.EditControllerSupport = {
    /***
     * The non-nested controller whose selection we are tracking
    */
    sourceController: null,
    sourceSelectionDidChange: function() {
        if (this.get('content')) {
            // Get the unnested store selection for the sourceController
            var selectedItem = this.getPath('sourceController.selection.firstObject');
            if (!selectedItem) {
                this.deselectObjects(this.getPath('selection'));
                return;
            }

            // Find the nested store equivalent
            var nestedStoreItem = this.get('content').filter(function(item) { return item.get('id')===selectedItem.get('id')})[0];
            // If it doesn't match our selection update our selection
            if (!SC.Set.create([nestedStoreItem]).isEqual(SC.Set.create(this.get('selection'))))
                this.selectObject(nestedStoreItem);
        }
    }.observes('*sourceController.selection', '.content'),

    // If our selection goes to none selected resync with the source controller's selection
    // This happens when a managing state is exited
    selectionDidChange: function() {
        if (this.getPath('selection.length') == 0 &&
            this.getPath('sourceController.selection.length') > 0) {
            // Resync
            this.sourceSelectionDidChange();
        }
    }.observes('.selection')
};

/***
 * Copies the behavior of SC.ManyArray to calculate a combined status of the items. The max status of all items is returned by calculatedStatus
 * @type {{contentDidChange: Function, calculateStatus: Function, _calcluateStatus: Function, calculatedStatus: null, refresh: Function, toString: Function}}
 */
Footprint.CalculatedStatusSupport = {

    // Set up observers.
    contentDidChange: function() {
        var observedRecords = this._observedRecords;
        if (!observedRecords) observedRecords = this._observedRecords = [];
        var record, i, len;
        // If any items in observedRecords are not in content, stop observing them.
        len = observedRecords.length;
        for (i = len - 1; i >= 0; i--) {
            record = observedRecords.objectAt(i);
            if (!this.contains(record)) {
                record.removeObserver('status', this, this.calculateStatus);
                observedRecords.removeObject(record);
            }
        }
        // If any item in content is not in observedRecords, observe them.
        len = this.get('length');
        for (i = 0; i < len; i++) {
            record = this.objectAt(i);
            if (!observedRecords.contains(record)) {
                record.addObserver('status', this, this.calculateStatus);
                this.invokeOnce(this.calculateStatus);
                observedRecords.pushObject(record);
            }
        }
    }.observes('[]'),

    calculateStatus: function() {
        this.invokeOnce(this._calcluateStatus);
    },
    _calcluateStatus: function() {
        var length = this.get('length');
        var maxStatus = 0;
        for (i = 0; i < length; i++) {
            var status = this.objectAt(i).get('status');
            maxStatus = status > maxStatus ? status : maxStatus;
        }
        var status = maxStatus || SC.Record.EMPTY;
        this.setIfChanged('calculatedStatus', status);
    },

    calculatedStatus: null,

    refresh: function() {
        var length = this.get('length');
        for (i = 0; i < length; i++) {
            var record = this.objectAt(i);
            record.refresh();
        }
    },

    toString: function() {
        return sc_super() + "\n---->" +
            this.map(function(item) {
                return item.toString()
            }, this).join("\n---->");
    }
};

// This controller's content is the associated (non-deleted) children of the specified recordType
// in the specified nested store. For example, set parentRecord to the selected project and recordType
// to Footprint.Scenario to get the nested-store copies of the current project's scenarios.
Footprint.EditArrayController = Footprint.ArrayController.extend(Footprint.EditControllerSupport, Footprint.CalculatedStatusSupport, {
    recordType: null,
    nestedStore: null,
    // a property on the recordType being queried. If specified,
    // it will be used as a query filter matching the value of parentRecord
    // content will be null whenever parentEntityKey is specified but parentRecord is null.
    parentEntityKey: null,
    parentRecord: null,
    /***
     * Set by the Crud stat when saving starts and ends
     */
    isSaving: NO,
    conditions: 'deleted != YES',

    content: function() {
        var nestedStore = this.get('nestedStore'),
            parentRecord = this.get('parentRecord'),
            parentEntityKey = this.get('parentEntityKey');

        var recordType = typeof this.get('recordType') === 'string' ?
            SC.objectForPropertyPath(this.get('recordType')) : this.get('recordType');

        if (!nestedStore || !recordType || (parentEntityKey && !parentRecord))
            return null;
        return this.get('nestedStore').find(SC.Query.local(recordType, this.get('parentEntityKey') ? {
                conditions: '%@ $ {parentRecord} AND deleted != YES'.fmt(parentEntityKey),
                parentRecord: this.get('nestedStore').find(parentRecord.constructor, parentRecord.get('id'))
            } : {
                conditions: this.get('conditions')
            }
        ));
    }.property('recordType', 'nestedStore', 'parentRecord').cacheable()

});

Footprint.RecordControllerChangeSupport = {

    contentDidChangeEvent: null,
    selectedItemDidChangeEvent: null,

    /***
     * Announces a change of the content when its status matches READY
     */
    contentDidChange: function() {
        if (this.didChangeFor('contentOrStatusChange', 'status', 'content') &&
            // TODO this should just be READY_CLEAN, but our status is sometimes dirty
            // We have to check content.status instead of status. When content changes
            // status will still have the previous status.
            [SC.Record.READY_CLEAN, SC.Record.READY_DIRTY].contains(this.getPath('content.status')))
            Footprint.statechart.sendAction(this.get('contentDidChangeEvent'), this);
    }.observes('content', 'status'),

    /***
     * Announces a change of the selected item.
     */
    selectedItemDidChangeObserver: function() {
        if (this.get('status') & SC.Record.READY && this.getPath('selection.firstObject.status') & SC.Record.READY)
            Footprint.statechart.sendAction(this.get('selectedItemDidChangeEvent'), SC.Object.create({content : this.getPath('selection.firstObject')}));
    }.observes('.status', '.selection')
}

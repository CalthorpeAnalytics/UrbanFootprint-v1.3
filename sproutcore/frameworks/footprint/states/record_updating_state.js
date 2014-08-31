/*
* UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
* 
* Copyright (C) 2014 Calthorpe Associates
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
 *  Base class for simple updating all types of records.
 *  This class allows multiple records to update any attributes.
 *  It does not support nested updates--see record_crud_states for that.
 *
 */
Footprint.RecordUpdatingState = SC.State.extend({

    /***
     * The event to call when the record(s) sucessfully update
     */
    recordsDidUpdateEvent: null,

    /***
     * The event to call when the record(s) failed to update
     */
    recordsDidFailToUpdateEvent: null,

    /***
     * The action to call to handle undoing the record(s) with their undoManager
     */
    undoAction: null,
    /***
     * The action to call to handle updating within a redo operation
     */
    updateAction: null,

    initialSubstate:'readyState',
    readyState:SC.State,

    /***
     * Event called after the records update to register an undo in the context's undoManager, using the context's
     * undoContext as the target for the undo operation
     * @param context
     */
    recordsDidUpdate:function(context) {
        var undoManager = context.get('undoManager');
        var undoContext = context.get('undoContext');
        var self = this;
        undoManager.registerUndo(function() {
            // This registers a redo by doing a normal update within the undo. Amazing.
            undoManager.registerUndo(function() {
                Footprint.statechart.sendAction(self.get('updateAction'), context);
            });
            // Sends an action that can be handled by the parent state if the context recordType matches
            Footprint.statechart.sendAction(self.get('updateAction'), undoContext);
        });
        // Send the didUpdateEvent
        Footprint.statechart.sendEvent(this.get('recordsDidUpdateEvent'), this._context);
    },

    /***
     * Cancel the in-process update
     * @param context
     */
    cancelUpdate: function() {
        // Remove observers
        this._recordsQueue.forEach(function(record) {
            record.removeObserver('status', this, 'recordStatusDidChange');
        }, this);

        if (this._records)
            this._records.getPath('firstObject.store').discardChanges();
        // Use the undoContext to reset each records values
        var undoContext = this._context.get('undoContext');
        // Just like when we prepare for the update, except instead update the records
        // according to the undoContext.
        this.updateRecordsToContexts(undoContext.get('recordContexts'));
    },
    /***
     * React to record save failures by canceling the entire update to avoid bad state problems
     * @param context
     * @returns {NO|*}
     */
    recordsDidFailToUpdate: function(context) {
        this.cancelUpdate();
        return NO;
    },

    /***
     * Enters the updating state
     * @param context. An object with the following properties:
     *  recordType: The recordType of all the records in recordContexts
     *  recordContexts: An array of SC.Objects with the following structure:
     *      record: The record instance
     *      attribute1...attributeN: any number of attributes and their target values.
     *       -- Each record is thus paired with attributes and values with which to update the record.
     *          This structure is naturally used for updating, undoing, and redoing.
     *  undoManager: The SC.UndoManager used to manage this record, recordType, logical group of records, etc.
     *      The granularity of the undoManager depends on what the user reasonably expects undo/redo to do in a
     *      certain UI context.
     *  undoContext: Identical in structure to the entire context param, minus an undoContext.
     *  Used to undo the update that is configured. No undoContext is needed because the undoManager already knows
     *  how to undo to the previous context by the entire context.
     */
    enterState: function(context) {
        this._context = context;
        var recordContexts = context.get('recordContexts');
        // Create a lookup of each record by id, mapping it to it's recordContext
        var recordContextLookup = $.mapToDictionary(recordContexts, function(recordContext) {
            return [recordContext.getPath('record.id'), recordContext]
        });
        this._records = recordContexts.map(function(recordContext) {
            return recordContext.get('record');
        });
        this._recordsQueue = SC.Set.create(this._records);
        // Prevent a race condition below
        this._finished = NO;

        // Perform our actual record updates
        this._records.forEach(function(record) {
            // Add observer on each record
            record.addObserver('status', this, 'recordStatusDidChange');
        }, this);
        // Applies the attributes in the recordContexts to the records
        this.updateRecordsToContexts(recordContexts);

        // Commit the records to the datasource
        this._nestedStore = this._records.getPath('firstObject.store');
        this._nestedStore.commitRecords(
            this._records.mapProperty('storeKey').map(function(storeKey) {
                return this._nestedStore.recordTypeFor(storeKey);
            }, this),
            this._records.mapProperty('id'),
            this._records.mapProperty('storeKey')
        );
        // Manually invoke observer in case everything is already done
        this.recordStatusDidChange();
    },

    /***
     * Takes the record in each recordContext and updates it to the key/value pairs in the context
     * @param recordContexts
     */
    updateRecordsToContexts: function(recordContexts) {
        return recordContexts.map(function(recordContext) {
            // Set attributes of record based on the key/value pairs stored with it
            // If the records were already modified then the context won't contain any attributes
            var record = recordContext.get('record');
            var updateHash = filter_keys(recordContext, record.constructor.allRecordAttributeProperties(), 'object');
            record.setIfChanged(updateHash);
            // SC doesn't call recordDidChange when you go from A to B and then back to B on a set attribute
            // Seems to be a bug. Call manually instead
            record.recordDidChange();
        }, this);
    },

    recordStatusDidChange: function(sender) {
        this.invokeOnce(this._recordStatusDidChange);
    },
    _recordStatusDidChange: function() {
        if (!this._recordsQueue)
            // Late binding
            return;

        var recordsDequeue = [];
        if ($.any(this._recordsQueue, function(record) {
            return record && record.get('status') === SC.Record.ERROR;
        })) {
            this._finished = YES;
            SC.AlertPane.warn({
                message: "Records failed to update. Report this error if it recurs."
            });
            Footprint.statechart.sendEvent(this.get('recordsDidFailToUpdateEvent'), this._context);
            return;
        }

        this._recordsQueue.forEach(function(record) {
            if (record && record.get('status') & SC.Record.READY) { // === SC.Record.READY_CLEAN) { until we fix the LayerSelecdtion problem
                recordsDequeue.pushObject(record);
            }
        }, this);
        recordsDequeue.forEach(function(record) {
            record.removeObserver('status', this, 'recordStatusDidChange');
            this._recordsQueue.removeObject(record);
        }, this);

        if (this._recordsQueue.length == 0) {
            if (this._finished) // Avoid a race condition that results in two calls
                return;
            this._finished = YES;

            // All good, send the updated records to the main store
            this._nestedStore.commitChanges(YES);
            // Register an undo (if this isn't an undo) and send the recordsDidUpdateEvent
            this.recordsDidUpdate(this._context);
        }
    },

    exitState: function() {
        // Cancel any pending update in case we are about to reenter this state;
        if (this._recordsQueue.length > 0)
            this.cancelUpdate();

        this._context = null;
        // Remove observers
        this._records.forEach(function(record) {
            // Remove orphaned observers
            record.removeObserver('status', this, 'recordStatusDidChange');
        }, this);

        this._recordsQueue = null;
        this._finished = null;
    }
});

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


/***
 *  Base class for simple updating all types of records.
 *  This class allows multiple records to update any attributes.
 *  It does not support nested updates--see record_crud_states for that.
 *
*/
Footprint.RecordUpdatingState = SC.State.extend({

    // Handles another update action when already in the updating state
    // By default this enters the updatingState. Override it to disable a new update while updating is in progress
    doUpdate: function(context) {
        this.gotoState('attemptingUpdateState', context);
    },

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
            // This registers a redo!
            undoManager.registerUndo(function() {
                self.gotoState('updatingState', context)
            });
            // Sends an action that can be handled by the parent state if the context recordType matches
            Footprint.statechart.sendAction('doRecordUndo', undoContext);
        })
    },
    recordsDidError:function(context) {
        SC.AlertPane.warn({
            message: "Records failed to update. Report this error if it recurs."
        });
        Footprint.statechart.sendEvent('updateDidFail', context);
    },

    initialSubstate:'readyState',
    readyState:SC.State,

    enterState:function(context) {
        // If we have things to update, try to update them
        if (context && context.get('recordContexts'))
            Footprint.statechart.gotoState(
                '%@.attemptingUpdateState'.fmt(this.get('fullPath')),
                context);
        // Otherwise do nothing
    },

    attemptingUpdateState:SC.State.extend({
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
            var recordIds = recordContexts.map(function(recordContext) {
                return recordContext.getPath('record.id');
            });
            // Create a lookup of each record by id, mapping it to it's recordContext
            var recordContextLookup = $.mapToDictionary(recordContexts, function(recordContext) {
                return [recordContext.getPath('record.id'), recordContext]
            });

            this._nestedStore = Footprint.store.chainAutonomousStore();
            var nestedRecords = this._nestedStore.find(SC.Query.local(
                context.get('recordType'),
                "id ANY {ids}", {
                    ids: recordIds
                }));

            this._savingRecords = nestedRecords;
            this._recordsQueue = SC.Set.create(nestedRecords);
            // Prevent a race condition below
            this._finished = NO;

            // Perform our actual record updates
            nestedRecords.forEach(function(record) {
                // Add observer on each record
                record.addObserver('status', this, 'recordStatusDidChange');

                // Set attributes of record based on the key/value pairs stored with it
                var recordContext = recordContextLookup[record.get('id').toString()];

                context.get('recordType').allRecordAttributeProperties().forEach(function(attr) {
                    var value = recordContext.get(attr);
                    if (value !== undefined)
                        record.set(attr, value);

                }, this);
            }, this);

            // Commit the records to the datasource
            this._nestedStore.commitRecords(
                nestedRecords.mapProperty('storeKey').map(function(storeKey) {
                    return this._nestedStore.recordTypeFor(storeKey);
                }, this),
                nestedRecords.mapProperty('id'),
                nestedRecords.mapProperty('storeKey')
            );
            // Manually invoke observer in case everything is already done
            this.recordStatusDidChange();
        },

        recordStatusDidChange: function(sender) {
            this.invokeOnce(this._recordStatusDidChange);
        },
        _recordStatusDidChange: function() {
            var recordsDequeue = [];
            if ($.any(this._recordsQueue, function(record) {
                return record && record.get('status') === SC.Record.ERROR;
            })) {
                this._finished = YES;
                Footprint.statechart.sendEvent('recordsDidError', this._context);
                return;
            }

            this._recordsQueue.forEach(function(record) {
                if (record && record.get('status') === SC.Record.READY_CLEAN) {
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
                this._nestedStore.commitChanges();
                // Alert listeners that the records updated
                Footprint.statechart.sendEvent('recordsDidUpdate', this._context);
            }
        },

        exitState: function() {
            this._context = null;
            // Remove observers
            this._savingRecords.forEach(function(record) {
                // Remove orphaned observers
                record.removeObserver('status', this, 'recordStatusDidChange');
            }, this);

            // Destroy the nested store. If this state is superseded by another call to updatingState,
            // the previous store is destroyed here and its datasource updateRecords result will be ignored
            this._nestedStore.destroy();
        }
    })
});
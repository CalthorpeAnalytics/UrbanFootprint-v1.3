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
 * This state CRUDs all child records of record in parallel
 * @type {*}
 */
Footprint.SavingChildRecordsState = SC.State.extend({

    // React to child records completing their save operation. We don't do anything here, although we could log
    didFinishChildRecords: function(context) {
    },

    // React to the each SavingRecordState finishing. We don't want this event to percolate up to parent states.
    // The top-level state will only care when the top level record(s) finish saving.
    didFinishRecords: function(context) {
       return YES;
    },

    /***
     * Receives failure messages and sends a specific event alerting the parent records that the children have failed
     * @param context
     */
    saveRecordsDidFail: function(context) {
       Footprint.statechart.sendEvent('saveChildRecordsDidFail');
    },

    getProperties: function(record) {
    },

    initialSubstate:'readyState',
    readyState:SC.State,

    enterState:function(context) {
        this._context = context;
        var records = context.get('content');
        // Assume all records are the same recordType
        var properties = this.getProperties(records.get('firstObject'));
        this._properties = properties;
        properties.forEach(function(property) {
            // Map the property of each each record and flatten into childRecords
            // ($.map automajically flattens)
            var childRecords = $.shallowFlatten(records.mapProperty(property).map(function(x) {return x}));
            // Save each child record in a new SavingRecordState substate of savingChildrenState
            this.get('savingChildrenState').addSubstate(
                'saving%@State'.fmt(property.capitalize()),
                Footprint.SavingRecordState,
                {_context: SC.Object.create({content:childRecords, nestedStore:context.get('nestedStore')}) }
            );
        });
        this.invokeOnce('gotoSubstateIfNeeded');
    },

    /***
     * Goes to the savingChildrenState with concurrent substates if any were created.
     * Otherwise sends the didFinishChildRecords event
     */
    gotoSubstateIfNeeded: function() {
        if (this.getPath("savingChildrenState.substates.length") > 0)
            this.gotoState('savingChildrenState', this._context);
        else
            Footprint.statechart.sendEvent('didFinishChildRecords', this._context);
    },

    exitState: function(context) {
        this.getPath('savingChildrenState.substates').forEach(function(substate) {
            substate.destroy();
        }, this);
        this._properties.forEach(function(property) {
            this.set('saving%@State'.fmt(property.capitalize()), null);
        }, this);
    },

    savingChildrenState: SC.State.extend({
        substatesAreConcurrent:YES,

        enterState: function(context) {
            this._savingRecordsQueue = [];
            this._context = context;
            this.get('substates').forEach(function(substate) {
                substate.getPath('_context.content').forEach(function(childRecord) {
                    this._savingRecordsQueue.push(childRecord);
                    childRecord.addObserver('status', this, 'savingChildRecordStatusDidChange')
                }, this);
            }, this);
            this.savingChildRecordStatusDidChange();
        },

        savingChildRecordStatusDidChange:function() {
            this.invokeOnce(this._savingChildRecordStatusDidChange);
        },

        _savingChildRecordStatusDidChange:function() {
            var dequeueRecords = this._savingRecordsQueue.filter(function(childRecord) {
                if (sender.get('status') & SC.Record.READY) {
                    childRecord.removeObserver('status', this, 'savingChildRecordStatusDidChange');
                    return YES;
                }
                return NO;
            }, this);
            this._savingRecordsQueue.removeObjects(dequeueRecords);
            if (this._savingRecordsQueue.length == 0) {
                Footprint.statechart.sendEvent('didFinishChildRecords', this._context);
            }
        }
    })
});


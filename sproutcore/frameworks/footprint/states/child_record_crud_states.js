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
 * This state CRUDs all child records of record in parallel
 * @type {*}
 */
Footprint.SavingChildRecordsState = SC.State.extend({

    /***
     * The event to call upon success.
     */
    successEvent: null,
    /***
     * The name of the event to send in the event of failure
     */
    failEvent: null,

    /***
     * Handles the failure of saving child records by sending an event saveBeforeRecordsDidFail
     * @param context
     */
    saveRecordsDidFail: function(context) {
        if (this.getPath('parentState._context.content') === context.get('content')) {
            SC.Logger.debug("Handled %@".fmt(context.getPath('content.firstObject.constructor')));
            Footprint.statechart.sendEvent(this.get('failEvent', context));
            return YES;
        }
        SC.Logger.debug("Not handled");
        return NO;
    },

    didFinishChildRecords: function(context) {

        if (this.getPath('parentState._context.content') === context.get('content')) {
            SC.Logger.debug("Handled %@".fmt(context.getPath('content.firstObject.constructor')));
            // Resassign the updated records to the content to trick the content instances into
            // updating their attributes
            this.reassignUpdatedRecords(context);
            Footprint.statechart.sendEvent(this.get('successEvent'), context);
            return YES;
        }
        SC.Logger.debug("Not handled");
        return NO;
    },

    /***
     * Called in didFinishChildRecords
     * @param context
     */
    reassignUpdatedRecords: function (context) {
        // The instance reference is always updated but the attribute id is not.
        // The fix is to set the instance property to itself, which is probably harmless
        var properties = this.getProperties(context.getPath('content.firstObject'));
        context.get('content').forEach(function (content) {
            properties.forEach(function (property) {
                if (content.get(property))
                    content.writeAttribute(property, content.get(property).get('id'));
                // We could instead call writeAttribute to avoid throwing events
                //content.set(property, content.get(property));
            });
        });
    },

    /***
     * Receives failure messages and sends a specific event alerting the parent records that the children have failed
     * @param context
     */
    saveRecordsDidFail: function(context) {
       Footprint.statechart.sendEvent('saveChildRecordsDidFail', context);
    },

    getProperties: function(record) {
        throw Error("Must override");
    },

    initialSubstate:'readyState',
    readyState:SC.State,

    enterState:function() {
        // Always use the _context set in the parentState, not the passed in context. This matters when recursing because
        // concurrent sessions receive the context of the concurrent base state, which we don't want
        var context = this._context = this.getPath('parentState._context');
        var records = context.get('content');
        // Assume all records are the same recordType
        var properties = this.getProperties(records.get('firstObject'));
        this._properties = properties;

        // Save each child record in a new SavingRecordState substate of savingChildrenState
        var savingChildrenState = this.getState('%@.savingChildrenState'.fmt(this.get('fullPath')));
        properties.forEach(function(propertyPath) {
            // Map the property of each each record and flatten into childRecords
            // It's possibly to have no child records if the property on all records is null or empty
            var childRecords = $.shallowFlatten(mapPropertyPath(records, propertyPath)).compact();
            if (childRecords.length > 0) {
                var substateName = 'saving%@State'.fmt(propertyPath.capitalize().camelize());
                if (savingChildrenState.getState(substateName)) {
                    // For some reason, the child state sometimes already exists
                    var substate = savingChildrenState.getState(substateName);
                    // Just update the context
                    substate._context = SC.Object.create({content:childRecords, nestedStore:context.get('nestedStore')});
                    // Use flag until we can destroy them
                    substate._active = YES;
                }
                else {
                    savingChildrenState.addSubstate(
                        substateName,
                        Footprint.SavingRecordState,
                        // These are attributes of the state, not the context passed to its enter state
                        // We need to make sure that _context overrules the context passed in, since that will be the parent's
                        // Therefor SavingRecordState.enterState prioritizes the _context
                        {_context: SC.Object.create({content:childRecords, nestedStore:context.get('nestedStore')}), _active:YES }
                    );
                }
            }
        }, this);
        this.invokeOnce('gotoSubstateIfNeeded');
    },

    /***
     * Goes to the savingChildrenState with concurrent substates if any were created.
     * Otherwise sends the didFinishChildRecords event
     */
    gotoSubstateIfNeeded: function() {
        if (this.getPath("savingChildrenState.substates.length") > 0)
            this.gotoState('%@.savingChildrenState'.fmt(this.get('fullPath')), this._context);
        else
            Footprint.statechart.sendEvent('didFinishChildRecords', this._context);
    },

    savingChildrenState: SC.State.extend({
        substatesAreConcurrent:YES,

        enterState: function(context) {
            this._savingRecordsQueue = [];
            this._context = context;
            this.get('substates').forEach(function(substate) {
                if (!substate._active)
                    return;

                // TODO
                // This should never be undefined, but sometimes is when we reenter substates
                // Hopefully the solution is to property destroy the child states each time
                (substate.getPath('_context.content') || []).forEach(function(childRecord) {
                    this._savingRecordsQueue.push(childRecord);
                }, this);
            }, this);
            if (this._savingRecordsQueue.length == 0) {
                // No records to save
                Footprint.statechart.sendEvent('didFinishChildRecords', this._context);
            }
        },
        exitState: function(context) {
            // Destroy dynamic child substates on exit so we can recreate them on the next run
            // TODO this causes instability
            /*
            this.getPath('substates').forEach(function (substate) {
                substate.destroy();
                this.set(substate.get('name'), undefined);
            }, this);
            */
            this._savingRecordsQueue = null;
            this._context = null;
        },

        /**
         * Respond to a child state finishing
         * @param context
         */
        didFinishRecords: function(context) {
            var handled = NO;
            this.get('substates').forEach(function(substate) {
                if (!substate._active)
                    return;

                if (!handled && substate.getPath('_context.content') == context.get('content')) {
                    handled = YES;
                    SC.Logger.debug("Handled %@".fmt(context.getPath('content.firstObject.constructor')));
                    var dequeueRecords = [];
                    substate.getPath('_context.content').forEach(function(childRecord) {
                        dequeueRecords.push(childRecord);
                    }, this);
                    this._savingRecordsQueue.removeObjects(dequeueRecords);
                    if (this._savingRecordsQueue.length == 0) {
                        Footprint.statechart.sendEvent('didFinishChildRecords', this._context);
                    }
                }
            }, this);
            if (handled)
                return YES;
            SC.Logger.debug("Not handled");
            return NO;
        }
    })
});


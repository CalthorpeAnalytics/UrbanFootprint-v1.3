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

Footprint.SavingRecordState = SC.State.extend({
    _active:YES,
    doCancel: function() {
        this.gotoState('noModalState');
    },

    initialSubstate: 'savingBeforeRecordsState',

    //Don't send event
    startingCrudState: function(context) {
    },
    /***
     *
     * @param context - contains the nestedStore to be used for the buffered save and the content, which is an
     * array of one or more records to save
     */
    enterState:function(context) {
        // If we enter this as a dynamic substate (for recursion), this_context will already be set, so we ignore the passed in parent context
        this._context = this._context || context;

        this.startingCrudState(this._context);

        if (!this._context.get('nestedStore'))
            throw Error("No nested store");
    },

    exitState: function() {
        this._context = null;
        this._active = NO;
    },

    /***
     * Saves all records of a properties that need to be saved before the main records are saved.
     * This is important in the create case where a dependent record needs to be created first.
     * For instance if a record type BuiltForm has a property Medium, the Medium should be created
     * before the BuiltForm so that the BuiltForm can reference it when it is created.
     *
     * All child records are saved concurrently. Thus if there are m main records that have p properties that
     * each have an array or c (child) records, then m*p*c records will be saved concurrently.
     */
    savingBeforeRecordsState:Footprint.SavingChildRecordsState.extend({

        enterState:function() {
            if (!this.getPath('parentState._active'))
                return;
            sc_super()
        },
        successEvent: 'didFinishBeforeRecords',
        failEvent: 'saveBeforeRecordsDidFail',
        getProperties: function(record) {
            return record._saveBeforeProperties();
        },
        didFinishBeforeRecords: function(context) {
            if (this.getPath('_context.content') === context.get('content')) {
                SC.Logger.debug("Handled %@".fmt(context.getPath('content.firstObject.constructor')));
                this.gotoState('%@.savingMainRecordState'.fmt(this.getPath('parentState.fullPath')), context);
                return YES;
            }
            SC.Logger.debug("Not handled");
            return NO;
        }
    }),

    /***
     * Saves the main record(s). Sends the event saveRecordsDidFail if something goes wrong.
     */
    savingMainRecordState:SC.State.extend({

        didFinishMainRecords: function(context) {

            if (context.get('content') === this._context.get('content')) {
                SC.Logger.debug("Handled %@".fmt(context.getPath('content.firstObject.constructor')));
                this.gotoState('%@.savingAfterRecordsState'.fmt(this.getPath('parentState.fullPath')), context)
                return YES;
            }
            SC.Logger.debug("Not handled");
            return NO;
        },

        /***
         * Handles errors in persisting records by calling saveRecordsDidFail.
         * This is in turn handled by savingBeforeRecordState, savingAfterRecordState if these records where
         * part of a child record save operation.
         * @param context
         * @returns {*}
         */
        mainRecordsDidError:function(context) {
            Footprint.statechart.sendEvent('saveRecordsDidFail', context);
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

            var nestedStore = this.getPath('parentState._context.nestedStore');
            nestedStore.discardChanges();
            return NO;

            // Use the undoContext to reset each records values
            /**
             * TODO TEST
            var undoContext = this._context.getPath('parentState.undoContext');
            // Just like when we prepare for the update, except instead update the records
            // according to the undoContext.
            if (undoContext)
                this.updateRecordsToContexts(undoContext.get('recordContexts'));
             **/
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

        enterState: function(context) {
            this._context = this.getPath('parentState._context');
            // commitRecords from changelog of nestedStore
            var nestedStore = this.getPath('parentState._context.nestedStore');
            var records = this.getPath('parentState._context.content');

            var templateRecord = records.get('firstObject');
            // Get properties that should be removed from the instance for saving.
            // They will be added back on after
            var deferredProperties = templateRecord._saveAfterProperties();
            if (deferredProperties.get('length') > 0) {
                records.forEach(function(record) {
                    // If any save after properties are new or dirty, tell the record to defer publishing
                    if ((typeof(record.get('no_post_save_publishing')) != 'undefined') &&
                        deferredProperties.find(function(property) {
                            return [SC.Record.READY_DIRTY, SC.Record.READY_NEW].contains(record.get(property).get('status'));
                        }, this)) {

                        record.set('no_post_save_publishing', YES);
                    }

                }, this);
            }
            // To prevent trying to save newly cloned records before the main record,
            // create a lookup of each record storeKey to a dict with a key and value for each cloneProperty
            // The key is the property and the value is the cloned property value
            // In the process the record property is temporary nulled out
            // These cloned properties will be reassigned to the record after for post main record saving
            this._deferredPropertyLookup = $.mapToDictionary(
                records,
                function(record) {
                    return [
                        // key by store key
                        record.get('storeKey'),
                        // value by a dict keyed by property and valued by instance
                        $.mapToDictionary(deferredProperties, function(propertyPath) {
                            var value = record.getPath(propertyPath);
                            if (value && value.isEnumerable) {
                                // If enumerable, extract the items so we don't maintain the ManyArray which will be cleared
                                // during the save/reload
                                value = value.toArray();
                                record.getPath(propertyPath).removeObjects(value);
                            }
                            else {
                                record.setPath(propertyPath, null);
                            }
                            return [propertyPath, value];
                        })
                    ];
                }
            );

            records.forEach(function(record) {
                record.addObserver('status', this, 'recordStatusDidChange');
            }, this);

            this._recordsQueue = SC.Set.create(records);
            // Prevent a race condition below
            this._finished = NO;
            this.recordStatusDidChange();

            nestedStore.commitRecords(
                records.map(function(record) {
                    return nestedStore.recordTypeFor(record.get('storeKey'));
                }, this),
                null,
                records.mapProperty('storeKey')
            );
        },
        recordStatusDidChange: function() {
            this.invokeOnce(this._recordStatusDidChange);
        },
        _recordStatusDidChange: function() {
            if (this._finished)
                return;

            if ($.any(this._recordsQueue, function(record) {
                return record && record.get('status') === SC.Record.ERROR;
            })) {
                // Give up on any more processing of records in this scope.
                this._finished = YES;
                Footprint.statechart.sendEvent('mainRecordsDidError', this.getPath('parentState._context'));
            }

            var nestedStore = this.getPath('_context.nestedStore');
            var recordsDequeue = this._recordsQueue.filter(function(record) {
                // Detect coding errors where instances are dirtied by observers right away
                if ((record.get('status') & SC.Record.READY) && record.get('status') != SC.Record.READY_CLEAN)
                    logWarning("Saved recordType %@ of id %@ was dirtied by an observer upon reload. Track this down and fix".fmt(record.constructor, record.get('id')));
                return record && record.get('status') & SC.Record.READY;
            }, this);
            recordsDequeue.forEach(function(record) {
                record.removeObserver('status', this, 'recordStatusDidChange');
                this._recordsQueue.removeObject(record);
            }, this);

            if (this._recordsQueue.length == 0) {
                // Restore the deferred properties
                $.each(this._deferredPropertyLookup, function(storeKey, propertyLookup) {
                    var record = nestedStore.materializeRecord(storeKey);
                    // The record will not exist if it was removed from the store by a delete operation
                    if (record) {
                        $.each(propertyLookup, function(key, value) {
                            // Since we detached the property values, they don't pick up the new id of the saved
                            // records. So use the inverse property to assign the reference back to the reference
                            // if present.
                            var segments = key.split('.');
                            var propertyPath = segments.slice(0,-1).join('.');
                            var property = segments.slice(-1)[0];
                            var resolvedRecord = segments.get('length') > 1 ? record.getPath(propertyPath) : record;

                            // Use the normal inverse property or our special softInverse if we couldn't set the inverse property on the field, due to polymorphism problems
                            var inverseProperty = resolvedRecord[property].inverse || resolvedRecord[property].softInverse;
                            if (value.isEnumerable) {
                                resolvedRecord.get(property).removeObjects(resolvedRecord.get(property));
                                value.forEach(function(item) {
                                    if (inverseProperty)
                                        item.set(inverseProperty, resolvedRecord);
                                });
                                resolvedRecord.get(property).pushObjects(value);
                            }
                            else
                                if (inverseProperty) {
                                    value.set(inverseProperty, resolvedRecord);
                                    resolvedRecord.setPath(property, value);
                                }
                        });
                    }
                });
                // Mark the state as finished to avoid race conditions
                this._finished = YES;
                // Announce that the main records finished.
                // At this point the state is no longer active (I forget why), so we
                // send an event which the active version of the state processes.
                Footprint.statechart.sendEvent('didFinishMainRecords', this._context);
            }
        }
    }),

    savingAfterRecordsState:Footprint.SavingChildRecordsState.extend({
        successEvent: 'didFinishRecords',
        failEvent: 'saveAfterRecordsDidFail',
        getProperties: function(record) {
            return record._saveAfterProperties();
        }
    })
});

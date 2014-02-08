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
sc_require('state/child_record_crud_states');

Footprint.SavingRecordState = SC.State.extend({
    doCancel: function() {
        this.gotoState('modalState.readyState');
    },

    initialSubstate: 'savingBeforeRecordsState',

    /***
     *
     * @param context - contains the nestedStore to be used for the buffered save and the content, which is an
     * array of one or more records to save
     */
    enterState:function(context) {

        this._context = context;
        if (!this._context.get('nestedStore'))
            throw Error("No nested store");
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

        /***
         * Handles the failure of saving child records by sending an event saveBeforeRecordsDidFail
         * @param context
         */
        saveRecordsDidFail: function(context) {
            Footprint.statechart.sendEvent('saveBeforeRecordsDidFail', context);
        },

        didFinishChildRecords: function(context) {
            if (this.getPath('parentState._context.content') === context.get('content')) {
                this.gotoState('savingMainRecordState', context);
                return YES;
            }
            return NO;
        },

        getProperties: function(record) {
            return record._saveBeforeProperties();
        }
    }),

    /***
     * Saves the main record(s). Sends the event saveRecordsDidFail if something goes wrong.
     */
    savingMainRecordState:SC.State.extend({

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

        enterState: function(context) {
            // commitRecords from changelog of nestedStore
            var nestedStore = this.getPath('parentState._context.nestedStore');
            var records = this.getPath('parentState._context.content');

            var cloneProperties = records.getPath('firstObject._cloneProperties')();

            // To prevent trying to save newly cloned records before the main record,
            // create a lookup of each record storeKey to a dict with a key and value for each cloneProperty
            // The key is the property and the value is the cloned property value
            // In the process the record property is temporary nulled out
            // These cloned properties will be reassigned to the record after for post main record saving
            this.recordToClonePropertyHashes = $.mapToCollectionsObject(
                records,
                function(record) {
                    return record.get('storeKey');
                },
                function(record) {
                    cloneProperties.map(function(cloneProperty) {
                        var cloneValue = record.get(cloneProperty);
                        record.set(cloneProperty, record[cloneProperty].kindOf(SC.ManyAttribute) ? [] : null);
                        return {key:cloneProperty, value:cloneValue};
                    });
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

            var nestedStore = this.getPath('parentState._context.nestedStore');
            var recordsDequeue = this._recordsQueue.filter(function(record) {
                return record && record.get('status') === SC.Record.READY_CLEAN;
            }, this);
            recordsDequeue.forEach(function(record) {
                record.removeObserver('status', this, 'recordStatusDidChange');
                this._recordsQueue.removeObject(record);
            }, this);

            if (this._recordsQueue.length == 0) {
                $.each(this.recordToClonePropertyHashes, function(storeKey, propertyHashes) {
                    var record = nestedStore.materializeRecord(storeKey);
                    propertyHashes.forEach(function(propertyHash) {
                        record.set(propertyHash.key, propertyHash.value);
                    });
                });
                // Mark the state as finished to avoid race conditions
                this._finished = YES;
                this.gotoState('savingAfterRecordsState', this.getPath('parentState._context'));
            }
        }
    }),

    savingAfterRecordsState:Footprint.SavingChildRecordsState.extend({
        /***
         * Handles the failure of saving child records by sending an event saveAfterRecordsDidFail
         * @param context
         */
        saveChildRecordsDidFail: function(context) {
            Footprint.statechart.sendEvent('saveAfterRecordsDidFail', context);
        },

        didFinishChildRecords: function(context) {
            if (this.getPath('parentState._context.content') === context.get('content')) {
                Footprint.statechart.sendEvent('didFinishRecords', context);
                return YES;
            }
            return NO;
        },

        getProperties: function(record) {
            return [];
            // Handle on server for now
            //return record._saveAfterProperties();
        }
    })
});

/***
 * The state of preparing records for create or update. Implentors of this state
 * should respond to a save action by going to the substate savingRecordState.
 * @type {*}
 */
Footprint.EditingRecordState = SC.State.extend({
    _infoPanes: [],

    enterState:function(context) {
        this._context = context;
        // This will be the record(s) to clone or null for the new case
        var recordType = context.get('recordType');
        this._recordType = recordType;
        this._content = context.get('activeRecord') || nestedStore.createRecord(recordType, {});
        var infoPanesCache = this._infoPanes;
        var infoPane = infoPanesCache[recordType.toString()] || Footprint.FeatureInfoView.create({
            recordType:recordType,
            nowShowing:'Footprint.FeatureSummaryInfoView'
        });
        infoPanesCache[recordType.toString()] = infoPane;
        infoPane.set('content', this._content);
        infoPane.append();
        this._infoPane = infoPane;
    },

    initialSubstate:'setupState',
    setupState: SC.State.extend({
        enterState:function() {
            this.gotoState('loadingRecordsState', this.get('parentState')._context);
        }
    }),

    loadingRecordsState:Footprint.LoadingRecordsState.extend({
        didLoadRecords: function() {
            this.gotoState('%@.readyState'.fmt(this.getPath('parentState.fullPath')), this._context);
        }
    }),

    /***
     * Override this to set up the record(s) for editing, either adding or updating
     */
    readyState:null,

    savingRecordState: Footprint.SavingRecordState,

    exitState:function() {
        this._infoPane.set('content', null);
        this._infoPane.remove();
        this._nestedStore.destroy();
        this._nestedStore = null;
        Footprint.recordEditController.set('content', null);
    }
});


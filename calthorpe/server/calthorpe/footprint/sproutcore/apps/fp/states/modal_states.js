
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
sc_require('states/record_crud_states');
sc_require('states/querying_states');

Footprint.ModalState = SC.State.extend({
    initialSubstate:'readyState',

    doCancel: function() {
        this.gotoState('%@.readyState'.fmt(this.get('fullPath')));
    },

    /***
     * The initial state readyState responds to all actions when a modal window is not displayed
     */
    readyState:SC.State.extend({
        /***
         * Create a brand spankin' new record with minimum attributes copied from the context.
         * @param context - context.activeRecord is the is the context that is minimally copied
         */
        doNewRecord:function(context) {
            this.gotoState('addingRecordState', SC.Object.create(context, {newRecord:YES}));
        },
        /***
         * Create a new record by cloning the record in the context
         * @param context - context.activeRecord is cloned
         */
        doAddRecord:function(context) {
            this.gotoState('addingRecordState', context);
        },
        /***
         * Edt the record in the context
         * @param context - context.activeRecord is used for the editing states
         */
        doEditRecord:function(context) {
            this.gotoState('updatingRecordState', context);
        },
        /***
         * Query based on the recordType in the context
         * @param context - context.recordType is the type of record used for the querying states
         */
        doQueryRecords: function(context) {
            this.gotoState('queryingRecordsState', context);
        }
    }),

    addingRecordState:Footprint.EditingRecordState.extend({

        /***
         * Called when all records, including children have completed creation
         * @param context
         */
        didFinishRecords: function(context) {
            // Goto our readyState so that the user can update what they just created, if desired.
            this.gotoState('%@.readyState'.fmt(this.getPath('parentState.fullPath')), context);
        },

        /***
         * Called when the main records being saved fail (as opposed to child records).
         */
        saveRecordsDidFail: function(context) {
            SC.AlertPane.warn({
                message: "Failed to create records. Report this error if it recurs.",
                description: "Record Types: %@".fmt(uniqueRecordTypes(context.get('nestedStore'), context.get('content')).join(', '))
            });
            // Goto our readyState so that the user can attempt to update again.
            this.gotoState('%@.readyState'.fmt(this.getPath('parentState.fullPath')), context);
        },
        saveBeforeRecordsDidFail: function(context) {
            SC.AlertPane.warn({
                message: "Failed to create prerequisite records. Report this error if it recurs.",
                description: "Record Types: %@".fmt(uniqueRecordTypes(context.get('nestedStore'), context.get('content')).join(', '))
            });
        },
        saveAfterRecordsDidFail: function(context) {
            SC.AlertPane.warn({
                message: "Failed to create dependent records. Report this error if it recurs.",
                description: "Record Types: %@".fmt(uniqueRecordTypes(context.get('nestedStore'), context.get('content')).join(', '))
            });
        },


        readyState:SC.State.extend({
            enterState:function(context) {
                // If we are not re-entering this state after a successful save or failure, set up the nested store
                // and clone the record
                var nestedStore, clonedRecord;
                if (!this.getPath('parentState._nestedStore')) {
                    nestedStore = Footprint.store.chainAutonomousStore();
                    this.setPath('parentState._nestedStore', nestedStore);
                    this._content = this.getPath('parentState._content');
                    var nestedRecord = nestedStore.materializeRecord(this._content.get('storeKey'));
                    clonedRecord = nestedRecord.cloneRecord(this._content);
                    // If we are cloning, use the record type's _cloneSetup function to copy over
                    // values only used for cloning
                    if (!context.get('newRecord'))
                        clonedRecord._cloneSetup(this._content);
                    // TODO no need to use a public controller here. Switch to private variable
                    Footprint.recordEditController.set('content', clonedRecord);
                }
                else {
                    clonedRecord = Footprint.recordEditController.get('content');
                    nestedStore = this.getPath('parentState._nestedStore');
                    // If we came in from an error, reset the record to dirty so that the user can try to save again
                    changeRecordStatus(nestedStore, clonedRecord, SC.Record.ERROR, SC.Record.READY_DIRTY);
                }
            },
            doSave: function() {
                this.gotoState('savingRecordState',
                    SC.Object.create({
                        content:[Footprint.recordEditController.get('content')],
                        nestedStore: this.getPath('parentState._nestedStore')
                    }));
            }
        })
    }),

    /***
     * The main state for updating existing records
    */
    updatingRecordState:Footprint.EditingRecordState.extend({

        /***
         * Called when all records, including children have completed creation
         * @param context
         */
        didFinishRecords: function(context) {
            // Goto our readyState so that the user can further update what they just updated, if desired.
            this.gotoState('readyState', context);
        },

        /***
         * Called when the main records being saved fail (as opposed to child records).
         */
        saveRecordsDidFail: function(context) {
            SC.AlertPane.warn({
                message: "Failed to update records. Report this error if it recurs.",
                description: "Record Types: %@".fmt(uniqueRecordTypes(context.get('nestedStore'), context.get('content')).join(', '))
            });
            // Goto our readyState so that the user can attempt to update again.
            this.gotoState('readyState', context);
        },
        saveBeforeRecordsDidFail: function(context) {
            SC.AlertPane.warn({
                message: "Failed to update prerequisite records. Report this error if it recurs.",
                description: "Record Types: %@".fmt(uniqueRecordTypes(context.get('nestedStore'), context.get('content')).join(', '))
            });
        },
        saveAfterRecordsDidFail: function(context) {
            SC.AlertPane.warn({
                message: "Failed to update dependent records. Report this error if it recurs.",
                description: "Record Types: %@".fmt(uniqueRecordTypes(context.get('nestedStore'), context.get('content')).join(', '))
            });
        },

        readyState:SC.State.extend({
            enterState:function(context) {
                var nestedStore = Footprint.store.chainAutonomousStore();
                this.setPath('parentState._nestedStore', nestedStore);
                this._content = this.get('parentState')._content;
                var nestedContent = nestedStore.find(SC.Query.local(
                    this.getPath('parentState._recordType'),
                    "id ANY {ids}", {
                    ids: this._content.mapProperty('id')
                }));
                Footprint.recordEditController.set('content', nestedContent);
            },
            doSave: function() {
                this.gotoState('savingRecordState',
                    SC.Object.create({
                        content:Footprint.recordEditController.get('content'),
                        nestedStore: this.getPath('parentState._nestedStore')
                    }));
            }
        })
    }),

    queryingRecordsState:Footprint.QueryingRecordsState
});

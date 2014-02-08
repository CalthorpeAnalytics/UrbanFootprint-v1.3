
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
 * A state designed to run concurrently with other states, but ready to handle removing records
 * @type {*}
*/
Footprint.RecordRemovingState = SC.State.extend({

    /***
     * Called to commence removing a record.
     * @param context - SC.Object with the following:
     *  content - An array of records to be removed
     *  recordType - The recordType of the records
     *  undoManager = The undoManager of for the records
     */
    doRemoveRecord: function(context) {
        this.gotoState('showingAlertState', context)
    },
    /***
     * Called after the user accepts the warning message to proceed with the removal
     * @param context
     */
    doProceedWithRemoveRecord:function(context) {
        this.gotoState('removingRecordState', context);
    },

    /***
     * Cancels the remove and returns to this state to the readyState
     * @param context
     */
    doCancelRemoveRecord:function(context) {
        this.gotoState('readyState');
    },

    initialSubstate:'readyState',

    /***
     * Hang out here until a remove record action is taken.
     */
    readyState: SC.State,

    /***
     * Pops up a dialog box to warn the user about removing. Cotains a cancel and proceed button
     */
    showingAlertState: SC.State.extend({

        /***
         * Delegate function that handles alert pane dismissal
         * @param pane
         * @param status
         */
        alertPaneDidDismiss: function(pane, status) {
            switch(status) {
                // Bravely proceed
                case SC.BUTTON1_STATUS:
                    Footprint.statechart.sendAction('doProceedWithRemoveRecord', this._context);
                    break;
                // Cancel
                case SC.BUTTON2_STATUS:
                    Footprint.statechart.sendAction('doCancelRemoveRecord');
                    break;
            }
        },

        enterState: function(context) {
            this._context = context;
            SC.AlertPane.warn({
                message: "You are about to remove the following item%@: %@. All data will remain intact on the server.".fmt(
                    context.getPath('content.length') > 1 ? 's' : '', // TODO auto-pluralize
                    context.get('content').mapProperty('name').split(', ')
                ),
                description: "",
                caption: "",
                delegate: this,
                buttons: [
                    { title: "Cancel" },
                    { title: "Proceed" }
                ]
            });
        },

        exitState: function() {
            this._context = null;
        }
    }),

    removingRecordState: Footprint.RecordUpdatingState.extend({
        enterState: function(context) {
            var removingContext = SC.Object.create({
                // The undoManager for the records as defined in the context
                undoManager: context.get('undoManager'),
                undoContext: this._undoContext(context),
                recordType: context.get('recordType'),
                // An array of each record to be updated along with the deleted attribute set to YES
                recordContexts:context.get('content').map(function(record) {
                    return SC.Object.create({
                            record:record
                        },
                        {deleted:YES}
                    )
                })
            });
        },
        // Context to undo the delete
        _undoContext: function(context) {
            return SC.Object.create({
                undoManager: context.get('undoManager'),
                recordType: context.get('recordType'),
                // An array of each record to be updated along with the deleted attribute set back to NO
                recordContexts:context.get('content').map(function(record) {
                    return SC.Object.create({
                            record:record
                        },
                        {deleted:NO}
                    )
                })
            })
        }
    })
});

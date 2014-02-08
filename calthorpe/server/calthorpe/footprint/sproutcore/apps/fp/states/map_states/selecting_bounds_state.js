
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
Footprint.SelectingBoundsState = SC.State.extend({

    enterState: function(context) {
        // Disable apply, info, etc until the features are ready again
        Footprint.toolController.set('featurerIsEnabled', NO);
        // Start off by checking the bounds for changes to prime the pump
        Footprint.statechart.sendAction('doTestSelectionChange', context);
    },

    // Stores the most recently selected bounds so that when a new doTestSelectionChange happens we
    // can check to see if the bounds actually changed
    _bounds:null,

    // Triggered by a timer (box) or points (polygon) or whatever. Is
    // also run when entering the state in case the layer selection is already set to something
    doTestSelectionChange: function(context) {
        var time = new Date().getTime();
        if (!context)
            return;
        if ((this._bounds == context.get('bounds') && time-this._time > 500) ||
            context.selectionWantsToEnd) {
            // If a change occurred since last save (geoms, query doesn't match, etc),
            // and a decent amount of time has passed or the selection wants to end,
            // goto the savingSelectionState substate in order to update the server
            // The context might include a selectionWantsToEnd, which savingSelectionState will handle
            this._time = time;
            this._bounds = context.get('bounds');
            this.gotoState('savingSelectionState', context); // just forward the context arg
        }
    },

    // doStartSelecting doesn't need to be handled here, because any time the user re-starts selecting,
    // they will have first ended or cleared the selection.

    // Event thrown by substates when they've decided that we're ready to end selecting.
    selectionDidEnd: function(context) {
        if (!context.getPath('features.length'))
            // If there are no features selected
            this.gotoState('noSelectionState');
        else
            // Selection is ready to load the full Features
            this.gotoState('selectionIsReadyState');
    },

    // Tell the map controller whenever a new selection layer is ready
    selectionDidUpdate:function(context) {
        Footprint.mapController.refreshSelectionLayer();
        if (context.get('selectionWantsToEnd')) {
            // Send the layerSelection as the context
            Footprint.statechart.sendEvent('selectionDidEnd', context.get('content'));
        }
    },
    selectionDidError: function(context) {
        // If selection wants to end, throw an error message to the user.
        if (context && context.get('selectionWantsToEnd')) {
            SC.AlertPane.error({
                message: 'A selection error occurred',
                description: 'There was an error processing your selection. You can try selecting fewer features.'
            });
        }
        // Either way, run selectionDidUpdate.
        // slight hack... an errored selection behaves the same as an updated selection + error message... so
        // we keep it internal here rather than routing it through an action call.
        this.selectionDidUpdate(context);
    },

    initialSubstate:'vampingState', // Good chance we'll immediately go to saving, but that's the job of doTestSelectionChange above.

    // If we don't have anything to save (e.g. incomplete polygon) or nothing's changed
    // since we last successfully saved, we just hang out here waiting for doEndSelecting.
    vampingState:SC.State.extend({
        doEndSelecting: function(context) {
            Footprint.statechart.sendEvent('selectionDidEnd', context);
        }
    }),

    savingSelectionState: Footprint.SavingSelectionState
});

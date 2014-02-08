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


// Saves the current selected geometry to the LayerSelection instance and possibly ends the selection
// process.
Footprint.SavingSelectionState = SC.State.extend({
    doEndSelecting: function() {
        this._selectionWantsToEnd = YES;
        Footprint.statechart.sendEvent('selectionDidEnd');
    },

    enterState: function(context) {
        // This might be the last save. (see doClearSelection above)
        if (context && context.selectionWantsToEnd) {
            this._selectionWantsToEnd = YES;
        }
        this._nestedStore = Footprint.store.chainAutonomousStore();
        this._layerSelection = this._nestedStore.materializeRecord(Footprint.layerSelectionActiveController.get('storeKey'));
        // Pass one in the bounds or query. Only one or none will be non-null
        this._layerSelection.set('bounds', context.get('bounds'));
        this._layerSelection.set('query', context.get('query'));
        this._layerSelection.set('aggregates', context.get('aggregates'));
        this._layerSelection.set('groupBy', context.get('groupBy'));
        this._layerSelection.set('joins', context.get('joins'));

        this._layerSelection.addObserver('status', this, 'selectionStatusDidChange');
        this._nestedStore.commitRecord(
            [Footprint.LayerSelection],
            this._layerSelection.get('id'),
            this._layerSelection.get('storeKey')
        );
    },

    selectionStatusDidChange: function() {
        if (this._layerSelection.get('status') & SC.Record.READY) {
            // Commit changes in nested store to get them up to the parent store
            this._nestedStore.commitChanges();
            Footprint.statechart.sendEvent('selectionDidUpdate', SC.Object.create({
                selectionWantsToEnd: this._selectionWantsToEnd,
                content:this._layerSelection
            }));
        }
        else if (this._layerSelection.get('status') === SC.Record.ERROR) {
            Footprint.statechart.sendEvent('selectionDidError', SC.Object.create({
                selectionWantsToEnd: this._selectionWantsToEnd,
                content:this._layerSelection
            }));
        }
        // Otherwise, we keep waiting.
    },

    exitState: function() {
        this._layerSelection.removeObserver('status', this, 'selectionStatusDidChange');
        // Destroy the nested store (whether or not it's completed saving).
        // If we enter the state again before the previous version of the state exits, it will force the previous to exit
        this._nestedStore.destroy();
        this._selectionWantsToEnd = null;
    }
});

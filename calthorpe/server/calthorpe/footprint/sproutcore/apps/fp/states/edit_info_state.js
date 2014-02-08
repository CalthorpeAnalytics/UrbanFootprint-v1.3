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

// Simple statuses for the controller. This could be moved to a state class in the future
Footprint.EDIT_LOADING_CREATE = 'loading_create';
Footprint.EDIT_READY_CREATE= 'edit_create';
Footprint.EDIT_LOADING_UPDATE = 'loading_update';
Footprint.EDIT_READY_UPDATE = 'ready_update';
Footprint.EDIT_NOT_READY = 'not_ready';

/***
 * Provides states to track the opening, editing, and saving of info panes and their associated records.
 * @type {*}
 */
Footprint.EditInfoState = SC.State.extend({
    editController: null,
    editPane: null,
    initialSubstate:'readyState',

    readyState: SC.State,

    doEdit: function(context) {
        if (context.get('content').instanceOf(this.getPath('editController.recordType'))) {
            this.gotoState('loadingState', context);
            return YES;
        }
        else
            return NO;
    },

    loadingState: SC.State.extend({

        enterState: function(context) {
            var editController = this.getPath('parentState.editController');
            var content = context ? context.get('content'): null;
            if (content.get('status') & SC.Record.READY) {
                this.gotoState('editingState', context);
            }
            else {
                this._context = context;
                content.addObserver('status', this, 'checkContentStatus');
            }
            if (!this.get('editPane')) {
                this.setPath('parentState.editPane', SC.objectForPropertyPath(this.get('editPanePath')));
            }
            var editPane = this.get('editPane');
            // TODO Show loading thingy
        },

        checkContentStatus: function() {
            if (this._context.getPath('content.status') & SC.Record.READY) {
                this.gotoState('editingState', this._context);
            }
        },

        cancel: function() {

        },

        exitState:function() {
            this._context.get('content').removeObserver('status', this, 'checkContentStatus');
            this._context = null;
        }
    }),

    editingState: SC.State.extend({
        enterState: function(context) {
            var content = context.get('content');
            var editController = this.getPath('parentState.editController');
            var nestedStore = Footprint.store.chain();
            editController.set('nestedStore', nestedStore);

            var nestedStoreContent = nestedStore.find(SC.Query.local(
                editController.get('recordType'),
                "storeKey ANY {keys}", {
                    keys: content.mapProperty('storeKey')
                }));
            editController.set('content', nestedStoreContent);
        },
        save: function() {
            var editController = this.getPath('parentState.editController').save();
        },
        cancel: function() {

        }
    }),
    savingState: SC.State.extend({
    }),
    errorState: SC.State.extend({
    })
});

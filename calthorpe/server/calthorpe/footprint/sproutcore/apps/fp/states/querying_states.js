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

Footprint.QueryingRecordsState = SC.State.extend({
    _infoPanes: [],

    enterState:function(context) {
        this._context = context;
        var recordType = context.get('recordType');
        var infoPanesCache = this._infoPanes;
        var infoPane = infoPanesCache[recordType.toString()] || Footprint.FeatureInfoView.create({
            recordType:recordType,
            nowShowing:'Footprint.FeatureQueryInfoView'
        });
        infoPanesCache[recordType.toString()] = infoPane;
        infoPane.append();
        this._infoPane = infoPane;
    },

    initialSubstate:'setupState',
    setupState:SC.State.extend({
        enterState: function() {
            this.gotoState('loadingRecordsState', this.get('parentState')._context);
        }
    }),

    loadingRecordsState:Footprint.LoadingRecordsState.extend({
        didLoadRecords: function() {
            this.gotoState('readyState');
        }
    }),

    readyState:SC.State.extend({
        doCancel: function() {
            this.gotoState('modalState.readyState');
        }
    }),

    exitState:function() {
        this._infoPane.set('content', null);
        this._infoPane.remove();
        Footprint.recordEditController.set('content', null);
    }
});


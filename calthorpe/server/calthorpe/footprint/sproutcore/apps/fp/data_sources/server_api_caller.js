/* 
 * UrbanFootprint-California (v1.0), Land Use Scenario Development and Modeling System.
 * 
 * Copyright (C) 2012 Calthorpe Associates
 * 
 * This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License.
 * 
 * This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * 
 * Contact: Joe DiStefano (joed@calthorpe.com), Calthorpe Associates. Firm contact: 2095 Rose Street Suite 201, Berkeley CA 94709. Phone: (510) 548-6800. Web: www.calthorpe.com
 */

sc_require('data_sources/server_api_caller');

Footprint.Request = SC.Request.extend({
    patchUrl: function(address, body) {
        var req = this.create().set('address', address).set('type', 'PATCH');
        if(body) { req.set('body', body) ; }
        return req ;
    }
});

Footprint.ServerApiCaller = SC.Object.extend({
    url: null,
    viewModel: null,
    protectedViewModel: null,
    /***
     * Creates the viewModel instance according to the structure of the JSON data
     */
    load: function(datasource, success, notificationData) {
        Footprint.Request.getUrl(this.uri)
            .set('isJSON', YES)
            .notify(datasource, success, notificationData)
            .send();
    },

    create: function(datasource, success, data) {
        // We always PATCH instead of POST so that we can support multiple objects
        // Tastypie post_list doesn't seem to actually process more than on object
        this.write(Footprint.Request.postUrl, 'PATCH', 'postUrl', datasource, success, data);
    },

    update: function(datasource, success, data) {
        this.write(Footprint.Request.patchUrl, 'PATCH', 'patchUrl', datasource, success, data);
    },

    write: function(func, method, call, datasource, success, data) {
        var storeKeys = data.storeKeys || [data.storeKey];
        Footprint.Request[call](this.uri).header($.extend({
            'Accept': 'application/json'},
            YES || method=='PATCH' ? {'X-HTTP-Method-Override': method} : {}
            )).json()
            .notify(datasource, success, data)
            .send({
                objects: storeKeys.map(function(storeKey) {
                    // Get the dataHash for the storeKey, performing any recordType specific preprocessing
                    var dataHash = this._processDataHash(data.store.readDataHash(storeKey), data.recordType);
                    // Get the parent store data hash so that we only send values that have actually changed
                    var originalDataHash = data.store.parentStore ?
                        this._processDataHash(data.store.parentStore.readDataHash(storeKey), data.recordType) :
                        null;

                    return datasource._transformSproutcoreJsonToTastypie(data.store, dataHash, originalDataHash, data.recordType);
                }, this)
            });
    },
    _processDataHash: function(dataHash, recordType) {
        if (recordType === Footprint.LayerSelection) {
            // Strip out the the features. We never want to send these.
            dataHash = $.extend({}, dataHash);
            delete dataHash.features;
        }
        return dataHash;
    },

    saveAsDraft: function(success) {
        var saveDraftUri = '%@%@'.fmt('/draft/save', uriPath);
        $.ajax(
            saveDraftUri, {
                type:'POST',
                contentType:'application/json',
                data:JSON.stringify($.merge({}, {draft:true},this.unmap())),
                success:success,
                error:function(jqXHR, textStatus, errorThrown) {}
            }
        );
    },

    revertToCurrent: function(success) {
        // TODO this could discard the draft on the server
        this.update(success)
    },
    recoverDraft: function(success) {
        var loadDraftUri = '%@%@'.fmt('/draft/load', uriPath);
        this._ajax(loadDraftUri, function(data) {
            this.update(data);
            success(data);
        });
    },
    getRevisions: function(success) {
        var loadDraftUri = '%@%@'.fmt('/draft/load', uriPath);
        this._ajax(loadDraftUri, function(data) {
            _update(data);
        });
    },

    revertToRevision: function(success) {
        var loadDraftUri = '%@%@'.fmt('/draft/load', uriPath);
        this._ajax(loadDraftUri, function(data) {
            _update(data);
        });
    },

    _ajax: function(uri, success) {
        $.getJSON(uri, success);
    },

    /***
     * Periodically save drafts to the server
     * @param delay
     */
    startSavingDrafts: function(delay) {
        var interval = setInterval(function() {
            this.saveAsDraft();
        }, delay);
        this.stopSavingDrafts = function() {
            clearInterval(interval)
        }
    },

    /***
     * Sync the data
     * @param delay
     */
    startIntervalSync: function(delay) {
        var interval = setInterval(function() {
            this.update();
        }, delay);
        this.stopIntervalSync = function() {
            clearInterval(interval)
        }
    }
});


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

Footprint.FixturesDataSource = SC.FixturesDataSource.extend(
    /** @scope CrudSample.AutoIdFixturesDataSource.prototype */ {

    /**
     * Let's simulate calling a remote server for CRUD operations
     */
    //simulateRemoteResponse: YES,

    /**
     * Assume we have a slow server that takes 1 second to respond
     */
    //latency: 5,

    /**
     * The next number to allocate to a primary key
     */
    nextNumber: 1000000,

    /**
     * Override this method so that we can allocate ID based on a number that starts at 1,000,000.  We don't start at
     * 1 because that is within range of our primary key in our fixtures.  We also want to return a number and not a
     * string.
     *
     * @param recordType
     * @param dataHash
     * @param store
     * @param storeKey
     */
    generateIdFor: function(recordType, dataHash, store, storeKey) {
        return this.nextNumber++;
    },

    loadFixturesFor: function(store, recordType, ret) {
        sc_super();
    },

        /**
     * Override _createRecords so that we can check for unique usernames
     *
     * @param store
     * @param storeKeys
     */
        /*
    _createRecords: function(store, storeKeys) {
        storeKeys.forEach(function(storeKey) {
            try {
                var id = store.idFor(storeKey),
                    recordType = store.recordTypeFor(storeKey),
                    dataHash = store.readDataHash(storeKey),
                    fixtures = this.fixturesFor(recordType);

                this.validateUniqueUsername(dataHash);

                if (!id) {
                    id = this.generateIdFor(recordType, dataHash, store, storeKey);
                }
                this._invalidateCachesFor(recordType, storeKey, id);
                fixtures[id] = dataHash;
                store.dataSourceDidComplete(storeKey, null, id);

            } catch (e) {
                // We have an error
                store.dataSourceDidError(storeKey, e);
            }
        }, this);
    },
        */

    /**
     * Override _updateRecords so that we can check for unique usernames
     * @param store
     * @param storeKeys
     */
        /*
    _updateRecords: function(store, storeKeys) {
        storeKeys.forEach(function(storeKey) {
            try {
                var hash = store.readDataHash(storeKey);
                this.validateUniqueUsername(hash);
                this.setFixtureForStoreKey(store, storeKey, hash);
                store.dataSourceDidComplete(storeKey);
            } catch (e) {
                // We have an error
                store.dataSourceDidError(storeKey, e);
            }
        }, this);
    },
        */

    /**
     * Checks if the username is unique in local store
     * This simulates checking on the server side
     *
     * @param storeKey Store key of the user record to check
     * @throws SC.Error
     */
        /*
    validateUniqueUsername: function(dataHash) {
        var username = dataHash.username;
        var query = SC.Query.local(CrudSample.UserRecord, {
            conditions: '(username = {name})',
            name: username
        });
        var userRecords = CrudSample.store.find(query);
        var count = userRecords.get('length');
        if (count == 0) {
            return;
        } else {
            if (count == 1) {
                // Check that we are not matching ourselves
                var dataHashPrimaryKey = dataHash.userId;
                if (dataHashPrimaryKey && dataHashPrimaryKey != undefined) {
                    var primaryKey = userRecords.objectAt(0).get('id');
                    if (dataHashPrimaryKey != primaryKey) {
                        throw SC.Error.desc('Username already exists', 'username');
                    }
                }
            } else {
                // Error - more than 1 match for whatever reason
                throw SC.Error.desc('Username already exists', 'username');
            }
        }
    }
        */
});

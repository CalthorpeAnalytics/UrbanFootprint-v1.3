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


// SC.Store (for nested records)
SC.Store.reopen({

     /**
    register a Child Record to the parent
  */
  registerChildToParent: function (parentStoreKey, childStoreKey, path) {
    var parentRecords, childRecords, oldPk, oldChildren, pkRef;

    // Check the child to see if it has a parent
    childRecords = this.childRecords || {};
    parentRecords = this.parentRecords || {};

    // first rid of the old parent
    oldPk = childRecords[childStoreKey];
    if (oldPk) {
      oldChildren = parentRecords[oldPk];
      if (oldChildren) // This is still a problem for db_entity.feature_behavior
        delete oldChildren[childStoreKey];
      // this.recordDidChange(null, null, oldPk, key);
    }
    pkRef = parentRecords[parentStoreKey] || {};
    pkRef[childStoreKey] = path || YES;
    parentRecords[parentStoreKey] = pkRef;
    childRecords[childStoreKey] = parentStoreKey;

    // sync the status of the child
    this.writeStatus(childStoreKey, this.statuses[parentStoreKey]);
    this.childRecords = childRecords;
    this.parentRecords = parentRecords;
  },

    writeDataHash: function (storeKey, hash, status) {

        // update dataHashes and optionally status.
        if (hash) this.dataHashes[storeKey] = hash;
        if (status) this.statuses[storeKey] = status ;

        // also note that this hash is now editable
        var editables = this.editables;
        if (!editables) editables = this.editables = [];
        editables[storeKey] = 1 ; // use number for dense array support

        var processedPaths={};
        // Update the child record hashes in place.
        if (!SC.none(this.parentRecords) ) {
            var children = this.parentRecords[storeKey] || {},
                childHash;

            for (var key in children) {
                if (children.hasOwnProperty(key)) {
                    if (hash) {
                        var childPath = children[key];
                        childPath = childPath.split('.');
                        if (childPath.length > 1) {
                            childHash = hash[childPath[0]][childPath[1]];
                        } else {
                            childHash = hash[childPath[0]];
                        }

                        if(!processedPaths[hash[childPath[0]]]){
                            // update data hash: required to push changes beyond the first nesting level
                            this.writeDataHash(key, childHash, status);
                        }
                        if(childPath.length > 1 && ! processedPaths[hash[childPath[0]]]) {
                            // save it so that we don't processed it over and over
                            processedPaths[hash[childPath[0]]]=true;

                            // force fetching of all children records by invoking the children_attribute wrapper code
                            // and then interating the list in an empty loop
                            // Ugly, but there's basically no other way to do it at the moment, other than
                            // leaving this broken as it was before
                            var that = this;
                            this.invokeLast(function(){
                                // TEMP fix, wrapping object
                                arrayOrItemToArray(that.records[storeKey].get(childPath[0])).forEach(function(it){});
                            });
                        }
                    } else {
                        this.writeDataHash(key, null, status);
                    }
                }
            }
        }

        return this;
    },

    hasBusyRecords: function() {
        return (this.changelog || []).some(function(storeKey) {
            return this.peekStatus(storeKey) & SC.Record.BUSY;
        }, this);
    },
    hasNoBusyRecords: function() {
        return !this.hasBusyRecords()
    },

    /***
     * Dump changes in the store, returning a list
     * @param recordType. Optional recordType to limit the changelog output
     * @returns {Array}
     */
    dumpChanges: function(recordType) {
        return (this.changelog || []).map(function(storeKey) {
            var record = this.materializeRecord(storeKey);
            if (!recordType || record.constructor==recordType)
                return [record.constructor, storeKey, getStatusString(record.get('status'))];
        }, this).compact();
    },
    dumpChainedChanges: function(recordType) {
        return (this.chainedChanges || []).map(function(storeKey) {
            var record = this.materializeRecord(storeKey);
            if (!recordType || record.constructor==recordType)
                return [record.constructor, storeKey, record.get('status')];
        }, this).compact();
    }
});

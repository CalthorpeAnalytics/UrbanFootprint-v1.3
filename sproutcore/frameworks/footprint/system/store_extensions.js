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


// SC.Store (for nested records)
SC.Store.reopen({
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

            if(childPath.length > 1 && ! processedPaths[hash[childPath[0]]]) {
                // save it so that we don't processed it over and over
                processedPaths[hash[childPath[0]]]=true;

                // force fetching of all children records by invoking the children_attribute wrapper code
                // and then interating the list in an empty loop
                // Ugly, but there's basically no other way to do it at the moment, other than
                // leaving this broken as it was before
                var that=this;
                this.invokeLast(function(){
                    arrayIfSingular(that.records[storeKey].get(childPath[0])).forEach(function(it){});
                });
            } else {
                this.writeDataHash(key, childHash, status);
            }
          } else {
            this.writeDataHash(key, null, status);
          }
        }
      }
    }

    return this;
  }
});

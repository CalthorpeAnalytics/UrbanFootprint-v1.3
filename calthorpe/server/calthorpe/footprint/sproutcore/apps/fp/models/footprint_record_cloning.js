
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

/****
  * Mixin to Footprint.Record that handles cloning records
*/
Footprint.RecordCloning = {

    /***
     * Clones this record. Cloning is recursive on any properties listed in _cloneProperties.
     * ToOne or ToMany properties should be listed in _cloneProperties or _copyProperties
     * Primitive attributes need not be listed. They will be copied in copyAttributes
     * cloneRecord must not be called until all deep child attributes are status READY, excepting attributes of
     * child objects that are merely being copied by reference.
     * @param store
     * @param parentClonedRecord: set for recursive calls to identify the parent cloned record. This is used to set isMaster:NO attributes back to the parentRecord
     * @returns {*} Returns the clonedRecord with a READY_NEW status.
     */
    cloneRecord: function(parentClonedRecord) {
        var newRecord = this.get('store').createRecord(
            this.get('store').recordTypeFor(this.storeKey),
            {},
            -Math.random(Math.floor(Math.random() * 99999999)));

        this._singleNonMasterProperties().forEach(function(property) {
            // Assume that any SingleAttribute property that is not master is a reference back to the self.
            // Thus set the property to the cloned parent record
            // We shouldn't have to set !isMaster
            //newRecord.set(property, parentClonedRecord);
        });

        // Copy the primitive attributes
        this.copyAttributes(newRecord);

        newRecord._cloneOrCopyChildAttributes(parentClonedRecord, this);
        return newRecord;
    },

    /***
     * Clones this record and transfers the properties to the given target.
     * Only _nonTransferableProperties, such as id and resource_id are not transfered
     * @param store
     * @param target
     * @param complete function called on completion of the operation
     */
    cloneAndTransferProperties: function(store, target, complete) {
        var clonedRecord = this.cloneRecord(store);
        $.each(clonedRecord, function(key, value) {
            if (!this.get('_nonTransferableProperties').contains(key)) {
                target.set(key, value)
            }
        });
        if (complete)
            complete();
        // The top-level clonedRecord has not further utility
        clonedRecord.destroy();
    },

    _copyMany: function(property, value) {
        // Handle many attributes
        this.get(property).pushObjects(value);
        return value;
    },
    _copyOne: function(property, value) {
        // Handle a one attribute
        this.set(property, value);
        return value;
    },
    _cloneMany: function(property, value, parentClonedRecord) {
        var store = this.get('store');
        // Clone each item of the many property normally or with the configured custom function
        var itemRecords = value.map(function(item) {
            return this._customCloneProperties()[property] ?
                this._customCloneProperties()[property](this, parentClonedRecord, item) :
                item.cloneRecord(this)
        }, this).compact();
        // Only push if no reverse relationship exists
        // TODO I don't understand this check, validate it
        if (itemRecords.length > 0 && itemRecords[0]._singleNonMasterProperties().length == 0)
            this.get(property).pushObjects(itemRecords);
        return itemRecords;
    },
    _cloneOne: function(property, value, parentClonedRecord) {
        var store = this.get('store');
        if (this._customCloneProperties()[property])
            return this._customCloneProperties()[property](this, parentClonedRecord, value);
        else {
            var clonedItem = value.cloneRecord(this);
            this.set(property,clonedItem);
            return clonedItem;
        }
    },

    /***
     * For a clonedRecord copy or clone properties from the sourceRecord
     * @param sourceRecord: Source records whose attributes we're cloning or referencing
     * @param parentClonedRecord: For child attribute records, the parent cloned record
     * @returns {*}
     * @private
     */
    _cloneOrCopyChildAttributes: function(parentClonedRecord, sourceRecord) {
        // Since we'll combine the copyProperties and clounderstandneProperties in our toProperty function below, create
        // a convenient lookup that tells us how to process each by index
        var propertyLookup = $.map(this._copyProperties(), function(property) {
            return {
                property:property,
                type:'copy',
                one:sourceRecord._copyOne,
                many:sourceRecord._copyMany
            };
        }).concat($.map(this._cloneProperties(), function(property) {
            return {
                property:property,
                type:'clone',
                one:sourceRecord._cloneOne,
                many:sourceRecord._cloneMany
            };
        }));
        propertyLookup.forEach(function(propertyInfo) {
            var propertyValue = sourceRecord.get(propertyInfo.property);
            Footprint.CloneOrCopy.create({
                sourceRecord:this,
                parentClonedRecord:parentClonedRecord,
                propertyInfo: propertyInfo,
                propertyValue: propertyValue
            });
        }, this);
    },

    /**
     * Copy any primitive attributes that are not ids and are not returned by _copyProperties(), _cloneProperties, nor _singleNonMasterProperties()
     * @param record
     * @returns {*}
     */
    copyAttributes: function(record) {
        var self = this;
        //var randomNumber = DatMath.floor(Math.random()*10e6);
        var randomNumber = SC.DateTime.create().toFormattedString('%Y_%m_%d_%H_%M_%S');
        $.each(this.attributes() || {}, function(key, value) {
            if (!['id', 'resource_uri'].concat(
                self._copyProperties(),
                self._cloneProperties(),
                self._singleNonMasterProperties(),
                $.map(self._customCloneProperties(), function(value, key) {return key;})).contains(key))
            {
                record.set(key, self._mapAttributes[key] ? self._mapAttributes[key](value, randomNumber) : value);
            }
        });
        return record;
    },

    /***
     * Recursively load all complex attributes and return a flat list. This is used to check/await statuses
     * @param record
     */
    loadAttributes: function(_alreadyFound, propertyPath) {
        _alreadyFound = _alreadyFound || SC.Set.create();
        propertyPath = propertyPath || [];

        if (_alreadyFound.contains(this))
            return;
        else
            _alreadyFound.add(this);

        var record = this;
        // Combine the keys of non-primitive attributes that need cloning and return the corresponding record value
        // Nulls are excluded
        var clonePropertyPairs = [].concat(
                this._cloneProperties(),
                $.map(this._customCloneProperties(), function(value, key) {return key;})
            ).map(function(key) {
                var value = record.get(key);
                return value ? {key:key, value:value} : null;
            }).compact();

        // Fetch separately the copy by reference attributes. We won't recurse on these
        var referencePropertyPairs = [].concat(
            this._copyProperties(),
            this._singleNonMasterProperties()
            ).map(function(key) {
                    var value = record.get(key);
                    return value ? {key:key, value:value} : null;
            }).compact().filter(function(propertyValue) {
                return propertyValue.kindOf && propertyValue.kindOf(Footprint.Record);
            });

        // Recurse on each attribute value if it is itself a record or an enumerable of records
        // Use $.map to force a flatten of the inner arrays
        // Prepend this record to the result list.
        // Nulls are excluded
        return [{key:propertyPath.join("."), value:this}].concat(referencePropertyPairs, $.map(clonePropertyPairs, function(propertyPair) {
            var propertyValue = propertyPair.value;
            var propertyKey = propertyPair.key;
            if (propertyValue.kindOf && propertyValue.kindOf(Footprint.Record)) {
                // Footprint Record instance
                return propertyValue.loadAttributes(_alreadyFound, propertyPath.concat([propertyKey]));
            }
            else if (propertyValue.isEnumerable) {
                // Enumerable
                return jQuery.map(propertyValue.toArray(), function(propertyValueItem, i) {
                    // Possibly Footprint Record instances
                    if (propertyValueItem.kindOf && propertyValueItem.kindOf(Footprint.Record)) {
                        return propertyValueItem.loadAttributes(_alreadyFound, propertyPath.concat([propertyKey, i]));
                    }
                }).compact();
            }
        }).compact())
    }
};

 Footprint.CloneOrCopy = SC.Object.extend({

     clonedRecord:null,
     parentClonedRecord: null,
     propertyInfo:null,
     propertyValue:null,
     property:null,

     clonedChildItems:null,

     init: function() {
         sc_super();
         this.set('property', this.getPath('propertyInfo.property'));
         this.set('clonedChildItems', []);
         this.cloneOrCopyProperty();
     },

     // When the child source attribute record or record array is READY_CLEAN call the many or one function where either copies or clones child property values
     // Clones will be asynchronous so we push items to _cloningChildItems and wait for them to complete
     cloneOrCopyProperty: function() {
         // We need to do this to mark toMany attributes that don't set statuses as complete, namely ChildArray
         if (!this.getPath('propertyValue.status')===SC.Record.READY_CLEAN)
            this.setPath('propertyValue.status', SC.Record.READY_CLEAN);

         var sourceRecord = this.get('sourceRecord');
         var parentClonedRecord = this.get('parentClonedRecord');
         var property = this.get('property');
         var propertyInfo = this.get('propertyInfo');
         var propertyValue = this.get('propertyValue');
         var clonedChildItems = this.get('clonedChildItems');

         if (sourceRecord[property].kindOf(SC.ManyAttribute) || sourceRecord[property].kindOf(SC.ChildrenAttribute))
             propertyInfo.many.apply(sourceRecord, [property, propertyValue, parentClonedRecord]).forEach(function(clonedItem) {
                 clonedChildItems.push(clonedItem);
             }, this);
         else {
             var clonedItem = propertyInfo.one.apply(sourceRecord, [property, propertyValue, parentClonedRecord]);
             clonedChildItems.push(clonedItem);
         }
     }
 });

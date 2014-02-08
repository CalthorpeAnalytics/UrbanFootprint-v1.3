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

sc_require('models/footprint_record_cloning');

Footprint.Status = Footprint.Status || {}
Footprint.Status.READY_NEW_CLONED = 0x204; // 516
Footprint.Record = SC.Record.extend(Footprint.RecordCloning, {
    primaryKey: 'id',

    // Used a pseudo-status property to track that cloning of new record's child items are complete
    // Each cloned child item will receive this READY_NEW_CLONED status for its _status property
    _status:null,

    properties: function() {
        return this.get('attributes') ?
            $.map(this.get('attributes'), function(value, key) {return key;}) :
            [];
    }.property('attributes'),

    //TODO local backup of record for editing. We might place this with a call to the server in the future.
    //http://www.veebsbraindump.com/2010/10/sproutcore-crud-tutorial-using-sc-tableview/
    /**
     * Return an object containing a backup of the properties
     * @returns SC.Object object containing properties to backup
     */
    backupProperties: function() {
        var self = this;
        return $.mapObjectToObject(
            this.get('attributes'),
            function(key, value) {
                return [key, self.get(key)];
            },
            function() {return SC.Object.create(); }
        );
    },

    /**
     * Restores properties from a backup crated by backupProperties().
     */
    restoreProperties: function(backup) {
        backup.forEach(function(key, value) {
            this.set(key, backup.get(key));
        }, this);
    },

    // Properties for cloneRecord to copy
    _copyProperties:function() {return ''.w();},
    // Properties for cloneRecord to clone (recursive cloneRecord)
    // Order doesn't matter unless a _customCloneProperties function makes use of a newly cloned sibling item
    _cloneProperties:function() {return ''.w();},
    // Properties that need a custom function to clone them.
    // For toOne attributes the function receives as arguments the cloned record, the parent cloned record (or null) and the original property value.
    // For toMany attributes the function is called for each item and receives as arguments the cloned record, the parent cloned record (or null), and the original item
    _customCloneProperties:function() { return {}; },

    _singleNonMasterProperties: function() {
        var self = this;
        return $.grep(this.get('properties'), function(property) {
            return self[property] && self[property].kindOf && self[property].kindOf(SC.SingleAttribute) && !self[property].isMaster;
        });
    },

    // Child attributes to save before saving this record
    _saveBeforeProperties: function() { return [] },
    // Child attributes to save after saving this record
    _saveAfterProperties: function() { return [] },

    // Mapping of primitive attributes to other values, (e.g. key: function(key, originalRecord, clonedRecord) { return key+'new';}
    _mapAttributes: { },

    // Properties that should never be transfered from one instance to another when updating the values of one instance to those (or the clones) of another
    _nonTransferableProperties: function() { return 'id resource_uri'.w(); },

    // Special actions for setting up a clone
    _cloneSetup: function(sourceRecord) {

    },
    _propertiesForNew: function() {
        return SC.Object.create();
    }
});

/***
 * Override this to limit the class name used by the subclasses to a base class name, or to use a custom name
 * @returns {string}
 */
SC.mixin(Footprint.Record, {
    apiClassName: function() {
        return null;
    },

    allRecordAttributeProperties: function() {
        var prototype = this.prototype;

        var filteredProperties = $.map(prototype, function (value, key) {
            return value && value.kindOf && value.kindOf(SC.RecordAttribute) ?
                key :
                null;
        }).compact();
        var parentRecordType = prototype.__proto__;
        return parentRecordType.allRecordAttributeProperties ?
            filteredProperties.concat(parentRecordType.allRecordAttributeProperties()) :
            filteredProperties;

    }
});


Footprint.ChildRecord = Footprint.Record.extend({
});

Footprint.ChildRecord = Footprint.Record.extend({
});

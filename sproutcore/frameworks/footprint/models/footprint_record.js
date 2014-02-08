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
Footprint.Record = SC.Record.extend(Footprint.RecordCloning, {
    primaryKey: 'id',

    // Used a pseudo-status property to track that cloning of new record's child items are complete
    // Each cloned child item will receive this READY_NEW_CLONED status for its _status property
    _status:null,
    // Used to track progress of saving the record on the server. The value is between 0 and 1
    // This only applies to records like ConfigEntity which do postSave processing on the server
    // When records are saved, their progress is set to 0, so saveInProgress will return true
    // until post processing brings the value to 1
    progress:null,
    saveInProgress: function() {
        return this.get('progress') != null && this.get('progress') >= 0 && this.get('progress') < 1;
    }.property("progress").cacheable(),

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

    // Properties not to copy or clone--typically properties that the server should take care of copying from the source
    _skipProperties:function() {return ''.w();},
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

    /***
     * Mapping of primitive attributes to other values, Each key/value takes the form:
     * key: function(cloneRecord, original record value, random number) { return key+random;}
     * where key is the attribute to map and original record value is the corresponding attribute value of the source record.
     * random provides a short timestamp for things that should be unique or replaced by the user
    **/
    _mapAttributes: { },
    /***
     * Like map attributes but for initialization. No original record value is passed in, so the key/values take the form :
     * key: function(cloneRecord, random number) { return "New'+random;}
     */
    _initialAttributes: { },

    // Properties that should never be transfered from one instance to another when updating the values of one instance to those (or the clones) of another
    _nonTransferableProperties: function() { return 'id resource_uri'.w(); },

    // Special actions for setting up a create from "scratch"
    // The sourceRecord is used to prime the pump--to give the instance essential attributes like parent references
    _createSetup: function(sourceRecord) {
        // Initialize preconfigured primitive attributes
        var self = this;
        var randomNumber = SC.DateTime.create().toFormattedString('%H_%M_%S');
        $.each(this._initialAttributes || {}, function(key, func) {
            self.set(key, func(self, randomNumber))
        });
    },
    // Special actions to take when setting up a record for cloning
    // that don't involve cloning particular attributes
    // For example, a clone might set its origin_instance to the source_record (this should just be standard)
    _cloneSetup: function(sourceRecord) {

    },
    /***
     * Sets the record's deleted property to YES. Override to do the same for nested records
     * TODO nested records should just be listed as nestedRecords so the crud state knows how
     * to create and delete all nested records
     * @private
     */
    _deleteSetup: function() {
        this.set('deleted', YES)
    },

    attributeKeys: function() {
        return $.map(this.attributes(), function(v,k) { return k;});
    }
});

/***
 * Override this to limit the class name used by the subclasses to a base class name, or to use a custom name
 * @returns {string}
 */
SC.mixin(Footprint.Record, {

    generateId: function() {
        return -Math.random(Math.floor(Math.random() * 99999999));
    },

    /***
     * Return a baseclass for certain record types
     * @param recordType
     * @returns {*}
     */
    apiRecordType: function() {
        return this;
    },

    /**
     * Map the name to somthing else for certain record types, if apiRecordType doesn't take care of it
     * @returns {null}
     */
    apiClassName: function() {
        return null;
    },

    infoPane: function() {
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

    },

    /***
     * Custom processes of a record's raw dataHash prior to saving
     * @param dataHash
     */
    processDataHash: function(dataHash, record) {
        return dataHash;
    }
});


Footprint.ChildRecord = Footprint.Record.extend({
});

Footprint.ChildRecord = Footprint.Record.extend({
});

